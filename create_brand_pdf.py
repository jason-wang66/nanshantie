# -*- coding: utf-8 -*-
"""
南山帖品牌手册PDF生成脚本
新中式雅致风格 - 黑金+宣纸白底
"""

import os
import sys

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 假设山客形象在 SCRIPT_DIR/../山客形象/ 或者 SCRIPT_DIR/山客形象/
BASE_DIR = os.path.dirname(SCRIPT_DIR)  # 工作目录

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

# 颜色定义
BLACK_BG = HexColor('#1a1a1a')
GOLD = HexColor('#D4B68A')
PAPER_WHITE = HexColor('#F5F0E6')
VERMILION = HexColor('#C23B22')
DARK_TEXT = HexColor('#5C4A3A')
LIGHT_TEXT = HexColor('#A69272')

# 字体路径
FONT_ZEN = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
FONT_MICRO = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

# 注册字体
pdfmetrics.registerFont(TTFont('ZenHei', FONT_ZEN))
pdfmetrics.registerFont(TTFont('MicroHei', FONT_MICRO))

# 页面尺寸
PAGE_WIDTH, PAGE_HEIGHT = A4

# 资源路径函数
def get_portrait_path(name):
    """获取山客形象路径"""
    # 尝试多种可能的位置
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

# 产品数据（从抽签_final.html提取）
PRODUCTS = [
    {"id": "tongmeng", "name": "童濛", "teaName": "白毫银针", "season": "春", 
     "story": "春山初醒，晨雾未散。露水从叶尖滑落，跌进泥土里，发出极轻的声响。有个孩子赤脚走过山径，衣襟上沾着青草的汁液，眼睛像刚洗过的天空。他看什么都新鲜，看什么都欢喜。",
     "flavor": "毫香清幽，如春日晨露。入口鲜甜，回甘绵长，带有淡淡的花香。",
     "value": "政和核心产区，明前头采，芽头肥壮，白毫密披，极具收藏价值。"},
    {"id": "fulan", "name": "浮岚", "teaName": "福建高山绿茶", "season": "春", 
     "story": "午后，山谷里起了雾。不是浓得化不开的那种，而是轻薄的，游走的，像是山在呼吸。雾从溪面升起，绕过松林，在半山腰停住。",
     "flavor": "清香淡雅，如山间雾气。入口鲜爽，带有淡淡的豆香与板栗香。",
     "value": "政和星溪乡海拔1200米高山茶园，云雾缭绕，品质优异。"},
    {"id": "buqi", "name": "不器", "teaName": "白牡丹", "season": "夏", 
     "story": "夏日漫长，蝉声如织。树荫下坐着一个人，他面前摆着粗陶碗，碗里盛着清水。他不拒绝任何人，也不强留任何人。他的性子温和，不偏不倚，像是山间的风。",
     "flavor": "花香馥郁，如夏日晚风。入口甘甜，有茉莉与兰花的复合香气。",
     "value": "政和白茶核心产区，一芽一二叶标准采摘，品质上乘。"},
    {"id": "dangui", "name": "丹桂", "teaName": "桂花红茶", "season": "秋", 
     "story": "入秋之前，院子里那棵桂树先开了花。不是满树金黄，只是疏疏几簇，香气却已经藏不住了。",
     "flavor": "桂香浓郁，如金秋时节。入口甜润，桂花的香与红茶的醇完美融合。",
     "value": "政和高山茶园，桂花与红茶窨制而成，秋日限定。"},
    {"id": "guilan", "name": "桂兰", "teaName": "肉桂", "season": "秋", 
     "story": "秋天深了，山里的桂树与兰草同开。她身上既有桂的冲，又有兰的静。她走路带风，说话却轻；她性子烈，却从不伤人。",
     "flavor": "桂皮辛香，如秋山深处。入口醇厚，岩韵显赫，辛辣中带花果香。",
     "value": "政和高山岩茶产区，肉桂品种，岩骨花香，越品越有层次。"},
    {"id": "tingzong", "name": "听枞", "teaName": "老枞", "season": "秋", 
     "story": "深山里有棵老枞，树龄已不可考。他常坐在树下，听风穿过枝叶的声音。他听了几十年，从少年听到白头。",
     "flavor": "枞韵幽深，如老林古道。入口醇厚，有苔藓味与粽叶香。",
     "value": "政和高山老枞茶树，树龄逾百年，枞韵独特，极具品鉴价值。"},
    {"id": "tianxiang", "name": "天香", "teaName": "大红袍", "season": "秋", 
     "story": "他住在山间一处僻静院落，院中植兰养桂，墙上挂着一幅「天香」的匾额。有人问天香是什么意思，他说天香就是天上的香气。",
     "flavor": "岩骨花香，如深山幽谷。入口醇厚，岩韵显赫，香气馥郁有层次。",
     "value": "政和岩茶核心产区，大红袍品种，岩骨花香，品质上乘。"},
    {"id": "lvshuang", "name": "履霜", "teaName": "工夫红茶", "season": "冬", 
     "story": "第一场霜落下来的时候，她来了。她踩在霜叶上，发出细微的碎裂声。她叫履霜——是踩在冬天边缘的人，也是带来温暖的人。",
     "flavor": "醇厚甘甜，如冬日暖阳。入口绵柔，有蜜香与薯香，回甘持久。",
     "value": "政和工夫红茶工艺，冬季采摘，内质丰富，越存越醇。"},
    {"id": "shuxue", "name": "漱雪", "teaName": "茉莉绿茶", "season": "冬", 
     "story": "大雪封山之后，另一个女子出现了。她喜欢在雪地里走，留下一串浅浅的脚印。她叫漱雪——南方有雪不易。",
     "flavor": "茉莉清香，如雪后初晴。入口鲜灵，有茉莉花的清雅与绿茶的鲜爽。",
     "value": "福建茉莉花茶传统窨制工艺，七窨一提，花香入骨。"},
    {"id": "shuyue", "name": "漱月", "teaName": "茉莉红茶", "season": "冬", 
     "story": "月圆那夜，有人在溪边掬水。水里有月亮的倒影，她掬起来，月亮就碎了；再掬，又圆了。她叫漱月——是用溪水洗月亮的人。",
     "flavor": "花香与茶香交融，如月光如水。入口甜润，茉莉的清与红茶的醇相得益彰。",
     "value": "福建茉莉花与红茶的完美结合，创新工艺，限量发售。"},
    {"id": "moli", "name": "莫离", "teaName": "茉莉银针", "season": "四时", 
     "story": "她住在山脚下那间小屋，屋前种着茉莉。花开的时候，满院子都是白的。她叫莫离——花与人，都不分离。",
     "flavor": "茉莉银针，如始终如一的守候。入口甘甜，花香持久，回味悠长。",
     "value": "福建茉莉花茶巅峰之作，银针为骨，茉莉为魂，四时皆宜。"},
    {"id": "banjian", "name": "半见", "teaName": "陈皮白茶", "season": "四时", 
     "story": "她喜欢躲在帘子后面，看外面的人来人往。不是害羞，而是觉得，保持一点距离刚刚好。她叫自己半见——半藏半显，半开半合。",
     "flavor": "陈皮与白茶交融，如光阴流转。入口甜润，有陈皮的果香与白茶的甘醇。",
     "value": "政和白茶与新会陈皮结合，创新工艺，跨界搭配，风味独特。"},
    {"id": "buzhi", "name": "步止", "teaName": "白茶饼", "season": "传说", 
     "story": "他走了很远很远的路，终于在这座山前停下来。不是走不动了，而是觉得，这里就是他要找的地方。他叫步止——不是止步不前，而是知道该在哪里停下来。",
     "flavor": "醇厚甘甜，如秋日暖阳。入口绵柔，有枣香与药香，回甘悠长。",
     "value": "政和白茶核心产区，陈化多年，滋味醇厚，具收藏价值。"},
    {"id": "wuji", "name": "无羁", "teaName": "17年白茶饼", "season": "传说", 
     "story": "他骑马走过很多地方，但他从不在任何一个地方停留太久。但有一年，他来到南山，遇到一条灵缇，他停了下来，这一停，就是很多年。",
     "flavor": "陈香幽远，如岁月沉淀。入口甘醇，有枣香与药香，陈韵悠长。",
     "value": "政和白茶，2017年陈化至今，七年老茶，滋味醇厚，极具收藏价值。"},
    {"id": "nanshan", "name": "南山", "teaName": "马年茶饼", "season": "传说", 
     "story": "这座山没有名字，山里的人就叫它南山。后来有个孩子出生在山下，属马那年家里做了批茶饼，他说叫马年茶。他养了条藏獒，取名厚重。",
     "flavor": "沉稳厚实，如南山之重。入口绵长，有陈香与木质香，回甘悠远。",
     "value": "政和白茶，2012年马年茶饼，陈化十余年，滋味醇厚，收藏珍品。"},
]

# 四季分组
SPRING = [p for p in PRODUCTS if p["season"] == "春"]
SUMMER = [p for p in PRODUCTS if p["season"] == "夏"]
AUTUMN = [p for p in PRODUCTS if p["season"] == "秋"]
WINTER = [p for p in PRODUCTS if p["season"] == "冬"]
FOUR_SEASONS = [p for p in PRODUCTS if p["season"] == "四时"]
LEGEND = [p for p in PRODUCTS if p["season"] == "传说"]

_temp_files = []  # 临时文件列表

def compress_image(image_path, max_width=400, quality=80):
    """压缩图片以减小PDF大小"""
    if not image_path or not os.path.exists(image_path):
        return None
    try:
        img = Image.open(image_path)
        # 保持宽高比
        ratio = max_width / img.width if img.width > max_width else 1
        if ratio < 1:
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        # 保存为临时文件
        temp_path = image_path.replace('.jpg', '_temp.jpg').replace('.png', '_temp.png')
        img = img.convert('RGB')
        img.save(temp_path, 'JPEG', quality=quality)
        _temp_files.append(temp_path)
        return temp_path
    except Exception as e:
        print(f"图片处理失败 {image_path}: {e}")
        return None

def draw_seal(c, x, y, size=30):
    """绘制朱红方印"""
    c.setStrokeColor(VERMILION)
    c.setFillColor(VERMILION)
    c.setLineWidth(1.5)
    c.rect(x, y, size, size, fill=0, stroke=1)
    c.setFont('ZenHei', 10)
    c.drawString(x + 5, y + 10, '南')

def draw_cover_page(c):
    """封面页 - 黑底金字"""
    c.setFillColor(BLACK_BG)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    
    # 金色品牌名
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 72)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 40, '南山帖')
    
    # 副标题
    c.setFont('MicroHei', 16)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 30, '政和 · 白茶')
    
    # 底部装饰线
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(PAGE_WIDTH/2 - 80, PAGE_HEIGHT/2 - 60, PAGE_WIDTH/2 + 80, PAGE_HEIGHT/2 - 60)
    
    # 底部小字
    c.setFillColor(LIGHT_TEXT)
    c.setFont('MicroHei', 10)
    c.drawCentredString(PAGE_WIDTH/2, 60, '四时之味 · 十五位山客')

def draw_brand_intro_page(c):
    """品牌序页 - 宣纸白底"""
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    
    # 左侧装饰竖线
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(60, PAGE_HEIGHT - 100, 60, 100)
    
    # 竖排文字（模拟）
    c.setFillColor(DARK_TEXT)
    c.setFont('ZenHei', 18)
    
    lines = [
        "南山有四季，四季有十二客。",
        "每一位山客，都是一盏茶的故事。",
        "政和山间，雾起雾落，",
        "茶人守着老手艺，",
        "等一片叶子慢慢变老。",
        "",
        "这帖，写给山，",
        "写给茶，写给品茶的人。"
    ]
    
    y = PAGE_HEIGHT - 130
    for line in lines:
        c.drawString(90, y, line)
        y -= 45
        if y < 200:
            break
    
    # 右上角方印
    draw_seal(c, PAGE_WIDTH - 80, PAGE_HEIGHT - 110, 35)

def draw_season_overview(c, products, title="", start_y=None):
    """绘制四季山客概览页"""
    if start_y:
        y = start_y
    else:
        y = PAGE_HEIGHT - 80
    
    # 标题
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 24)
    c.drawCentredString(PAGE_WIDTH/2, y, title)
    y -= 50
    
    # 分两列展示山客
    col1_x = 100
    col2_x = PAGE_WIDTH/2 + 50
    
    for i, p in enumerate(products):
        col_x = col1_x if i % 2 == 0 else col2_x
        if i % 2 == 0 and i > 0:
            y -= 140
        
        # 山客名
        c.setFillColor(DARK_TEXT)
        c.setFont('ZenHei', 16)
        c.drawString(col_x, y, p["name"])
        
        # 茶名
        c.setFillColor(LIGHT_TEXT)
        c.setFont('MicroHei', 11)
        c.drawString(col_x, y - 25, p["teaName"])
        
        # 季节标签
        c.setFillColor(GOLD)
        c.setFont('MicroHei', 9)
        c.drawString(col_x, y - 45, f"「{p['season']}」")
        
        y -= 70

def draw_product_detail_page(c, product):
    """山客详情页"""
    # 背景
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    
    # 获取山客形象路径
    portrait_path = get_portrait_path(product["name"])
    
    # 左侧山客形象（约50%宽度）
    if portrait_path:
        portrait_temp = compress_image(portrait_path, max_width=320)
        if portrait_temp and os.path.exists(portrait_temp):
            img = Image.open(portrait_temp)
            img_width, img_height = img.size
            # 保持宽高比放置
            display_height = PAGE_HEIGHT - 100
            display_width = img_width * (display_height / img_height)
            if display_width > PAGE_WIDTH * 0.45:
                display_width = PAGE_WIDTH * 0.45
                display_height = img_height * (display_width / img_width)
            
            c.drawImage(portrait_temp, 40, 50, width=display_width, height=display_height, preserveAspectRatio=True)
    
    # 右侧内容区
    right_x = PAGE_WIDTH * 0.52
    
    # 山客名（大字金色）
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 36)
    c.drawString(right_x, PAGE_HEIGHT - 80, product["name"])
    
    # 茶品名
    c.setFillColor(DARK_TEXT)
    c.setFont('MicroHei', 14)
    c.drawString(right_x, PAGE_HEIGHT - 115, product["teaName"])
    
    # 季节标签
    c.setFillColor(LIGHT_TEXT)
    c.setFont('MicroHei', 11)
    c.drawString(right_x + 120, PAGE_HEIGHT - 115, f"· {product['season']} ·")
    
    # 分隔线
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(right_x, PAGE_HEIGHT - 135, right_x + 200, PAGE_HEIGHT - 135)
    
    # 故事
    y = PAGE_HEIGHT - 170
    c.setFillColor(DARK_TEXT)
    c.setFont('MicroHei', 11)
    
    story_lines = product["story"]
    # 自动换行
    max_chars = 28
    for line in [story_lines[i:i+max_chars] for i in range(0, len(story_lines), max_chars)]:
        if y < 200:
            break
        c.drawString(right_x, y, line)
        y -= 22
    
    y -= 20
    
    # 风味笔记
    c.setFillColor(LIGHT_TEXT)
    c.setFont('MicroHei', 9)
    c.drawString(right_x, y, "风味笔记")
    y -= 20
    
    c.setFillColor(DARK_TEXT)
    c.setFont('MicroHei', 10)
    flavor_lines = [product["flavor"][i:i+32] for i in range(0, min(len(product["flavor"]), 80), 32)]
    for line in flavor_lines:
        c.drawString(right_x, y, line)
        y -= 18
    
    y -= 15
    
    # 收藏价值
    c.setFillColor(LIGHT_TEXT)
    c.setFont('MicroHei', 9)
    c.drawString(right_x, y, "收藏价值")
    y -= 20
    
    c.setFillColor(GOLD)
    c.setFont('MicroHei', 10)
    value_lines = [product["value"][i:i+32] for i in range(0, min(len(product["value"]), 80), 32)]
    for line in value_lines:
        c.drawString(right_x, y, line)
        y -= 18
    
    # 右下角方印
    draw_seal(c, PAGE_WIDTH - 70, 60, 30)

def draw_signature_samples(c):
    """签文样例页"""
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    
    # 标题
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 28)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 80, '签文 · 摘选')
    
    # 装饰线
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(PAGE_WIDTH/2 - 60, PAGE_HEIGHT - 95, PAGE_WIDTH/2 + 60, PAGE_HEIGHT - 95)
    
    # 签文样例
    signatures = [
        ("童濛签", "溪声便是广长舌，山色无非清净身", "今日适合放下思虑，以童心观世界。"),
        ("步止签", "行到水穷处，坐看云起时", "大吉之日！适合停下脚步，审视方向。"),
        ("天香签", "天生我材必有用，千金散尽还复来", "大吉之日！王者之气，势不可挡。"),
    ]
    
    y = PAGE_HEIGHT - 160
    for name, qianyu, inter in signatures:
        # 签名
        c.setFillColor(DARK_TEXT)
        c.setFont('ZenHei', 18)
        c.drawCentredString(PAGE_WIDTH/2, y, name)
        y -= 35
        
        # 签语
        c.setFillColor(GOLD)
        c.setFont('ZenHei', 14)
        c.drawCentredString(PAGE_WIDTH/2, y, qianyu)
        y -= 30
        
        # 解签
        c.setFillColor(LIGHT_TEXT)
        c.setFont('MicroHei', 10)
        c.drawCentredString(PAGE_WIDTH/2, y, inter)
        y -= 60
        
        # 分隔线
        if name != signatures[-1][0]:
            c.setStrokeColor(HexColor('#E8E0D0'))
            c.line(100, y + 20, PAGE_WIDTH - 100, y + 20)
            y -= 20
    
    # 右下角方印
    draw_seal(c, PAGE_WIDTH - 80, 60, 35)

def draw_brand_philosophy(c):
    """品牌理念页"""
    c.setFillColor(BLACK_BG)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    
    # 主标语
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 48)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 80, '你')
    
    c.setFont('ZenHei', 32)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 30, '是第十三位')
    
    # 装饰线
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(PAGE_WIDTH/2 - 100, PAGE_HEIGHT/2, PAGE_WIDTH/2 + 100, PAGE_HEIGHT/2)
    
    # 副标语
    c.setFillColor(LIGHT_TEXT)
    c.setFont('MicroHei', 14)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 50, '南山有四季，四季有十二客')
    
    # 底部说明
    c.setFont('MicroHei', 11)
    c.drawCentredString(PAGE_WIDTH/2, 120, '每一位品茶的你，都是独一无二的山客')

def draw_contact_page(c):
    """联系方式页"""
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    
    # 标题
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 28)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 100, '扫码 · 遇见你的山客')
    
    # 装饰线
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(PAGE_WIDTH/2 - 80, PAGE_HEIGHT - 120, PAGE_WIDTH/2 + 80, PAGE_HEIGHT - 120)
    
    # 微信二维码
    qr_path = get_qr_path()
    if qr_path:
        qr_temp = compress_image(qr_path, max_width=180, quality=85)
        if qr_temp:
            c.drawImage(qr_temp, PAGE_WIDTH/2 - 90, PAGE_HEIGHT/2 - 100, width=180, height=180, preserveAspectRatio=True)
    
    # 底部
    c.setFillColor(DARK_TEXT)
    c.setFont('ZenHei', 14)
    c.drawCentredString(PAGE_WIDTH/2, 150, '南山帖')
    
    c.setFillColor(LIGHT_TEXT)
    c.setFont('MicroHei', 10)
    c.drawCentredString(PAGE_WIDTH/2, 120, '政和 · 白茶')
    c.drawCentredString(PAGE_WIDTH/2, 100, '四时之味 · 十五位山客')

def create_brand_pdf():
    """生成品牌手册PDF"""
    output_path = os.path.join(SCRIPT_DIR, "南山帖_品牌手册.pdf")
    c = canvas.Canvas(output_path, pagesize=A4)
    
    # 1. 封面
    draw_cover_page(c)
    c.showPage()
    
    # 2. 品牌序
    draw_brand_intro_page(c)
    c.showPage()
    
    # 3. 四季总览 - 春·夏
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 28)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 80, '春 · 夏')
    draw_season_overview(c, SPRING + SUMMER)
    draw_seal(c, PAGE_WIDTH - 80, 60, 35)
    c.showPage()
    
    # 4. 四季总览 - 秋·冬
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 28)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 80, '秋 · 冬')
    draw_season_overview(c, AUTUMN + WINTER)
    draw_seal(c, PAGE_WIDTH - 80, 60, 35)
    c.showPage()
    
    # 5. 四时与传说
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 28)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 80, '四时 · 传说')
    draw_season_overview(c, FOUR_SEASONS + LEGEND)
    draw_seal(c, PAGE_WIDTH - 80, 60, 35)
    c.showPage()
    
    # 6-20. 15位山客详情
    for product in PRODUCTS:
        draw_product_detail_page(c, product)
        c.showPage()
    
    # 21. 签文样例
    draw_signature_samples(c)
    c.showPage()
    
    # 22. 品牌理念
    draw_brand_philosophy(c)
    c.showPage()
    
    # 23. 联系方式
    draw_contact_page(c)
    c.showPage()
    
    c.save()
    print(f"品牌手册已生成: {output_path}")
    
    # 清理临时文件
    for f in _temp_files:
        try:
            if os.path.exists(f):
                os.remove(f)
        except:
            pass
    
    return output_path

if __name__ == "__main__":
    create_brand_pdf()
