#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
南山帖品牌手册PDF - 第三版（大幅升级排版）
"""

import os

# 获取当前脚本所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

# 切换到父目录作为工作目录
os.chdir(PARENT_DIR)
print(f"工作目录: {os.getcwd()}")

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Image as RLImage
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ==================== 配置 ====================
OUTPUT_PATH = "./白茶品牌/南山帖_品牌手册.pdf"
PREVIEW_DIR = "./白茶品牌/preview/brand_manual_v3"

# 颜色定义
WARM_GOLD = HexColor('#D4B68A')
PAPER_WHITE = HexColor('#F5F0E6')
VERMILLION = HexColor('#C23B22')
DEEP_BLACK = HexColor('#1A1A1A')
TEXT_GRAY = HexColor('#333333')
ANNOTATION_GRAY = HexColor('#8B7355')

# 字体配置
FONT_TITLE = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
FONT_BODY = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'

# 页面尺寸
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 15 * mm

# ==================== 产品数据 ====================
PRODUCTS = [
    {
        "name": "童濛", "tea_name": "白毫银针", "season": "春",
        "product_img": "./用户上传/IMG_9754_1777874506741_pdtf.jpg",
        "ink_img": "./白茶品牌/山客形象/童濛.jpg",
        "story": "春山初醒，晨雾未散。露水从叶尖滑落，跌进泥土里，发出极轻的声响。有个孩子赤脚走过山径，衣襟上沾着青草的汁液，眼睛像刚洗过的天空。他看什么都新鲜，看什么都欢喜。山雀掠过，他仰头；野花绽放，他俯身。他叫童濛——是万物初生时的模样，是天地间第一缕干净的呼吸。",
        "flavor": "毫香清幽，如春日晨露。入口鲜甜，回甘绵长，带有淡淡的花香。",
        "value": "政和核心产区，明前头采，芽头肥壮，白毫密披，极具收藏价值。",
        "quote": "「溪声便是广长舌，山色无非清净身」"
    },
    {
        "name": "浮岚", "tea_name": "福建高山绿茶", "season": "春",
        "product_img": "./用户上传/IMG_9762_1777874511572_yuay.jpg",
        "ink_img": "./白茶品牌/山客形象/浮岚.jpg",
        "story": "午后，山谷里起了雾。不是浓得化不开的那种，而是轻薄的，游走的，像是山在呼吸。雾从溪面升起，绕过松林，在半山腰停住。有个少年站在雾里，衣袂被风轻轻吹起，看不清面容，只觉得他整个人都像是从云中长出来的。他叫浮岚——是山与天的交界，是看得见却握不住的轻盈。",
        "flavor": "清香淡雅，如山间雾气。入口鲜爽，带有淡淡的豆香与板栗香。",
        "value": "政和星溪乡海拔1200米高山茶园，云雾缭绕，品质优异。",
        "quote": "「山色空蒙雨亦奇，水光潋滟晴方好」"
    },
    {
        "name": "不器", "tea_name": "白牡丹", "season": "夏",
        "product_img": "./用户上传/IMG_9758_1777874508882_kb42.jpg",
        "ink_img": "./白茶品牌/山客形象/不器.jpg",
        "story": "夏日漫长，蝉声如织。树荫下坐着一个人，他面前摆着粗陶碗，碗里盛着清水。有人来问路，他指；有人来借火，他给；有人来闲谈，他听。他不拒绝任何人，也不强留任何人。他的性子温和，不偏不倚，像是山间的风，吹过就算了。他叫不器——君子不器，他什么都是，也什么都不是。",
        "flavor": "花香馥郁，如夏日晚风。入口甘甜，有茉莉与兰花的复合香气。",
        "value": "政和白茶核心产区，一芽一二叶标准采摘，品质上乘。",
        "quote": "「万物静观皆自得，四时佳兴与人同」"
    },
    {
        "name": "丹桂", "tea_name": "桂花红茶", "season": "秋",
        "product_img": "./用户上传/IMG_9757_1777874508245_33rc.jpg",
        "ink_img": "./白茶品牌/山客形象/丹桂.jpg",
        "story": "入秋之前，院子里那棵桂树先开了花。不是满树金黄，只是疏疏几簇，香气却已经藏不住了。有个女子在树下铺了竹匾，将落花拢在一起。她动作很轻，怕惊扰了那些细小的花瓣。她叫丹桂——不是秋天的全部，却是秋天最让人惦记的那一部分。",
        "flavor": "桂香浓郁，如金秋时节。入口甜润，桂花的香与红茶的醇完美融合。",
        "value": "政和高山茶园，桂花与红茶窨制而成，秋日限定。",
        "quote": "「何当共剪西窗烛，却话巴山夜雨时」"
    },
    {
        "name": "桂兰", "tea_name": "肉桂", "season": "秋",
        "product_img": "./用户上传/photo-1777875455719.jpg",
        "ink_img": "./白茶品牌/山客形象/桂兰.jpg",
        "story": "秋天深了，山里的桂树与兰草同开。桂是浓的，香得热烈，隔着几道弯都能闻见；兰是淡的，清清冷冷，不走近便不知道。有个人，她身上既有桂的冲，又有兰的静。她走路带风，说话却轻；她性子烈，却从不伤人。山里人都说，她像一壶滚水冲下去的肉桂——初闻凌厉，再品回甘。她叫桂兰，是秋天最复杂的那一口。",
        "flavor": "桂皮辛香，如秋山深处。入口醇厚，岩韵显赫，辛辣中带花果香，回甘持久。",
        "value": "政和高山岩茶产区，肉桂品种，岩骨花香，越品越有层次。",
        "quote": "「路遥知马力，日久见人心」"
    },
    {
        "name": "听枞", "tea_name": "老枞", "season": "秋",
        "product_img": "./用户上传/B501B54E-C250-49E1-9B96-123EF9A9F689_1777917106362_yw33.png",
        "ink_img": "./白茶品牌/山客形象/听枞.jpg",
        "story": "深山里有棵老枞，树龄已不可考。他常坐在树下，听风穿过枝叶的声音。风来时，树叶沙沙响，像是在说些什么。他听了几十年，从少年听到白头，终于听懂了——原来风什么也没说，是他自己心里有话。他养了条边牧，取名风声。风声风声，风过留声，人过留名。",
        "flavor": "枞韵幽深，如老林古道。入口醇厚，有苔藓味与粽叶香，回甘绵长。",
        "value": "政和高山老枞茶树，树龄逾百年，枞韵独特，极具品鉴价值。",
        "quote": "「此时无声胜有声，别有幽愁暗恨生」"
    },
    {
        "name": "天香", "tea_name": "大红袍", "season": "秋",
        "product_img": "./用户上传/AEAD773C-7E68-4BDA-B967-3A781EEF9053_1777917106874_rjkq.png",
        "ink_img": "./白茶品牌/山客形象/天香.jpg",
        "story": "他不是茶人，但他爱茶。他不懂制茶，但他懂品茶。他住在山间一处僻静院落，院中植兰养桂，墙上挂着一幅「天香」的匾额。有人问天香是什么意思，他说天香就是天上的香气，不是人间能有的。有人再问，那你为什么喜欢，他说，因为人间太苦，需要一点天上的味道。他养了条罗威纳，取名王者。王者王者，王者风范，不怒自威。",
        "flavor": "岩骨花香，如深山幽谷。入口醇厚，岩韵显赫，香气馥郁有层次。",
        "value": "政和岩茶核心产区，大红袍品种，岩骨花香，品质上乘。",
        "quote": "「天生我材必有用，千金散尽还复来」"
    },
    {
        "name": "履霜", "tea_name": "工夫红茶", "season": "冬",
        "product_img": "./用户上传/IMG_9760_1777874509814_emmf.jpg",
        "ink_img": "./白茶品牌/山客形象/履霜.jpg",
        "story": "第一场霜落下来的时候，她来了。她穿着素色的衣裳，走路很轻，踩在霜叶上，发出细微的碎裂声。她带来一篮火红的果子，说是山里采的。屋里生了炭火，她坐在火边，影子被拉得很长。有人递给她一杯热水，她捧在手里，却没有喝，只是看着热气慢慢升起来。她叫履霜——是踩在冬天边缘的人，也是带来温暖的人。",
        "flavor": "醇厚甘甜，如冬日暖阳。入口绵柔，有蜜香与薯香，回甘持久。",
        "value": "政和工夫红茶工艺，冬季采摘，内质丰富，越存越醇。",
        "quote": "「莫听穿林打叶声，何妨吟啸且徐行」"
    },
    {
        "name": "漱雪", "tea_name": "茉莉绿茶", "season": "冬",
        "product_img": "./用户上传/IMG_9761_1777874510488_knpz.jpg",
        "ink_img": "./白茶品牌/山客形象/漱雪.jpg",
        "story": "大雪封山之后，另一个女子出现了。她喜欢在雪地里走，留下一串浅浅的脚印。她走到梅树下，仰头看枝头的积雪。风吹过，雪落了她一身，她也不拂，只是站在那里，像是自己也成了一株梅。她叫漱雪——南方有雪不易。",
        "flavor": "茉莉清香，如雪后初晴。入口鲜灵，有茉莉花的清雅与绿茶的鲜爽。",
        "value": "福建茉莉花茶传统窨制工艺，七窨一提，花香入骨。",
        "quote": "「此时无声胜有声，别有幽愁暗恨生」"
    },
    {
        "name": "漱月", "tea_name": "茉莉红茶", "season": "冬",
        "product_img": "./用户上传/IMG_9763_1777874512056_mazd.jpg",
        "ink_img": "./白茶品牌/山客形象/漱月.jpg",
        "story": "月圆那夜，有人在溪边掬水。水里有月亮的倒影，她掬起来，月亮就碎了；再掬，又圆了。她一遍一遍地掬，像是在玩一个永远不会腻的游戏。她的影子落在水面上，和月亮混在一起，分不清哪个是她，哪个是月。她叫漱月——是用溪水洗月亮的人。",
        "flavor": "花香与茶香交融，如月光如水。入口甜润，茉莉的清与红茶的醇相得益彰。",
        "value": "福建茉莉花与红茶的完美结合，创新工艺，限量发售。",
        "quote": "「掬水月在手，弄花香满衣」"
    },
    {
        "name": "莫离", "tea_name": "茉莉银针", "season": "四时",
        "product_img": "./用户上传/photo-1777823574781.jpg",
        "ink_img": "./白茶品牌/山客形象/莫离.jpg",
        "story": "这些人来来去去，但总有一个人一直在。她住在山脚下那间小屋，屋前种着茉莉。花开的时候，满院子都是白的。她采花，晾花，然后把花收进瓷罐里，一层一层地铺好。有人问她为什么总是不离开，她指了指那罐花，又指了指自己。她叫莫离——花与人，都不分离。",
        "flavor": "茉莉银针，如始终如一的守候。入口甘甜，花香持久，回味悠长。",
        "value": "福建茉莉花茶巅峰之作，银针为骨，茉莉为魂，四时皆宜。",
        "quote": "「执子之手，与子偕老」"
    },
    {
        "name": "半见", "tea_name": "陈皮白茶", "season": "四时",
        "product_img": "./用户上传/615de78d9c273d421ecee56eaf40a4_1777917466550_6u9o.jpg",
        "ink_img": "./白茶品牌/山客形象/半见.jpg",
        "story": "她喜欢躲在帘子后面，看外面的人来人往。不是害羞，而是觉得，保持一点距离刚刚好。太近了会腻，太远了会淡。她叫自己半见——半藏半显，半开半合。她养了条法斗，取名若隐。若隐若隐，若有若无，是她喜欢的状态，也是她与这个世界相处的方式。",
        "flavor": "陈皮与白茶交融，如光阴流转。入口甜润，有陈皮的果香与白茶的甘醇。",
        "value": "政和白茶与新会陈皮结合，创新工艺，跨界搭配，风味独特。",
        "quote": "「犹抱琵琶半遮面，欲说还休」"
    },
    {
        "name": "步止", "tea_name": "白茶饼", "season": "传说",
        "product_img": "./用户上传/photo-1777917086577.jpg",
        "ink_img": "./白茶品牌/山客形象/步止.jpg",
        "story": "他走了很远很远的路，终于在这座山前停下来。不是走不动了，而是觉得，这里就是他要找的地方。他没有名字，来时无名，去时也无名。偶尔有人问他从哪里来，他只是指一指身后的云。有人问他叫什么，他说叫步止——不是止步不前，而是知道该在哪里停下来。他养了一条德国牧羊犬，取名守望。守望守望，守在这里，等那些走累了的旅人。",
        "flavor": "醇厚甘甜，如秋日暖阳。入口绵柔，有枣香与药香，回甘悠长。",
        "value": "政和白茶核心产区，陈化多年，滋味醇厚，具收藏价值。",
        "quote": "「行到水穷处，坐看云起时」"
    },
    {
        "name": "无羁", "tea_name": "17年白茶饼", "season": "传说",
        "product_img": "./用户上传/208CC47A-4737-4BB1-A9BD-58B908E5C118_1777917237993_vaev.png",
        "ink_img": "./白茶品牌/山客形象/无羁.jpg",
        "story": "他骑马走过很多地方，见识过很多风景，但他从不在任何一个地方停留太久。不是无情，而是怕情深。他觉得自己像一阵风，吹过就算了，不该留下什么。但有一年，他来到南山，遇到一条灵缇。灵缇追上了他，用鼻子蹭了蹭他的手背。他停了下来，这一停，就是很多年。他给灵缇取名无拘——无拘无束，随遇而安。无拘跟着他，他也跟着无拘。",
        "flavor": "陈香幽远，如岁月沉淀。入口甘醇，有枣香与药香，陈韵悠长。",
        "value": "政和白茶，2017年陈化至今，七年老茶，滋味醇厚，极具收藏价值。",
        "quote": "「海阔凭鱼跃，天高任鸟飞」"
    },
    {
        "name": "南山", "tea_name": "马年茶饼", "season": "传说",
        "product_img": "./用户上传/1A926B8E-72CC-4C9D-9769-786BA354FB29_1777917244865_tltf.png",
        "ink_img": "./白茶品牌/山客形象/南山.jpg",
        "story": "这座山没有名字，山里的人就叫它南山。后来，有个孩子出生在山下，属马那年家里做了批茶饼，有人问这茶叫什么，他说叫马年茶。后来这孩子长大了，成了山里的守护者。人们不知道他的名字，只叫他南山——山不需要名字，山就是山。他养了条藏獒，取名厚重。厚重厚重，沉稳厚重，是山的气质，也是他的。",
        "flavor": "沉稳厚实，如南山之重。入口绵长，有陈香与木质香，回甘悠远。",
        "value": "政和白茶，2012年马年茶饼，陈化十余年，滋味醇厚，收藏珍品。",
        "quote": "「山不在高，有仙则名；水不在深，有龙则灵」"
    }
]

# ==================== 工具函数 ====================

def register_fonts():
    """注册中文字体"""
    try:
        pdfmetrics.registerFont(TTFont('WenQuanYiZenHei', FONT_TITLE))
        pdfmetrics.registerFont(TTFont('WenQuanYiMicroHei', FONT_BODY))
        print("字体注册成功")
        return True
    except Exception as e:
        print(f"字体注册失败: {e}")
        return False

def hex_to_rgb(hex_color):
    """将十六进制颜色转换为RGB"""
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def draw_seal(draw, x, y, seal_size=40):
    """绘制朱红方印"""
    vermillion = hex_to_rgb('#C23B22')
    draw.rectangle([x, y, x + seal_size, y + seal_size], 
                   outline=vermillion, width=2)
    
    try:
        font = ImageFont.truetype(FONT_TITLE, int(seal_size * 0.6))
    except:
        font = ImageFont.load_default()
    
    text = "南"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = x + (seal_size - text_w) // 2
    text_y = y + (seal_size - text_h) // 2 - 2
    draw.text((text_x, text_y), text, fill=vermillion, font=font)

def add_title_to_ink_image(ink_path, name, output_path):
    """在水墨图上添加2字书法山客名和方印"""
    try:
        img = Image.open(ink_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        draw = ImageDraw.Draw(img)
        w, h = img.size
        
        try:
            font_large = ImageFont.truetype(FONT_TITLE, int(min(w, h) * 0.12))
        except:
            font_large = ImageFont.load_default()
        
        gold = hex_to_rgb('#D4B68A')
        
        bbox = draw.textbbox((0, 0), name, font=font_large)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = w - text_w - 30
        y = 25
        
        draw.text((x, y), name, fill=gold, font=font_large)
        
        draw_seal(draw, w - 65, h - 65, 50)
        
        img.save(output_path, 'JPEG', quality=75, optimize=True)
        print(f"水墨图处理完成: {output_path}")
        return output_path
    except Exception as e:
        print(f"处理水墨图失败: {e}")
        return ink_path

def add_info_to_product_image(product_path, tea_name, season, output_path):
    """在产品图上添加茶品名、季节和方印"""
    try:
        img = Image.open(product_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        draw = ImageDraw.Draw(img)
        w, h = img.size
        
        try:
            font_small = ImageFont.truetype(FONT_TITLE, int(min(w, h) * 0.04))
        except:
            font_small = ImageFont.load_default()
        
        gold = hex_to_rgb('#D4B68A')
        label = f"{tea_name} ·{season}·"
        
        bbox = draw.textbbox((0, 0), label, font=font_small)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (w - text_w) // 2
        y = 15
        
        bg_box = [x - 10, y - 5, x + text_w + 10, y + text_h + 5]
        draw.rectangle(bg_box, fill=(26, 26, 26, 180))
        
        draw.text((x, y), label, fill=gold, font=font_small)
        
        draw_seal(draw, w - 55, h - 55, 40)
        
        img.save(output_path, 'JPEG', quality=80, optimize=True)
        print(f"产品图处理完成: {output_path}")
        return output_path
    except Exception as e:
        print(f"处理产品图失败: {e}")
        return product_path

def process_all_images():
    """处理所有产品图和水墨图"""
    os.makedirs("./白茶品牌/images/processed", exist_ok=True)
    
    processed = {}
    for p in PRODUCTS:
        name = p['name']
        
        ink_output = f"./白茶品牌/images/processed/{name}_ink.jpg"
        processed_ink = add_title_to_ink_image(p['ink_img'], name, ink_output)
        
        product_output = f"./白茶品牌/images/processed/{name}_product.jpg"
        processed_product = add_info_to_product_image(
            p['product_img'], p['tea_name'], p['season'], product_output
        )
        
        processed[name] = {
            'ink': processed_ink,
            'product': processed_product
        }
    
    return processed

# ==================== PDF页面函数 ====================

def create_cover_page(c, width, height):
    """封面页 - 黑底金字"""
    c.setFillColor(DEEP_BLACK)
    c.rect(0, 0, width, height, fill=1)
    
    c.setFillColor(WARM_GOLD)
    c.setFont('WenQuanYiZenHei', 88)
    title = "南山帖"
    title_bbox = c.stringWidth(title, 'WenQuanYiZenHei', 88)
    c.drawString((width - title_bbox) / 2, height * 0.6, title)
    
    c.setFont('WenQuanYiZenHei', 36)
    subtitle = "政和·白茶"
    sub_bbox = c.stringWidth(subtitle, 'WenQuanYiZenHei', 36)
    c.drawString((width - sub_bbox) / 2, height * 0.5, subtitle)
    
    c.setStrokeColor(WARM_GOLD)
    c.setLineWidth(0.5)
    line_y = height * 0.45
    c.line(width * 0.35, line_y, width * 0.65, line_y)
    
    c.setFont('WenQuanYiZenHei', 24)
    footer = "四季十二客·三传说"
    footer_bbox = c.stringWidth(footer, 'WenQuanYiZenHei', 24)
    c.drawString((width - footer_bbox) / 2, height * 0.35, footer)
    
    seal_x = width - 60
    seal_y = 50
    seal_size = 35
    c.setStrokeColor(VERMILLION)
    c.setLineWidth(2)
    c.rect(seal_x, seal_y, seal_size, seal_size, stroke=1, fill=0)
    c.setFillColor(VERMILLION)
    c.setFont('WenQuanYiZenHei', 20)
    c.drawString(seal_x + 8, seal_y + 8, "南")

def create_brand_intro_page(c, width, height):
    """品牌序页"""
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, width, height, fill=1)
    
    c.setStrokeColor(HexColor('#D4B68A33'))
    c.setLineWidth(1)
    c.line(30, height * 0.15, 30, height * 0.85)
    
    seal_x = width - 70
    seal_y = height - 80
    seal_size = 40
    c.setStrokeColor(VERMILLION)
    c.setLineWidth(2)
    c.rect(seal_x, seal_y, seal_size, seal_size, stroke=1, fill=0)
    c.setFillColor(VERMILLION)
    c.setFont('WenQuanYiZenHei', 22)
    c.drawString(seal_x + 9, seal_y + 10, "南")
    
    c.setFillColor(TEXT_GRAY)
    c.setFont('WenQuanYiMicroHei', 18)
    
    lines = [
        "南山有四季，四季有十二客。",
        "每一位山客，都是一盏茶的故事。",
        "",
        "政和山间，雾起雾落，",
        "茶人守着老手艺，",
        "等一片叶子慢慢变老。",
        "",
        "这帖，写给山，",
        "写给茶，写给品茶的人。"
    ]
    
    start_y = height * 0.7
    for i, line in enumerate(lines):
        line_bbox = c.stringWidth(line, 'WenQuanYiMicroHei', 18)
        x = (width - line_bbox) / 2 + 20
        c.drawString(x, start_y - i * 35, line)

def create_overview_page(c, width, height, title, items):
    """总览页"""
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, width, height, fill=1)
    
    c.setFillColor(WARM_GOLD)
    c.setFont('WenQuanYiZenHei', 36)
    title_bbox = c.stringWidth(title, 'WenQuanYiZenHei', 36)
    c.drawString((width - title_bbox) / 2, height * 0.85, title)
    
    c.setStrokeColor(WARM_GOLD)
    c.setLineWidth(0.5)
    c.line(width * 0.35, height * 0.8, width * 0.65, height * 0.8)
    
    c.setFillColor(TEXT_GRAY)
    c.setFont('WenQuanYiMicroHei', 16)
    
    start_y = height * 0.7
    col1_x = width * 0.2
    col2_x = width * 0.55
    
    for i, item in enumerate(items):
        row = i // 2
        col = i % 2
        x = col1_x if col == 0 else col2_x
        y = start_y - row * 40
        
        text = f"{item['name']}  |  {item['tea_name']}  |  「{item['season']}」"
        c.drawString(x, y, text)
    
    seal_x = width - 70
    seal_y = 50
    seal_size = 40
    c.setStrokeColor(VERMILLION)
    c.setLineWidth(2)
    c.rect(seal_x, seal_y, seal_size, seal_size, stroke=1, fill=0)
    c.setFillColor(VERMILLION)
    c.setFont('WenQuanYiZenHei', 22)
    c.drawString(seal_x + 9, seal_y + 10, "南")

def wrap_text(text, c, font_name, font_size, max_width):
    """文本换行"""
    lines = []
    current_line = ""
    
    for char in text:
        test_line = current_line + char
        bbox = c.stringWidth(test_line, font_name, font_size)
        
        if bbox <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = char
    
    if current_line:
        lines.append(current_line)
    
    return lines

def create_product_detail_page(c, width, height, product, processed_images):
    """山客详情页 - 融合布局"""
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, width, height, fill=1)
    
    name = product['name']
    tea_name = product['tea_name']
    season = product['season']
    
    # 上半部分：左右并列图片区
    img_area_height = height * 0.50
    img_bottom_y = height * 0.40
    img_area_width = (width - MARGIN * 2) / 2 - 5
    
    # 左侧：产品实拍图
    product_img_path = processed_images['product']
    try:
        product_img = Image.open(product_img_path)
        pw, ph = product_img.size
        
        scale = img_area_height / ph
        display_w = pw * scale
        display_h = img_area_height
        
        if display_w > img_area_width:
            scale = img_area_width / pw
            display_w = img_area_width
            display_h = ph * scale
        
        img_x = MARGIN + (img_area_width - display_w) / 2
        c.drawImage(product_img_path, img_x, img_bottom_y, 
                   width=display_w, height=display_h,
                   preserveAspectRatio=True)
    except Exception as e:
        print(f"绘制产品图失败: {e}")
    
    # 右侧：水墨形象图
    ink_img_path = processed_images['ink']
    try:
        ink_img = Image.open(ink_img_path)
        iw, ih = ink_img.size
        
        scale = img_area_height / ih
        display_w = iw * scale
        display_h = img_area_height
        
        if display_w > img_area_width:
            scale = img_area_width / iw
            display_w = img_area_width
            display_h = ih * scale
        
        img_x = MARGIN + img_area_width + 10 + (img_area_width - display_w) / 2
        c.drawImage(ink_img_path, img_x, img_bottom_y,
                   width=display_w, height=display_h,
                   preserveAspectRatio=True)
    except Exception as e:
        print(f"绘制水墨图失败: {e}")
    
    # 下半部分：文字区
    text_top_y = img_bottom_y - 10
    text_bottom_y = 35
    
    current_y = text_top_y - 15
    
    # 山客名 + 茶品名 + 季节
    c.setFillColor(WARM_GOLD)
    c.setFont('WenQuanYiZenHei', 26)
    name_text = name
    c.drawString(MARGIN, current_y, name_text)
    
    c.setFont('WenQuanYiMicroHei', 13)
    detail_text = f"  {tea_name}  ·{season}·"
    c.drawString(MARGIN + c.stringWidth(name_text, 'WenQuanYiZenHei', 26) + 5, 
                 current_y + 4, detail_text)
    
    current_y -= 8
    
    # 分隔线
    c.setStrokeColor(WARM_GOLD)
    c.setLineWidth(0.5)
    c.line(MARGIN, current_y, width - MARGIN, current_y)
    
    current_y -= 12
    
    # 故事全文
    c.setFillColor(TEXT_GRAY)
    c.setFont('WenQuanYiMicroHei', 10)
    
    story_lines = wrap_text(product['story'], c, 'WenQuanYiMicroHei', 10, 
                           width - MARGIN * 2)
    
    for line in story_lines:
        if current_y > text_bottom_y + 85:
            c.drawString(MARGIN, current_y, line)
            current_y -= 14
    
    current_y -= 3
    
    # 风味笔记
    c.setFillColor(ANNOTATION_GRAY)
    c.setFont('WenQuanYiZenHei', 10)
    c.drawString(MARGIN, current_y, "风味笔记")
    current_y -= 12
    
    c.setFillColor(TEXT_GRAY)
    c.setFont('WenQuanYiMicroHei', 9)
    flavor_lines = wrap_text(product['flavor'], c, 'WenQuanYiMicroHei', 9,
                            width - MARGIN * 2)
    for line in flavor_lines:
        if current_y > text_bottom_y + 45:
            c.drawString(MARGIN, current_y, line)
            current_y -= 11
    
    current_y -= 3
    
    # 收藏价值
    c.setFillColor(ANNOTATION_GRAY)
    c.setFont('WenQuanYiZenHei', 10)
    c.drawString(MARGIN, current_y, "收藏价值")
    current_y -= 12
    
    c.setFillColor(TEXT_GRAY)
    c.setFont('WenQuanYiMicroHei', 9)
    value_lines = wrap_text(product['value'], c, 'WenQuanYiMicroHei', 9,
                           width - MARGIN * 2)
    for line in value_lines:
        if current_y > text_bottom_y + 20:
            c.drawString(MARGIN, current_y, line)
            current_y -= 11
    
    # 签文
    c.setFillColor(WARM_GOLD)
    c.setFont('WenQuanYiMicroHei', 10)
    c.drawString(MARGIN, text_bottom_y + 3, product['quote'])

def create_quote_page(c, width, height):
    """签文摘选页"""
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, width, height, fill=1)
    
    c.setFillColor(WARM_GOLD)
    c.setFont('WenQuanYiZenHei', 28)
    title = "签文 · 摘选"
    title_bbox = c.stringWidth(title, 'WenQuanYiZenHei', 28)
    c.drawString((width - title_bbox) / 2, height * 0.9, title)
    
    c.setStrokeColor(WARM_GOLD)
    c.setLineWidth(0.5)
    c.line(width * 0.35, height * 0.85, width * 0.65, height * 0.85)
    
    c.setFont('WenQuanYiMicroHei', 11)
    start_y = height * 0.78
    
    for i, product in enumerate(PRODUCTS):
        row = i // 2
        col = i % 2
        
        x = width * 0.12 if col == 0 else width * 0.52
        y = start_y - row * 50
        
        c.setFillColor(WARM_GOLD)
        c.setFont('WenQuanYiZenHei', 12)
        c.drawString(x, y, product['name'])
        
        c.setFillColor(TEXT_GRAY)
        c.setFont('WenQuanYiMicroHei', 10)
        c.drawString(x + 55, y, product['quote'])
    
    seal_x = width - 70
    seal_y = 50
    seal_size = 40
    c.setStrokeColor(VERMILLION)
    c.setLineWidth(2)
    c.rect(seal_x, seal_y, seal_size, seal_size, stroke=1, fill=0)
    c.setFillColor(VERMILLION)
    c.setFont('WenQuanYiZenHei', 22)
    c.drawString(seal_x + 9, seal_y + 10, "南")

def create_philosophy_page(c, width, height):
    """品牌理念页"""
    c.setFillColor(DEEP_BLACK)
    c.rect(0, 0, width, height, fill=1)
    
    c.setFillColor(WARM_GOLD)
    c.setFont('WenQuanYiZenHei', 88)
    title = "你"
    title_bbox = c.stringWidth(title, 'WenQuanYiZenHei', 88)
    c.drawString((width - title_bbox) / 2, height * 0.75, title)
    
    c.setFont('WenQuanYiZenHei', 48)
    subtitle = "是第十三位"
    sub_bbox = c.stringWidth(subtitle, 'WenQuanYiZenHei', 48)
    c.drawString((width - sub_bbox) / 2, height * 0.6, subtitle)
    
    c.setStrokeColor(WARM_GOLD)
    c.setLineWidth(0.5)
    c.line(width * 0.3, height * 0.52, width * 0.7, height * 0.52)
    
    c.setFont('WenQuanYiMicroHei', 18)
    lines = [
        "四季十二客，山间已至",
        "三位传说，等你结缘",
        "",
        "每一位品茶的你，都是独一无二的山客"
    ]
    
    start_y = height * 0.45
    for i, line in enumerate(lines):
        line_bbox = c.stringWidth(line, 'WenQuanYiMicroHei', 18)
        c.drawString((width - line_bbox) / 2, start_y - i * 30, line)

def create_contact_page(c, width, height):
    """联系方式页"""
    c.setFillColor(PAPER_WHITE)
    c.rect(0, 0, width, height, fill=1)
    
    qr_path = "./用户上传/photo-1777830978310.jpg"
    if os.path.exists(qr_path):
        try:
            qr_size = 180
            qr_x = (width - qr_size) / 2
            qr_y = height * 0.52
            c.drawImage(qr_path, qr_x, qr_y, width=qr_size, height=qr_size)
        except Exception as e:
            print(f"绘制二维码失败: {e}")
    
    c.setFillColor(WARM_GOLD)
    c.setFont('WenQuanYiZenHei', 22)
    scan_text = "扫码·遇见你的山客"
    scan_bbox = c.stringWidth(scan_text, 'WenQuanYiZenHei', 22)
    c.drawString((width - scan_bbox) / 2, height * 0.42, scan_text)
    
    c.setFillColor(TEXT_GRAY)
    c.setFont('WenQuanYiMicroHei', 14)
    lines = ["南山帖", "政和·白茶", "四季十二客·三传说"]
    
    start_y = height * 0.32
    for i, line in enumerate(lines):
        line_bbox = c.stringWidth(line, 'WenQuanYiMicroHei', 14)
        c.drawString((width - line_bbox) / 2, start_y - i * 25, line)
    
    seal_x = width - 70
    seal_y = 50
    seal_size = 40
    c.setStrokeColor(VERMILLION)
    c.setLineWidth(2)
    c.rect(seal_x, seal_y, seal_size, seal_size, stroke=1, fill=0)
    c.setFillColor(VERMILLION)
    c.setFont('WenQuanYiZenHei', 22)
    c.drawString(seal_x + 9, seal_y + 10, "南")

# ==================== 主函数 ====================

def create_brand_manual_v3():
    """创建第三版品牌手册"""
    print("开始创建南山帖品牌手册第三版...")
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    
    if not register_fonts():
        print("字体注册失败，退出")
        return False
    
    print("正在处理图片...")
    processed_images = process_all_images()
    
    print("正在创建PDF...")
    c = canvas.Canvas(OUTPUT_PATH, pagesize=A4)
    width, height = PAGE_WIDTH, PAGE_HEIGHT
    
    # 第1页 - 封面
    print("创建封面页...")
    create_cover_page(c, width, height)
    c.showPage()
    
    # 第2页 - 品牌序
    print("创建品牌序页...")
    create_brand_intro_page(c, width, height)
    c.showPage()
    
    # 第3页 - 春·夏总览
    print("创建春·夏总览页...")
    spring_summer = [p for p in PRODUCTS if p['season'] in ['春', '夏']]
    create_overview_page(c, width, height, "春 · 夏", spring_summer)
    c.showPage()
    
    # 第4页 - 秋·冬总览
    print("创建秋·冬总览页...")
    autumn_winter = [p for p in PRODUCTS if p['season'] in ['秋', '冬']]
    create_overview_page(c, width, height, "秋 · 冬", autumn_winter)
    c.showPage()
    
    # 第5页 - 四时·传说总览
    print("创建四时·传说总览页...")
    legend = [p for p in PRODUCTS if p['season'] in ['四时', '传说']]
    create_overview_page(c, width, height, "四时 · 传说", legend)
    c.showPage()
    
    # 第6-20页 - 山客详情页
    for i, product in enumerate(PRODUCTS):
        print(f"创建山客详情页 {i+1}/15: {product['name']}...")
        name = product['name']
        if name in processed_images:
            create_product_detail_page(c, width, height, product, processed_images[name])
        else:
            create_product_detail_page(c, width, height, product, {
                'ink': product['ink_img'],
                'product': product['product_img']
            })
        c.showPage()
    
    # 第21页 - 签文摘选
    print("创建签文摘选页...")
    create_quote_page(c, width, height)
    c.showPage()
    
    # 第22页 - 品牌理念
    print("创建品牌理念页...")
    create_philosophy_page(c, width, height)
    c.showPage()
    
    # 第23页 - 联系方式
    print("创建联系方式页...")
    create_contact_page(c, width, height)
    c.showPage()
    
    c.save()
    print(f"PDF保存完成: {OUTPUT_PATH}")
    
    return True

if __name__ == "__main__":
    create_brand_manual_v3()
