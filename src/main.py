#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VisionCompare - Image Comparison Tool Main Program
"""

import sys
from PySide6.QtWidgets import QApplication
from components.main_window import MainWindow


def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()