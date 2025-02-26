import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Windows 默认路径
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 输入输出目录配置
INPUT_DIR = os.path.join(BASE_DIR, "input_imgs")     # 输入图片目录
OUTPUT_DIR = os.path.join(BASE_DIR, "output_texts")  # 输出文本目录

# OCR配置
OCR_LANG = "chi_sim"  # 中文简体

# 线程池配置
MAX_WORKERS = 4  # 最大工作线程数
