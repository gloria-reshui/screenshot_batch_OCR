import cv2
import numpy as np
from PIL import Image

def preprocess_image(image):
    """图像预处理函数
    
    Args:
        image: PIL.Image对象
        
    Returns:
        PIL.Image: 预处理后的图像
    """
    # 转换为OpenCV格式
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 自适应阈值二值化
    binary = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, # 邻域大小
        2  # 常数项
    )
    
    # 降噪
    denoised = cv2.fastNlMeansDenoising(binary)
    
    # 转回PIL格式
    return Image.fromarray(denoised)

def create_markdown(text, title=None):
    """生成Markdown格式文本
    
    Args:
        text: OCR识别出的文本
        title: 可选的标题
        
    Returns:
        str: Markdown格式的文本
    """
    md = ""
    
    # 添加标题
    if title:
        md += f"# {title}\n\n"
    
    # 处理正文
    paragraphs = text.split('\n\n')
    for p in paragraphs:
        if p.strip():
            md += f"{p.strip()}\n\n"
            
    return md.strip()
