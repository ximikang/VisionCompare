# VisionCompare - Image Comparison Tool

VisionCompare is a simple and intuitive image comparison tool developed with Python and PySide6. It allows users to load and compare two images side by side.

## Features

- Load and display two images simultaneously
- Side-by-side image comparison
- Support for common image formats (PNG, JPG, JPEG, BMP, GIF)
- Intuitive graphical user interface

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main program:
```
python src/main.py
```

1. Click "Load First Image" to select the first image
2. Click "Load Second Image" to select the second image
3. Both images will be displayed side by side for comparison

## Dependencies

- Python 3.7+
- PySide6
- Pillow (PIL)

## License

MIT License
# VisionCompare

VisionCompare 是一个基于 PySide6 的图像对比工具，允许用户同时查看和比较两张图片的差异。

![界面预览](docs/preview.png) <!-- 如果有界面截图可以替换此链接 -->

## 功能特点

- 支持多种图像格式（JPEG, PNG, BMP 等）
- 提供多种图像对比模式（滑动对比、叠加对比等）
- 可调节对比参数（透明度、分割线位置等）
- 直观的图形界面操作

## 安装

### 克隆仓库

```bash
git clone <repository-url>
cd visionCompare
```

### 安装依赖

```bash
pip install -r requirements.txt
```

或者使用 pipenv:

```bash
pipenv install
```

## 使用方法

直接运行:

```bash
python src/main.py
```

或者安装后运行:

```bash
pip install .
visioncompare
```

## 开发

### 代码格式化

项目使用 black 进行代码格式化:

```bash
black .
```

### 运行测试

```bash
python -m pytest tests/
```

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

[MIT License](LICENSE)