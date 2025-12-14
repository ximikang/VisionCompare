#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main Window Class
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
    """Main Window Class"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VisionCompare - Image Comparison Tool")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize UI
        self.init_ui()
        
        # Store image paths
        self.image1_path = None
        self.image2_path = None
    
    def init_ui(self):
        """Initialize UI interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Load image buttons
        self.load_image1_btn = QPushButton("Load First Image")
        self.load_image1_btn.clicked.connect(self.load_image1)
        
        self.load_image2_btn = QPushButton("Load Second Image")
        self.load_image2_btn.clicked.connect(self.load_image2)
        
        # Add buttons to layout
        button_layout.addWidget(self.load_image1_btn)
        button_layout.addWidget(self.load_image2_btn)
        
        # Image display area
        self.image_viewer = ImageViewer()
        
        # Add widgets to main layout
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.image_viewer)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def load_image1(self):
        """Load the first image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select First Image", 
            "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            self.image1_path = file_path
            self.image_viewer.set_image1(file_path)
            self.statusBar().showMessage(f"Loaded first image: {os.path.basename(file_path)}")
    
    def load_image2(self):
        """Load the second image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Second Image", 
            "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            self.image2_path = file_path
            self.image_viewer.set_image2(file_path)
            self.statusBar().showMessage(f"Loaded second image: {os.path.basename(file_path)}")