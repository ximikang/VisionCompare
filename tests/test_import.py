#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单测试文件，验证项目导入是否正常
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """测试导入功能"""
    try:
        from components.main_window import MainWindow
        from components.image_viewer import ImageViewer
        print("所有模块导入成功")
        assert True
    except ImportError as e:
        print(f"导入失败: {e}")
        assert False

if __name__ == "__main__":
    test_imports()