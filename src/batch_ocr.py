import os
import pytesseract
from PIL import Image
import time
from concurrent.futures import ThreadPoolExecutor

# ============== 用户配置区 ==============
# 使用相对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input_imgs")     # 输入图片目录
OUTPUT_DIR = os.path.join(BASE_DIR, "output_texts")  # 输出文本目录
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Tesseract路径
LANGUAGES = 'chi_sim+eng'  # 识别语言：中文+英文
THREADS = 4                # 并发线程数（根据CPU核心数调整）

# 支持的图片格式
IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')

# OCR配置
OCR_CONFIG = '--psm 6 -c preserve_interword_spaces=1'

# ============== 核心函数 ==============
def process_image(img_path):
    """处理单张图片的OCR任务
    Args:
        img_path: 图片路径
    Returns:
        tuple: (是否成功, 消息)
    """
    try:
        # 1. 读取图片
        img = Image.open(img_path)
        
        # 2. 图像预处理（按需调整参数）
        img = img.convert('L')  # 灰度化
        # img = img.point(lambda x: 0 if x < 128 else 255)  # 二值化
        
        # 3. 执行OCR
        text = pytesseract.image_to_string(
            img,
            lang=LANGUAGES,
            config='--psm 6 -c preserve_interword_spaces=1'
        )
        
        # 4. 清理结果
        clean_text = "\n".join([line.strip() for line in text.split('\n') if line.strip()])
        
        # 添加markdown格式
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        formatted_text = f"# OCR结果: {base_name}\n\n---\n\n{clean_text}\n\n---\n_由OCR工具生成于 {time.strftime('%Y-%m-%d %H:%M:%S')}_"
        
        # 5. 保存结果
        output_path = os.path.join(OUTPUT_DIR, f"{base_name}.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
        
        return True, img_path
    except Exception as e:
        return False, f"{img_path}: {str(e)}"

# ============== 主程序 ==============
def main():
    start_time = time.time()
    
    # 检查路径
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    
    # 检查Tesseract是否安装
    if not os.path.exists(TESSERACT_PATH):
        print(f"错误：找不到Tesseract程序，请确认安装路径：{TESSERACT_PATH}")
        return

    # 检查输入目录
    if not os.path.exists(INPUT_DIR):
        print(f"错误：输入目录不存在：{INPUT_DIR}")
        return

    # 获取图片列表
    image_paths = [
        os.path.join(INPUT_DIR, f) 
        for f in os.listdir(INPUT_DIR)
        if f.lower().endswith(IMAGE_EXTS)
    ]

    if not image_paths:
        print(f"警告：在 {INPUT_DIR} 中没有找到支持的图片文件")
        print(f"支持的格式：{', '.join(IMAGE_EXTS)}")
        return
    
    # 显示处理信息
    total = len(image_paths)
    print(f"找到 {total} 个图片文件，开始处理...\n")

    results = []
    # 并发处理（线程池）
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(process_image, path) for path in image_paths]
        
        # 实时显示进度
        completed = 0
        for future in futures:
            completed += 1
            status, msg = future.result()
            results.append((status, msg))
            print(f"进度: [{completed}/{total}] {os.path.basename(msg)}")
            if not status:
                print(f"  ↳ 失败: {msg}")
    
    # 统计结果
    success_count = 0
    error_log = []
    for status, msg in results:
        if status:
            success_count += 1
        else:
            error_log.append(msg)
    
    # 输出报告
    print(f"处理完成！用时：{time.time() - start_time:.2f}秒")
    print(f"成功: {success_count}张, 失败: {len(error_log)}张")
    if error_log:
        print("\n失败文件列表：")
        for err in error_log:
            print(f" - {err}")
    
    # 完成后自动打开输出目录（可选）
    os.startfile(OUTPUT_DIR)

if __name__ == "__main__":
    main()
