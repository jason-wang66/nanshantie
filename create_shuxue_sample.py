# -*- coding: utf-8 -*-
"""
漱雪纸质帖样品PDF生成脚本
A5尺寸，模拟实体印刷品效果
"""

import os

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

# 颜色定义
PAPER_WHITE = HexColor('#F5F0E6')
GOLD = HexColor('#D4B68A')
DARK_TEXT = HexColor('#5C4A3A')
LIGHT_TEXT = HexColor('#A69272')
VERMILION = HexColor('#C23B22')

# 字体路径
FONT_ZEN = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
FONT_MICRO = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

# 注册字体
pdfmetrics.registerFont(TTFont('ZenHei', FONT_ZEN))
pdfmetrics.registerFont(TTFont('MicroHei', FONT_MICRO))

# A5页面尺寸
PAGE_WIDTH, PAGE_HEIGHT = A5

_temp_files = []

def get_portrait_path(name):
    """获取山客形象路径"""
    possible_paths = [
        os.path.join(BASE_DIR, "白茶品牌", "山客形象", f"{name}.jpg"),
        os.path.join(SCRIPT_DIR, "山客形象", f"{name}.jpg"),
        os.path.join(BASE_DIR, "山客形象", f"{name}.jpg"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def get_qr_path():
    """获取微信二维码路径"""
    possible_paths = [
        os.path.join(BASE_DIR, "用户上传", "photo-1777830978310.jpg"),
        os.path.join(SCRIPT_DIR, "用户上传", "photo-1777830978310.jpg"),
        os.path.join(BASE_DIR, "用户上传", "photo-1777830978310.jpg"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def compress_image(image_path, max_width=400, quality=80):
    """压缩图片"""
    if not image_path or not os.path.exists(image_path):
        return None
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        ratio = max_width / img.width if img.width > max_width else 1
        if ratio < 1:
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        temp_path = image_path.replace('.jpg', '_temp.jpg').replace('.png', '_temp.png')
        img.save(temp_path, 'JPEG', quality=quality)
        _temp_files.append(temp_path)
        return temp_path
    except Exception as e:
        print(f"图片处理失败: {e}")
        return None

def draw_seal(c, x, y, size=25):
    """绘制朱红方印"""
    c.setStrokeColor(VERMILION)
    c.setFillColor(VERMILION)
    c.setLineWidth(1.5)
    c.rect(x, y, size, size, fill=0, stroke=1)
    c.setFont('ZenHei', 9)
    c.drawString(x + 4, y + 8, '南')

def draw_decorative_corner(c):
    """绘制左上角淡墨山水装饰"""
    c.setStrokeColor(HexColor('#D4CFC0'))
    c.setLineWidth(0.3)
    
    # 简单山形轮廓
    points = [(20, PAGE_HEIGHT - 30), (35, PAGE_HEIGHT - 50), (50, PAGE_HEIGHT - 35), 
              (65, PAGE_HEIGHT - 55), (80, PAGE_HEIGHT - 40), (95, PAGE_HEIGHT - 30)]
    
    # 使用path绘制
    p = c.beginPath()
    p.moveTo(points[0][0], points[0][1])
    for i in range(1, len(points)):
        p.lineTo(points[i][0], points[i][1])
    c.drawPath(p, stroke=1, fill=0)
    
    # 云雾线
    c.setLineWidth(0.2)
    for i in range(3):
        y = PAGE_HEIGHT - 20 - i * 8
        c.arc(25, y - 5, 40, y + 5, 0, 180)

def create_shuxue_sample():
    """生成漱雪纸质帖样品"""
    output_path = os.path.join(SCRIPT_DIR, "漱雪_纸质帖样品.pdf")
    c = canvas.Canvas(output_path, pagesize=A5)
    
    # 宣纸白底
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    
    # 左上角淡墨装饰
    draw_decorative_corner(c)
    
    # 漱雪山客形象
    portrait_path = get_portrait_path("漱雪")
    if portrait_path:
        portrait_temp = compress_image(portrait_path, max_width=200, quality=85)
        if portrait_temp:
            img = Image.open(portrait_temp)
            img_w, img_h = img.size
            
            # 页面可用高度约为 210mm * 0.55
            display_height = PAGE_HEIGHT * 0.55
            display_width = img_w * (display_height / img_h)
            
            # 如果宽度超出页面，缩放
            if display_width > PAGE_WIDTH * 0.85:
                display_width = PAGE_WIDTH * 0.85
                display_height = img_h * (display_width / img_w)
            
            x = (PAGE_WIDTH - display_width) / 2
            y = PAGE_HEIGHT - display_height - 15
            
            c.drawImage(portrait_temp, x, y, width=display_width, height=display_height, preserveAspectRatio=True)
    
    # 中间区域
    mid_y = PAGE_HEIGHT * 0.38
    
    # "漱雪" 两个大字（金色书法感）
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 42)
    c.drawCentredString(PAGE_WIDTH/2, mid_y + 30, '漱雪')
    
    # "茉莉绿茶" 小字
    c.setFillColor(DARK_TEXT)
    c.setFont('MicroHei', 14)
    c.drawCentredString(PAGE_WIDTH/2, mid_y, '茉莉绿茶')
    
    # 漱雪的故事（精简版）
    c.setFillColor(LIGHT_TEXT)
    c.setFont('MicroHei', 10)
    
    story = "大雪封山之后，另一个女子出现了。她喜欢在雪地里走，留下一串浅浅的脚印。她叫漱雪——南方有雪不易。"
    
    # 换行处理
    max_chars = 22
    story_lines = [story[i:i+max_chars] for i in range(0, len(story), max_chars)]
    
    story_y = mid_y - 30
    for line in story_lines[:3]:  # 最多3行
        c.drawCentredString(PAGE_WIDTH/2, story_y, line)
        story_y -= 18
    
    # 下方区域
    bottom_y = 80
    
    # 扫码提示
    c.setFillColor(DARK_TEXT)
    c.setFont('MicroHei', 11)
    c.drawCentredString(PAGE_WIDTH/2, bottom_y + 50, '扫码，遇见你的山客')
    
    # 微信二维码
    qr_path = get_qr_path()
    if qr_path:
        qr_temp = compress_image(qr_path, max_width=80, quality=85)
        if qr_temp:
            c.drawImage(qr_temp, PAGE_WIDTH/2 - 35, bottom_y - 5, width=70, height=70, preserveAspectRatio=True)
    
    # 右下角朱红方印
    draw_seal(c, PAGE_WIDTH - 55, 30, 28)
    
    # 保存
    c.save()
    print(f"漱雪纸质帖样品已生成: {output_path}")
    
    # 清理临时文件
    for f in _temp_files:
        try:
            if os.path.exists(f):
                os.remove(f)
        except:
            pass
    
    return output_path

if __name__ == "__main__":
    create_shuxue_sample()
