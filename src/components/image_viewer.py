#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image Viewer Component
"""

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PIL import Image
import numpy as np


class ImageViewer(QWidget):
    """Image Viewer"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Image data
        self.pixmap1 = None
        self.pixmap2 = None
    
    def init_ui(self):
        """Initialize UI"""
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        # Create two labels for displaying images
        self.label1 = QLabel("Please load the first image")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setMinimumSize(400, 300)
        self.label1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label1.setStyleSheet("border: 1px solid gray;")
        
        self.label2 = QLabel("Please load the second image")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setMinimumSize(400, 300)
        self.label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label2.setStyleSheet("border: 1px solid gray;")
        
        # Add to layout
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
    
    def set_image1(self, image_path):
        """Set the first image"""
        try:
            pixmap = QPixmap(image_path)
            self.pixmap1 = pixmap
            
            # Scale image to fit label size
            scaled_pixmap = pixmap.scaled(
                self.label1.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            self.label1.setPixmap(scaled_pixmap)
            self.label1.setText("")
        except Exception as e:
            self.label1.setText(f"Failed to load image: {str(e)}")
    
    def set_image2(self, image_path):
        """Set the second image"""
        try:
            pixmap = QPixmap(image_path)
            self.pixmap2 = pixmap
            
            # Scale image to fit label size
            scaled_pixmap = pixmap.scaled(
                self.label2.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            self.label2.setPixmap(scaled_pixmap)
            self.label2.setText("")
        except Exception as e:
            self.label2.setText(f"Failed to load image: {str(e)}")