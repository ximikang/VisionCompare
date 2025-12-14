#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
High-Performance Dual Image Viewer with Efficient Pixel RGB Overlay
"""
import os
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QGraphicsView, 
                               QGraphicsScene, QGraphicsPixmapItem, QFrame)
from PySide6.QtCore import Qt, Signal, QPointF, QRectF, QSize
from PySide6.QtGui import (QPixmap, QWheelEvent, QPainter, QColor, 
                           QPen, QFont, QImage)
import math

class ProGraphicsView(QGraphicsView):
    state_changed = Signal(float, float, float)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing, False) 
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setOptimizationFlags(QGraphicsView.DontAdjustForAntialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("background-color: #202020;")
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self._pixmap_item = None
        self._image = None
        self._is_programmatic_change = False
        self.horizontalScrollBar().valueChanged.connect(self._notify_change)
        self.verticalScrollBar().valueChanged.connect(self._notify_change)
        # --- pixel overlay config ---
        self.pixel_display_min_scale = 16.0   # show RGB when one image pixel >= this many screen pixels
        self._max_overlay_pixels = 4000       # cap to avoid huge draws

    def load_image(self, pixmap: QPixmap):
        self.scene.clear()
        self._pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self._pixmap_item)
        self._image = pixmap.toImage()
        self.scene.setSceneRect(QRectF(pixmap.rect()))
        self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)

    def wheelEvent(self, event: QWheelEvent):
        zoom_in = 1.15
        zoom_out = 1.0 / zoom_in
        factor = zoom_in if event.angleDelta().y() > 0 else zoom_out
        current_scale = self.transform().m11()
        if factor > 1 and current_scale > 1000:
            return
        if factor < 1 and current_scale < 0.05:
            return
        self.scale(factor, factor)
        self.viewport().update() 
        self._notify_change()
        event.accept()

    def _notify_change(self):
        if self._is_programmatic_change or self.scene.width() == 0:
            return
        view_rect = self.mapToScene(self.viewport().rect()).boundingRect()
        center = view_rect.center()
        scene_rect = self.scene.sceneRect()
        x_ratio = center.x() / scene_rect.width() if scene_rect.width() > 0 else 0.5
        y_ratio = center.y() / scene_rect.height() if scene_rect.height() > 0 else 0.5
        current_scale = self.transform().m11()
        self.state_changed.emit(current_scale, x_ratio, y_ratio)

    def sync_state(self, scale, x_ratio, y_ratio):
        if self.scene.width() == 0: return
        self._is_programmatic_change = True
        try:
            new_transform = self.transform()
            new_transform.setMatrix(scale, new_transform.m12(), new_transform.m13(),
                                    new_transform.m21(), scale, new_transform.m23(),
                                    new_transform.m31(), new_transform.m32(), new_transform.m33())
            self.setTransform(new_transform)
            scene_rect = self.scene.sceneRect()
            target_x = scene_rect.width() * x_ratio
            target_y = scene_rect.height() * y_ratio
            self.centerOn(target_x, target_y)
        finally:
            self._is_programmatic_change = False

    def drawForeground(self, painter: QPainter, rect: QRectF):
        """高效像素RGB叠加，三行显示RGB，字体颜色为对应通道色，亮度不变，像素隔离线更细"""
        if self._image is None:
            return
        pixel_scale = self.transform().m11()
        if pixel_scale < self.pixel_display_min_scale:
            return

        visible = self.mapToScene(self.viewport().rect()).boundingRect()
        ix1 = max(0, int(visible.left()))
        iy1 = max(0, int(visible.top()))
        ix2 = min(self._image.width() - 1, int(visible.right()))
        iy2 = min(self._image.height() - 1, int(visible.bottom()))
        if ix2 < ix1 or iy2 < iy1:
            return

        pixel_size = pixel_scale

        min_text_box = 18
        if pixel_size < min_text_box:
            return

        w = ix2 - ix1 + 1
        h = iy2 - iy1 + 1
        total = w * h
        step = 1
        if total > self._max_overlay_pixels:
            step = int(math.ceil(math.sqrt(total / self._max_overlay_pixels)))
            if step < 1: step = 1

        painter.save()
        painter.resetTransform()

        font_size = max(6, pixel_size * 0.22)
        font = QFont("Consolas")
        font.setStyleHint(QFont.Monospace)
        font.setPointSizeF(font_size)
        painter.setFont(font)

        line_height = pixel_size / 3.0

        # 更细的像素隔离线
        grid_pen = QPen(QColor(180, 180, 180, 180))
        grid_pen.setWidthF(0.7)
        grid_pen.setCosmetic(True)

        for yy in range(iy1, iy2 + 1, step):
            for xx in range(ix1, ix2 + 1, step):
                rgb = QColor(self._image.pixel(xx, yy))
                r, g, b = rgb.red(), rgb.green(), rgb.blue()
                pt = self.mapFromScene(QPointF(xx + 0.5, yy + 0.5))
                box_size = pixel_size
                bg_rect = QRectF(
                    pt.x() - box_size/2 + 1, pt.y() - box_size/2 + 1,
                    box_size - 2, box_size - 2
                )
                # 只用透明度做背景，亮度不变
                painter.fillRect(bg_rect, QColor(r, g, b, 80))

                # 画更细的像素格线
                painter.setPen(grid_pen)
                painter.drawRect(bg_rect)

                # 三行分别显示R/G/B，字体颜色为对应通道色，亮度与原像素一致
                rgb_colors = [
                    QColor(r, 0, 0), 
                    QColor(0, g, 0), 
                    QColor(0, 0, b)
                ]
                for i, (val, color) in enumerate(zip((r, g, b), rgb_colors)):
                    # 保持亮度不变，使用原像素亮度
                    orig_lum = r * 0.299 + g * 0.587 + b * 0.114
                    if color.red() > 0:
                        pen_color = QColor(r, 0, 0)
                    elif color.green() > 0:
                        pen_color = QColor(0, g, 0)
                    else:
                        pen_color = QColor(0, 0, b)
                    # 保持亮度不变（不做亮度增强或反色）
                    painter.setPen(pen_color)
                    line_rect = QRectF(
                        bg_rect.left(),
                        bg_rect.top() + i * line_height,
                        bg_rect.width(),
                        line_height
                    )
                    painter.drawText(line_rect, Qt.AlignCenter, str(val))
        painter.restore()

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pixel Peeping Analyzer")
        self.resize(1200, 800)
        layout = QHBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        self.view1 = ProGraphicsView()
        self.view2 = ProGraphicsView()
        layout.addWidget(self.view1)
        layout.addWidget(self.view2)
        self.view1.state_changed.connect(lambda s, x, y: self.sync_views(self.view2, s, x, y))
        self.view2.state_changed.connect(lambda s, x, y: self.sync_views(self.view1, s, x, y))
        self.sync_enabled = True
    def sync_views(self, target_view, scale, x_ratio, y_ratio):
        if self.sync_enabled:
            target_view.sync_state(scale, x_ratio, y_ratio)

# -----------------------------------------------------------------------------
# 测试代码
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    def create_gradient_pixmap():
        img = QImage(256, 256, QImage.Format_RGB32)
        for y in range(256):
            for x in range(256):
                img.setPixelColor(x, y, QColor(x, y, 128)) 
        return QPixmap.fromImage(img)

    app = QApplication(sys.argv)
    viewer = ImageViewer()
    pm = create_gradient_pixmap()
    viewer.view1.load_image(pm)
    viewer.view2.load_image(pm)
    viewer.show()
    sys.exit(app.exec())