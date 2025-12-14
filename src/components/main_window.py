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
        
        # Load both images button
        self.load_both_images_btn = QPushButton("Load Both Images")
        self.load_both_images_btn.clicked.connect(self.load_both_images)
        
        # Reset zoom button
        self.reset_zoom_btn = QPushButton("Reset Zoom")
        self.reset_zoom_btn.clicked.connect(self.reset_zoom)
        self.reset_zoom_btn.setEnabled(False)
        
        # Add buttons to layout
        button_layout.addWidget(self.load_image1_btn)
        button_layout.addWidget(self.load_image2_btn)
        button_layout.addWidget(self.load_both_images_btn)
        button_layout.addWidget(self.reset_zoom_btn)
        
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
            pixmap = QPixmap(file_path)
            self.image_viewer.view1.load_image(pixmap)
            self.statusBar().showMessage(f"Loaded first image: {os.path.basename(file_path)}")
            self.update_button_states()
    
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
            pixmap = QPixmap(file_path)
            self.image_viewer.view2.load_image(pixmap)
            self.statusBar().showMessage(f"Loaded second image: {os.path.basename(file_path)}")
            self.update_button_states()
    
    def load_both_images(self):
        """Load both images at once"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Two Images",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        # Check if exactly two files were selected
        if len(file_paths) == 2:
            self.image1_path = file_paths[0]
            self.image2_path = file_paths[1]
            
            pixmap1 = QPixmap(file_paths[0])
            pixmap2 = QPixmap(file_paths[1])
            
            self.image_viewer.view1.load_image(pixmap1)
            self.image_viewer.view2.load_image(pixmap2)
            
            self.statusBar().showMessage(
                f"Loaded images: {os.path.basename(file_paths[0])}, {os.path.basename(file_paths[1])}"
            )
            self.update_button_states()
        elif len(file_paths) > 0:
            # If only one or more than two files selected, show warning
            QMessageBox.warning(
                self,
                "Invalid Selection",
                "Please select exactly two images."
            )
    
    def reset_zoom(self):
        """Reset zoom for both images"""
        if self.image1_path:
            self.image_viewer.view1.fitInView(self.image_viewer.view1.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        if self.image2_path:
            self.image_viewer.view2.fitInView(self.image_viewer.view2.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        self.statusBar().showMessage("Zoom reset to 100%")
    
    def update_button_states(self):
        """Update button enabled states based on loaded images"""
        images_loaded = self.image1_path is not None and self.image2_path is not None
        self.reset_zoom_btn.setEnabled(images_loaded)