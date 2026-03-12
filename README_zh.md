# IIIF 下载器

一个用于解析 IIIF (国际图像互操作框架) 格式并下载图像的 Python 应用程序，具有用户友好的图形界面。

## 功能特点

- **JSON 输入支持**：直接接受 IIIF JSON 数据
- **自动提取图像 URL**：从 IIIF manifest.json 中提取所有高分辨率图像 URL
- **批量下载**：下载所有图像，带有进度条和速度显示
- **按作品名称创建文件夹**：创建以作品名称命名的文件夹，便于组织存储
- **默认保存路径**：使用系统下载文件夹作为默认保存位置
- **取消下载**：允许用户随时取消下载过程
- **用户友好界面**：干净直观的 GUI，带有输入/输出区域的滚动条

## 系统要求

- Windows 7 或更高版本
- 无需安装 Python（独立可执行文件）

## 使用方法

1. **下载可执行文件**：从 `dist` 文件夹获取 `IIIF-Downloader.exe`
2. **运行应用程序**：双击 `IIIF-Downloader.exe`
3. **输入 IIIF JSON**：将 IIIF JSON 数据粘贴到输入区域
4. **选择保存路径**：选择保存下载图像的位置（默认：下载文件夹）
5. **下载图像**：点击"下载全部图片"开始下载
6. **取消下载**：点击"取消下载"停止下载过程

## 工作原理

1. **JSON 解析**：应用程序解析 IIIF JSON 数据以提取图像 URL
2. **图像提取**：从 manifest 中提取所有高分辨率图像 URL
3. **批量下载**：在单独的线程中下载所有图像，保持 UI 响应
4. **进度跟踪**：显示实时进度和下载速度
5. **文件夹创建**：创建以作品名称命名的文件夹来存储下载的图像

## 技术细节

- **核心技术**：Python、Tkinter (GUI)、Requests (HTTP)、tqdm (进度条)
- **打包**：使用 PyInstaller 创建独立可执行文件
- **架构**：模块化设计，具有单独的解析、下载和 UI 模块

## 开发

### 先决条件

- Python 3.7+
- pip

### 安装

```bash
# 克隆仓库
git clone <repository-url>
cd IIIF-downloader

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行应用程序
python main.py
```

### 打包

```bash
# 创建可执行文件
pyinstaller --onefile --windowed --name IIIF-Downloader main.py

# 可执行文件将在 dist 文件夹中
```

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 LICENSE 文件。

## 致谢

- [IIIF (国际图像互操作框架)](https://iiif.io/)
- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Requests](https://requests.readthedocs.io/)
- [tqdm](https://tqdm.github.io/)