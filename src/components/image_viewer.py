#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图像查看器组件
"""

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PIL import Image
import numpy as np


class ImageViewer(QWidget):
    """图像查看器"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # 图像数据
        self.pixmap1 = None
        self.pixmap2 = None
    
    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        # 创建两个标签用于显示图像
        self.label1 = QLabel("请加载第一张图像")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setMinimumSize(400, 300)
        self.label1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label1.setStyleSheet("border: 1px solid gray;")
        
        self.label2 = QLabel("请加载第二张图像")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setMinimumSize(400, 300)
        self.label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label2.setStyleSheet("border: 1px solid gray;")
        
        # 添加到布局
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
    
    def set_image1(self, image_path):
        """设置第一张图像"""
        try:
            pixmap = QPixmap(image_path)
            self.pixmap1 = pixmap
            
            # 缩放图像以适应标签大小
            scaled_pixmap = pixmap.scaled(
                self.label1.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            self.label1.setPixmap(scaled_pixmap)
            self.label1.setText("")
        except Exception as e:
            self.label1.setText(f"加载图像失败: {str(e)}")
    
    def set_image2(self, image_path):
        """设置第二张图像"""
        try:
            pixmap = QPixmap(image_path)
            self.pixmap2 = pixmap
            
            # 缩放图像以适应标签大小
            scaled_pixmap = pixmap.scaled(
                self.label2.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            self.label2.setPixmap(scaled_pixmap)
            self.label2.setText("")
        except Exception as e:
            self.label2.setText(f"加载图像失败: {str(e)}")