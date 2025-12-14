#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VisionCompare - 图像对比工具主程序
"""

import sys
from PySide6.QtWidgets import QApplication
from components.main_window import MainWindow


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()