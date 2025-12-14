#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主窗口类
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from components.image_viewer import ImageViewer
import os


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VisionCompare - 图像对比工具")
        self.setGeometry(100, 100, 1200, 800)
        
        # 初始化UI
        self.init_ui()
        
        # 存储图像路径
        self.image1_path = None
        self.image2_path = None
    
    def init_ui(self):
        """初始化UI界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 加载图像按钮
        self.load_image1_btn = QPushButton("加载第一张图像")
        self.load_image1_btn.clicked.connect(self.load_image1)
        
        self.load_image2_btn = QPushButton("加载第二张图像")
        self.load_image2_btn.clicked.connect(self.load_image2)
        
        # 添加按钮到布局
        button_layout.addWidget(self.load_image1_btn)
        button_layout.addWidget(self.load_image2_btn)
        
        # 图像显示区域
        self.image_viewer = ImageViewer()
        
        # 添加控件到主布局
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.image_viewer)
        
        # 状态栏
        self.statusBar().showMessage("就绪")
    
    def load_image1(self):
        """加载第一张图像"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "选择第一张图像", 
            "", 
            "图像文件 (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            self.image1_path = file_path
            self.image_viewer.set_image1(file_path)
            self.statusBar().showMessage(f"已加载第一张图像: {os.path.basename(file_path)}")
    
    def load_image2(self):
        """加载第二张图像"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "选择第二张图像", 
            "", 
            "图像文件 (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            self.image2_path = file_path
            self.image_viewer.set_image2(file_path)
            self.statusBar().showMessage(f"已加载第二张图像: {os.path.basename(file_path)}")