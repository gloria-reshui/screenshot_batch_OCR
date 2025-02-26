# Screenshot Batch OCR

> 🔍 一款基于本地TesseractOCR的截图批量转Markdown工具，让PC端截图一键变为可编辑文本。
> A local screenshot-to-Markdown batch converter powered by TesseractOCR, instantly turning your screenshot text into editable content.

利用最新版TesseractOCR自动将电脑截图转换为 Markdown 格式文本的工具，方便批量导入大量截图至Obsidian等MD笔记文件夹。支持多线程加速和图像预处理优化。

*部署用时：顺利的话，预计15分钟*
## 效果演示

![gif](https://github.com/user-attachments/assets/61f719b6-d23a-4cca-972e-d58ea9572437)

## 开发原因

日常学习中，我经常需要将截图中的文字内容快速整理到文档或笔记中。手动输入耗时耗力，现有OCR光学识别工具和截图没有我喜欢的强关联工作流工具。因此开发此工具，实现以下目标：

- **一键转换**：截图直接生成结构化 Markdown 文件
- **批量处理**：高效处理大量截图文件，快速
- **精准识别**：通过图像预处理提升 OCR 准确率
- **数据安全**：拒绝使用百度云等OCR等API接口，脚本处理路径在本地

## 🦭额外特性

### 1. 多线程加速
- **技术原理**：利用 Python 的 `ThreadPoolExecutor` 并行处理多个截图文件，相比单线程处理速度提升 2-5 倍（取决于 CPU 核心数）

### 2. 图像二值化
- **技术原理**：将彩色/灰度图像转换为黑白两色，消除背景噪点干扰，使文字边缘更清晰

### 3. Markdown 格式化
- 自动添加标题（基于文件名）
- 保留段落换行和基本标点
- 支持后续手动扩展模板（如添加代码块标记）
 
### 基础功能文件结构示例

#### input_imgs/              # 原始图片目录（自动截图保存）
- 发票1.png
- 合同截图.jpg
#### output_texts/           # OCR结果目录（脚本运行后创建）
- 发票1.md
- 合同截图.md
#### scr
- batch_ocr.py            # 批量处理脚本


## 🛠️ 安装步骤

### 前置要求
- Python 3.8+ (推荐 3.10)
- Tesseract OCR 5.0+

### 步骤 1：安装 Tesseract OCR

#### Windows
1. 前往 [Tesseract 官方下载页](https://github.com/UB-Mannheim/tesseract/wiki)  
2. 下载并运行 `tesseract-ocr-w64-setup.exe`（最新版）  
3. **安装时勾选以下选项**：  
   ✅ 添加 Tesseract 到系统 PATH  
   ✅ 中文语言包（Chinese）  

#### macOS (Homebrew)
```bash
brew install tesseract
# 下载中文语言包
wget -P /usr/local/share/tessdata https://ghproxy.com/https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata 
```

#### Linux (Debian/Ubuntu)

```
sudo apt install tesseract-ocr tesseract-ocr-chi-s
```

### 步骤 2：配置 Python 环境

1. 克隆仓库并进入目录：
```git clone https://github.com/你的用户名/sreenshot_batch_ocr.git
cd sreenshot_batch_ocr
```

2. 安装 Python 依赖：
```
pip install -r requirements.txt
```

### 步骤 3：**配置 Tesseract 路径**

修改 `src/config.py` 中的 `TESSERACT_PATH` 为你的实际安装路径：

```
# Windows 默认路径
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# macOS/Linux 默认路径
# TESSERACT_PATH = "/usr/local/bin/tesseract"
```

#### 下载中文语言包

```
wget https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata
mkdir tessdata
mv chi_sim.traineddata tessdata/

```
- 确认下载好的chi_sim.traineddata文件在tessdata文件夹下

### 步骤 4：验证安装

1. **检查 Tesseract 路径**
    
    - Windows: 确保 `C:\Program Files\Tesseract-OCR\tesseract.exe` 存在
        
    - macOS/Linux: 终端运行 `which tesseract` 应返回有效路径才对
        
2. **测试 OCR 功能**

- 放入测试图片

```
python batch_ocr.py --input examples/input_images --output test_output
```
✅ 成功运行后，`test_output` 目录将生成 `.md` 文件

3. **测试拓展的配置源码**

```
# 在 batch_ocr.py 中添加以下代码
from config import TESSERACT_PATH
print(f"Tesseract 路径: {TESSERACT_PATH}")
```
✅ 应输出正确的 Tesseract 可执行文件路径。
```
# 在 batch_ocr.py 中添加以下代码
from utils import preprocess_image
from PIL import Image

# 测试图像预处理
img = Image.open("examples/input_images/sample1.png")
processed_img = preprocess_image(img)
processed_img.save("test_output/processed_sample1.png")
```
 **测试 `utils.py` 功能**
 ✅ 应生成灰度化 + 二值化处理后的图片。
 
### ⚡ 实现截图自动保存设置：

**设置截图（win快捷键：win+shift+S）自动保存**
1. 搜索并找到**截图工具**（win直接搜索）
2. 右侧三点找到设置
3. 打开截图保存开关：自动保存原始截图
4. 更改保存文件夹至目标路径**input_imgs**
---

### 🚨 故障排查

|错误现象|解决方案|
|---|---|
|`TesseractNotFoundError`|修改 `src/config.py` 中的 `TESSERACT_PATH` 为你的实际安装路径|
|中文识别为乱码|检查 `tessdata` 目录是否包含 `chi_sim.traineddata` 文件|
|`No module named 'PIL'`|重新安装 Pillow：`pip install --force-reinstall Pillow`|
|处理速度慢|减少线程数：`python screenshot_batch_ocr.py --input ... --output ... --threads 2`|

---

## License_开源协议

MIT License

Copyright (c) 2025 Reshui

Permission is hereby granted, free of charge, to any person obtaining a copy
of this tool and associated documentation files, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of them.

## **About AUTHORS_关于我**

热水_Reshui，an independent philosopher or somebody.
Sometimes make tools for girls fun and usage.
