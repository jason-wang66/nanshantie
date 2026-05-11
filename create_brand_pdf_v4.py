# -*- coding: utf-8 -*-
"""
南山帖品牌手册PDF生成脚本 v4
改进：采用上下布局，图片在上，文字在下
"""

import os
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

# 颜色定义
BLACK_BG = HexColor('#1A1A1A')
GOLD = HexColor('#D4B68A')
PAPER_WHITE = HexColor('#F5F0E6')
VERMILION = HexColor('#C23B22')
DARK_TEXT = HexColor('#333333')
LIGHT_TEXT = HexColor('#8B7355')
ANNOTATION_GRAY = HexColor('#8B7355')

# 字体
FONT_ZEN = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
FONT_MICRO = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

pdfmetrics.registerFont(TTFont('ZenHei', FONT_ZEN))
pdfmetrics.registerFont(TTFont('MicroHei', FONT_MICRO))

PAGE_WIDTH, PAGE_HEIGHT = A4

def get_portrait_path(name):
    paths = [
        os.path.join(BASE_DIR, "白茶品牌", "山客形象", f"{name}.jpg"),
        os.path.join(BASE_DIR, "山客形象", f"{name}.jpg"),
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def get_qr_path():
    paths = [
        os.path.join(BASE_DIR, "用户上传", "photo-1777830978310.jpg"),
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

PRODUCTS = [
    {"name": "童濛", "teaName": "白毫银针", "season": "春",
     "story": "春山初醒，晨雾未散。露水从叶尖滑落，跌进泥土里，发出极轻的声响。有个孩子赤脚走过山径，衣襟上沾着青草的汁液，眼睛像刚洗过的天空。他看什么都新鲜，看什么都欢喜。山雀掠过，他仰头；野花绽放，他俯身。他叫童濛——是万物初生时的模样，是天地间第一缕干净的呼吸。",
     "flavor": "毫香清幽，如春日晨露。入口鲜甜，回甘绵长，带有淡淡的花香。",
     "value": "政和核心产区，明前头采，芽头肥壮，白毫密披，极具收藏价值。"},
    {"name": "浮岚", "teaName": "福建高山绿茶", "season": "春",
     "story": "午后，山谷里起了雾。不是浓得化不开的那种，而是轻薄的，游走的，像是山在呼吸。雾从溪面升起，绕过松林，在半山腰停住。有个少年站在雾里，衣袂被风轻轻吹起，看不清面容，只觉得他整个人都像是从云中长出来的。他叫浮岚——是山与天的交界，是看得见却握不住的轻盈。",
     "flavor": "清香淡雅，如山间雾气。入口鲜爽，带有淡淡的豆香与板栗香。",
     "value": "政和星溪乡海拔1200米高山茶园，云雾缭绕，品质优异。"},
    {"name": "不器", "teaName": "白牡丹", "season": "夏",
     "story": "夏日漫长，蝉声如织。树荫下坐着一个人，他面前摆着粗陶碗，碗里盛着清水。有人来问路，他指；有人来借火，他给；有人来闲谈，他听。他不拒绝任何人，也不强留任何人。他的性子温和，不偏不倚，像是山间的风，吹过就算了。他叫不器——君子不器，他什么都是，也什么都不是。",
     "flavor": "花香馥郁，如夏日晚风。入口甘甜，有茉莉与兰花的复合香气。",
     "value": "政和白茶核心产区，一芽一二叶标准采摘，品质上乘。"},
    {"name": "丹桂", "teaName": "桂花红茶", "season": "秋",
     "story": "入秋之前，院子里那棵桂树先开了花。不是满树金黄，只是疏疏几簇，香气却已经藏不住了。有个女子在树下铺了竹匾，将落花拢在一起。她动作很轻，怕惊扰了那些细小的花瓣。她叫丹桂——不是秋天的全部，却是秋天最让人惦记的那一部分。",
     "flavor": "桂香浓郁，如金秋时节。入口甜润，桂花的香与红茶的醇完美融合。",
     "value": "政和高山茶园，桂花与红茶窨制而成，秋日限定。"},
    {"name": "桂兰", "teaName": "肉桂", "season": "秋",
     "story": "秋天深了，山里的桂树与兰草同开。桂是浓的，香得热烈，隔着几道弯都能闻见；兰是淡的，清清冷冷，不走近便不知道。有个人，她身上既有桂的冲，又有兰的静。她走路带风，说话却轻；她性子烈，却从不伤人。山里人都说，她像一壶滚水冲下去的肉桂——初闻凌厉，再品回甘。她叫桂兰，是秋天最复杂的那一口。",
     "flavor": "桂皮辛香，如秋山深处。入口醇厚，岩韵显赫，辛辣中带花果香，回甘持久。",
     "value": "政和高山岩茶产区，肉桂品种，岩骨花香，越品越有层次。"},
    {"name": "听枞", "teaName": "老枞", "season": "秋",
     "story": "深山里有棵老枞，树龄已不可考。他常坐在树下，听风穿过枝叶的声音。风来时，树叶沙沙响，像是在说些什么。他听了几十年，从少年听到白头，终于听懂了——原来风什么也没说，是他自己心里有话。他养了条边牧，取名风声。风声风声，风过留声，人过留名。",
     "flavor": "枞韵幽深，如老林古道。入口醇厚，有苔藓味与粽叶香，回甘绵长。",
     "value": "政和高山老枞茶树，树龄逾百年，枞韵独特，极具品鉴价值。"},
    {"name": "天香", "teaName": "大红袍", "season": "秋",
     "story": "他不是茶人，但他爱茶。他不懂制茶，但他懂品茶。他住在山间一处僻静院落，院中植兰养桂，墙上挂着一幅「天香」的匾额。有人问天香是什么意思，他说天香就是天上的香气，不是人间能有的。有人再问，那你为什么喜欢，他说，因为人间太苦，需要一点天上的味道。他养了条罗威纳，取名王者。王者王者，王者风范，不怒自威。",
     "flavor": "岩骨花香，如深山幽谷。入口醇厚，岩韵显赫，香气馥郁有层次。",
     "value": "政和岩茶核心产区，大红袍品种，岩骨花香，品质上乘。"},
    {"name": "履霜", "teaName": "工夫红茶", "season": "冬",
     "story": "第一场霜落下来的时候，她来了。她穿着素色的衣裳，走路很轻，踩在霜叶上，发出细微的碎裂声。她带来一篮火红的果子，说是山里采的。屋里生了炭火，她坐在火边，影子被拉得很长。有人递给她一杯热水，她捧在手里，却没有喝，只是看着热气慢慢升起来。她叫履霜——是踩在冬天边缘的人，也是带来温暖的人。",
     "flavor": "醇厚甘甜，如冬日暖阳。入口绵柔，有蜜香与薯香，回甘持久。",
     "value": "政和工夫红茶工艺，冬季采摘，内质丰富，越存越醇。"},
    {"name": "漱雪", "teaName": "茉莉绿茶", "season": "冬",
     "story": "大雪封山之后，另一个女子出现了。她喜欢在雪地里走，留下一串浅浅的脚印。她走到梅树下，仰头看枝头的积雪。风吹过，雪落了她一身，她也不拂，只是站在那里，像是自己也成了一株梅。她叫漱雪——南方有雪不易。",
     "flavor": "茉莉清香，如雪后初晴。入口鲜灵，有茉莉花的清雅与绿茶的鲜爽。",
     "value": "福建茉莉花茶传统窨制工艺，七窨一提，花香入骨。"},
    {"name": "漱月", "teaName": "茉莉红茶", "season": "冬",
     "story": "月圆那夜，有人在溪边掬水。水里有月亮的倒影，她掬起来，月亮就碎了；再掬，又圆了。她一遍一遍地掬，像是在玩一个永远不会腻的游戏。她的影子落在水面上，和月亮混在一起，分不清哪个是她，哪个是月。她叫漱月——是用溪水洗月亮的人。",
     "flavor": "花香与茶香交融，如月光如水。入口甜润，茉莉的清与红茶的醇相得益彰。",
     "value": "福建茉莉花与红茶的完美结合，创新工艺，限量发售。"},
    {"name": "莫离", "teaName": "茉莉银针", "season": "四时",
     "story": "这些人来来去去，但总有一个人一直在。她住在山脚下那间小屋，屋前种着茉莉。花开的时候，满院子都是白的。她采花，晾花，然后把花收进瓷罐里，一层一层地铺好。有人问她为什么总是不离开，她指了指那罐花，又指了指自己。她叫莫离——花与人，都不分离。",
     "flavor": "茉莉银针，如始终如一的守候。入口甘甜，花香持久，回味悠长。",
     "value": "福建茉莉花茶巅峰之作，银针为骨，茉莉为魂，四时皆宜。"},
    {"name": "半见", "teaName": "陈皮白茶", "season": "四时",
     "story": "她喜欢躲在帘子后面，看外面的人来人往。不是害羞，而是觉得，保持一点距离刚刚好。太近了会腻，太远了会淡。她叫自己半见——半藏半显，半开半合。她养了条法斗，取名若隐。若隐若隐，若有若无，是她喜欢的状态，也是她与这个世界相处的方式。",
     "flavor": "陈皮与白茶交融，如光阴流转。入口甜润，有陈皮的果香与白茶的甘醇。",
     "value": "政和白茶与新会陈皮结合，创新工艺，跨界搭配，风味独特。"},
    {"name": "步止", "teaName": "白茶饼", "season": "传说",
     "story": "他走了很远很远的路，终于在这座山前停下来。不是走不动了，而是觉得，这里就是他要找的地方。他没有名字，来时无名，去时也无名。偶尔有人问他从哪里来，他只是指一指身后的云。有人问他叫什么，他说叫步止——不是止步不前，而是知道该在哪里停下来。他养了一条德国牧羊犬，取名守望。守望守望，守在这里，等那些走累了的旅人。",
     "flavor": "醇厚甘甜，如秋日暖阳。入口绵柔，有枣香与药香，回甘悠长。",
     "value": "政和白茶核心产区，陈化多年，滋味醇厚，具收藏价值。"},
    {"name": "无羁", "teaName": "17年白茶饼", "season": "传说",
     "story": "他骑马走过很多地方，见识过很多风景，但他从不在任何一个地方停留太久。不是无情，而是怕情深。他觉得自己像一阵风，吹过就算了，不该留下什么。但有一年，他来到南山，遇到一条灵缇。灵缇追上了他，用鼻子蹭了蹭他的手背。他停了下来，这一停，就是很多年。他给灵缇取名无拘——无拘无束，随遇而安。无拘跟着他，他也跟着无拘。",
     "flavor": "陈香幽远，如岁月沉淀。入口甘醇，有枣香与药香，陈韵悠长。",
     "value": "政和白茶，2017年陈化至今，七年老茶，滋味醇厚，极具收藏价值。"},
    {"name": "南山", "teaName": "马年茶饼", "season": "传说",
     "story": "这座山没有名字，山里的人就叫它南山。后来，有个孩子出生在山下，属马那年家里做了批茶饼，有人问这茶叫什么，他说叫马年茶。后来这孩子长大了，成了山里的守护者。人们不知道他的名字，只叫他南山——山不需要名字，山就是山。他养了条藏獒，取名厚重。厚重厚重，沉稳厚重，是山的气质，也是他的。",
     "flavor": "沉稳厚实，如南山之重。入口绵长，有陈香与木质香，回甘悠远。",
     "value": "政和白茶，2012年马年茶饼，陈化十余年，滋味醇厚，收藏珍品。"},
]

SIGNATURES = [
    {"name": "童濛签", "text": "溪声便是广长舌，山色无非清净身"},
    {"name": "步止签", "text": "行到水穷处，坐看云起时"},
    {"name": "天香签", "text": "人间太苦，需要一点天上的味道"},
    {"name": "漱雪签", "text": "南方有雪不易"},
    {"name": "无羁签", "text": "风过就算了，但这一停，就是很多年"},
    {"name": "南山签", "text": "山不需要名字，山就是山"},
]

_temp_files = []

def compress_image(image_path, max_width=400, quality=80):
    if not image_path or not os.path.exists(image_path):
        return None
    try:
        img = Image.open(image_path)
        ratio = max_width / img.width if img.width > max_width else 1
        if ratio < 1:
            img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
        img = img.convert('RGB')
        temp_path = os.path.join(tempfile.gettempdir(), f"pdf_{hash(image_path)}.jpg")
        img.save(temp_path, 'JPEG', quality=quality)
        _temp_files.append(temp_path)
        return temp_path
    except Exception as e:
        print(f"图片处理失败: {e}")
        return None

def draw_seal(c, x, y, size=30):
    c.setStrokeColor(VERMILION)
    c.setFillColor(VERMILION)
    c.setLineWidth(1.5)
    c.rect(x, y, size, size, fill=0, stroke=1)
    c.setFont('ZenHei', size * 0.4)
    c.drawString(x + 5, y + 10, '南')

def draw_cover(c):
    c.setFillColor(BLACK_BG)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 88)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 30, '南山帖')
    c.setFont('MicroHei', 36)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 50, '政和 · 白茶')
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(PAGE_WIDTH/2 - 100, PAGE_HEIGHT/2 - 80, PAGE_WIDTH/2 + 100, PAGE_HEIGHT/2 - 80)
    c.setFont('MicroHei', 24)
    c.drawCentredString(PAGE_WIDTH/2, 80, '四季十二客 · 三传说')
    draw_seal(c, PAGE_WIDTH - 70, 50, 40)

def draw_brand_intro(c):
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(60, PAGE_HEIGHT - 80, 60, 80)
    draw_seal(c, PAGE_WIDTH - 90, PAGE_HEIGHT - 120, 45)
    c.setFillColor(DARK_TEXT)
    c.setFont('ZenHei', 22)
    lines = ["南山有四季，四季有十二客。", "每一位山客，都是一盏茶的故事。", "",
             "政和山间，雾起雾落，", "茶人守着老手艺，", "等一片叶子慢慢变老。", "",
             "这帖，写给山，", "写给茶，写给品茶的人。"]
    y = PAGE_HEIGHT - 150
    for line in lines:
        if line:
            c.drawString(90, y, line)
        y -= 50
    draw_seal(c, PAGE_WIDTH - 70, 50, 35)

def draw_season_overview(c, title, products):
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 32)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 80, title)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(PAGE_WIDTH/2 - 60, PAGE_HEIGHT - 100, PAGE_WIDTH/2 + 60, PAGE_HEIGHT - 100)
    y = PAGE_HEIGHT - 170
    col1_x, col2_x = 100, PAGE_WIDTH/2 + 50
    for i, p in enumerate(products):
        col_x = col1_x if i < len(products)/2 else col2_x
        if i == len(products)//2:
            y = PAGE_HEIGHT - 170
        c.setFillColor(DARK_TEXT)
        c.setFont('ZenHei', 20)
        c.drawString(col_x, y, p["name"])
        c.setFillColor(LIGHT_TEXT)
        c.setFont('MicroHei', 14)
        c.drawString(col_x, y - 30, p["teaName"])
        c.setFillColor(GOLD)
        c.setFont('MicroHei', 12)
        c.drawString(col_x, y - 55, f"「{p['season']}」")
        y -= 100
    draw_seal(c, PAGE_WIDTH - 70, 50, 35)

def draw_four_legend(c):
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 32)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 80, '四时 · 传说')
    c.setStrokeColor(GOLD)
    c.line(PAGE_WIDTH/2 - 60, PAGE_HEIGHT - 100, PAGE_WIDTH/2 + 60, PAGE_HEIGHT - 100)
    four_seasons = [p for p in PRODUCTS if p["season"] == "四时"]
    legend = [p for p in PRODUCTS if p["season"] == "传说"]
    y = PAGE_HEIGHT - 170
    c.setFillColor(ANNOTATION_GRAY)
    c.setFont('MicroHei', 12)
    c.drawString(100, y, '—— 四时 ——')
    y -= 40
    for p in four_seasons:
        c.setFillColor(DARK_TEXT)
        c.setFont('ZenHei', 18)
        c.drawString(100, y, p["name"])
        c.setFillColor(LIGHT_TEXT)
        c.setFont('MicroHei', 13)
        c.drawString(170, y, p["teaName"])
        c.setFillColor(GOLD)
        c.setFont('MicroHei', 11)
        c.drawString(320, y, f"「{p['season']}」")
        y -= 40
    y -= 30
    c.setFillColor(ANNOTATION_GRAY)
    c.setFont('MicroHei', 12)
    c.drawString(100, y, '—— 传说 ——')
    y -= 40
    for p in legend:
        c.setFillColor(DARK_TEXT)
        c.setFont('ZenHei', 18)
        c.drawString(100, y, p["name"])
        c.setFillColor(LIGHT_TEXT)
        c.setFont('MicroHei', 13)
        c.drawString(170, y, p["teaName"])
        c.setFillColor(GOLD)
        c.setFont('MicroHei', 11)
        c.drawString(320, y, f"「{p['season']}」")
        y -= 40
    draw_seal(c, PAGE_WIDTH - 70, 50, 35)

def draw_product_detail(c, product):
    """山客详情页 - 改进：全宽布局，图片和文字区域分离"""
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    
    # 右上角装饰
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 22)
    c.drawRightString(PAGE_WIDTH - 55, PAGE_HEIGHT - 40, product["name"])
    draw_seal(c, PAGE_WIDTH - 95, PAGE_HEIGHT - 70, 26)
    
    # 左侧山客形象 - 约占页面50%宽度
    portrait_path = get_portrait_path(product["name"])
    if portrait_path:
        portrait_temp = compress_image(portrait_path, max_width=280, quality=80)
        if portrait_temp and os.path.exists(portrait_temp):
            img = Image.open(portrait_temp)
            img_w, img_h = img.size
            # 图片高度为页面高度的一半
            display_height = (PAGE_HEIGHT - 100) / 2
            display_width = img_w * (display_height / img_h)
            if display_width > PAGE_WIDTH * 0.45:
                display_width = PAGE_WIDTH * 0.45
                display_height = img_h * (display_width / img_w)
            c.drawImage(portrait_temp, 40, PAGE_HEIGHT - 100 - display_height, 
                       width=display_width, height=display_height, preserveAspectRatio=True)
    
    # 右侧内容区 - 从中间位置开始，使用全宽
    right_x = PAGE_WIDTH / 2 + 20
    content_top = PAGE_HEIGHT - 50
    
    # 茶品名 + 季节
    c.setFillColor(DARK_TEXT)
    c.setFont('MicroHei', 14)
    c.drawString(right_x, content_top, product["teaName"])
    c.setFillColor(GOLD)
    c.setFont('MicroHei', 12)
    c.drawString(right_x + 110, content_top, f"· {product['season']} ·")
    
    # 分隔线
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(right_x, content_top - 18, PAGE_WIDTH - 40, content_top - 18)
    
    # 故事 - 从右上方开始，向下延伸
    y = content_top - 45
    c.setFillColor(DARK_TEXT)
    c.setFont('MicroHei', 10.5)
    
    story = product["story"]
    # 使用更小的字号和每行更多字符
    max_chars = 34
    story_lines = [story[i:i+max_chars] for i in range(0, len(story), max_chars)]
    
    for line in story_lines:
        if y < PAGE_HEIGHT / 2:
            break
        c.drawString(right_x, y, line)
        y -= 18
    
    y -= 15
    
    # 风味笔记
    c.setFillColor(ANNOTATION_GRAY)
    c.setFont('MicroHei', 10)
    c.drawString(right_x, y, "风味笔记")
    y -= 18
    
    c.setFillColor(DARK_TEXT)
    c.setFont('MicroHei', 10)
    flavor_lines = [product["flavor"][i:i+36] for i in range(0, len(product["flavor"]), 36)]
    for line in flavor_lines:
        c.drawString(right_x, y, line)
        y -= 15
    
    y -= 10
    
    # 收藏价值
    c.setFillColor(ANNOTATION_GRAY)
    c.setFont('MicroHei', 10)
    c.drawString(right_x, y, "收藏价值")
    y -= 18
    
    c.setFillColor(GOLD)
    c.setFont('MicroHei', 10)
    value_lines = [product["value"][i:i+36] for i in range(0, len(product["value"]), 36)]
    for line in value_lines:
        c.drawString(right_x, y, line)
        y -= 15
    
    # 故事延续区域 - 页面下半部分左侧
    y_bottom = PAGE_HEIGHT / 2 - 30
    story_continued = False
    for line in story_lines:
        if y < PAGE_HEIGHT / 2 - 10:
            story_continued = True
            break
    
    # 如果故事太长，在下方继续显示
    if len(story_lines) > 14:  # 大约需要延续
        y_cont = PAGE_HEIGHT / 2 - 30
        c.setFillColor(DARK_TEXT)
        c.setFont('MicroHei', 10.5)
        # 从第15行开始继续
        for i, line in enumerate(story_lines[14:], start=14):
            if y_cont < 80:
                break
            c.drawString(50, y_cont, line)
            y_cont -= 18
    
    # 右下角朱红方印
    draw_seal(c, PAGE_WIDTH - 65, 35, 28)

def draw_signatures(c):
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 32)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 80, '签文 · 摘选')
    c.setStrokeColor(GOLD)
    c.line(PAGE_WIDTH/2 - 60, PAGE_HEIGHT - 100, PAGE_WIDTH/2 + 60, PAGE_HEIGHT - 100)
    y = PAGE_HEIGHT - 160
    for i, sig in enumerate(SIGNATURES):
        c.setFillColor(ANNOTATION_GRAY)
        c.setFont('MicroHei', 12)
        c.drawCentredString(PAGE_WIDTH/2, y, sig["name"])
        y -= 35
        c.setFillColor(GOLD)
        c.setFont('ZenHei', 18)
        c.drawCentredString(PAGE_WIDTH/2, y, sig["text"])
        y -= 70
        if i < len(SIGNATURES) - 1:
            c.setStrokeColor(HexColor('#E8E0D0'))
            c.line(150, y + 20, PAGE_WIDTH - 150, y + 20)
    draw_seal(c, PAGE_WIDTH - 70, 50, 35)

def draw_philosophy(c):
    c.setFillColor(BLACK_BG)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 88)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 60, '你')
    c.setFont('ZenHei', 52)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2, '是第十三位')
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(PAGE_WIDTH/2 - 120, PAGE_HEIGHT/2 - 40, PAGE_WIDTH/2 + 120, PAGE_HEIGHT/2 - 40)
    c.setFont('MicroHei', 24)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 90, '四季十二客，山间已至')
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 130, '三位传说，等你结缘')
    c.setFont('MicroHei', 16)
    c.drawCentredString(PAGE_WIDTH/2, 80, '每一位品茶的你，都是独一无二的山客')

def draw_contact(c):
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
    c.setFillColor(GOLD)
    c.setFont('ZenHei', 32)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 80, '扫码 · 遇见你的山客')
    c.setStrokeColor(GOLD)
    c.line(PAGE_WIDTH/2 - 80, PAGE_HEIGHT - 100, PAGE_WIDTH/2 + 80, PAGE_HEIGHT - 100)
    
    # 微信二维码 - 放大到260x260
    qr_path = get_qr_path()
    if qr_path:
        qr_temp = compress_image(qr_path, max_width=350, quality=90)
        if qr_temp:
            qr_size = 260
            qr_x = (PAGE_WIDTH - qr_size) / 2
            qr_y = PAGE_HEIGHT/2 - qr_size/2 + 30
            c.drawImage(qr_temp, qr_x, qr_y, width=qr_size, height=qr_size, preserveAspectRatio=False)
    
    c.setFillColor(DARK_TEXT)
    c.setFont('ZenHei', 18)
    c.drawCentredString(PAGE_WIDTH/2, 150, '南山帖')
    c.setFillColor(LIGHT_TEXT)
    c.setFont('MicroHei', 14)
    c.drawCentredString(PAGE_WIDTH/2, 120, '政和 · 白茶')
    c.drawCentredString(PAGE_WIDTH/2, 95, '四季十二客 · 三传说')
    draw_seal(c, PAGE_WIDTH - 70, 50, 35)

def create_brand_pdf():
    output_path = os.path.join(SCRIPT_DIR, "南山帖_品牌手册.pdf")
    c = canvas.Canvas(output_path, pagesize=A4)
    
    # 1. 封面
    draw_cover(c)
    c.showPage()
    
    # 2. 品牌序
    draw_brand_intro(c)
    c.showPage()
    
    # 3. 四季总览 - 春·夏
    draw_season_overview(c, '春 · 夏', [p for p in PRODUCTS if p["season"] in ["春", "夏"]])
    c.showPage()
    
    # 4. 四季总览 - 秋·冬
    draw_season_overview(c, '秋 · 冬', [p for p in PRODUCTS if p["season"] in ["秋", "冬"]])
    c.showPage()
    
    # 5. 四时·传说
    draw_four_legend(c)
    c.showPage()
    
    # 6-20. 15位山客详情
    for product in PRODUCTS:
        draw_product_detail(c, product)
        c.showPage()
    
    # 21. 签文摘选
    draw_signatures(c)
    c.showPage()
    
    # 22. 品牌理念
    draw_philosophy(c)
    c.showPage()
    
    # 23. 联系方式
    draw_contact(c)
    c.showPage()
    
    c.save()
    print(f"品牌手册已生成: {output_path}")
    
    for f in _temp_files:
        try:
            if os.path.exists(f):
                os.remove(f)
        except:
            pass
    
    return output_path

if __name__ == "__main__":
    create_brand_pdf()
