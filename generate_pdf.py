#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
南山帖白茶品牌产品手册PDF生成脚本（运势签版）
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, 
    PageBreak, Table, TableStyle, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage

# 注册中文字体
FONT_TITLE = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
FONT_BODY = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
pdfmetrics.registerFont(TTFont('WenQuanYiZenHei', FONT_TITLE))
pdfmetrics.registerFont(TTFont('WenQuanYiMicroHei', FONT_BODY))

# 配色方案
BG_COLOR = HexColor('#1a1a1a')  # 深色背景
GOLD_COLOR = HexColor('#C9A96E')  # 暗金色
CREAM_COLOR = HexColor('#F5F0E8')  # 米色/象牙白
WARM_COLOR = HexColor('#C4956A')  # 暖色 - 宜
COLD_COLOR = HexColor('#8B7D6B')  # 冷色 - 忌
TEXT_LIGHT = HexColor('#E8E4DE')  # 浅色文字
TEXT_DIM = HexColor('#9A958E')  # 暗淡文字

# 页面尺寸
PAGE_WIDTH, PAGE_HEIGHT = A4  # 595.27 x 841.89 points
MARGIN = 1.8 * cm

# 图片路径
IMAGE_DIR = './用户上传'

# 产品图片映射
PRODUCT_IMAGES = {
    '白毫银针': 'IMG_9722_1777823187995_eidk.jpg',
    '福建高山绿茶': 'IMG_9727_1777823189473_li4f.jpg',
    '白牡丹': 'IMG_9724_1777823188682_g4mn.jpg',
    '桂花红茶': 'IMG_9723_1777823188319_wm8i.jpg',
    '工夫红茶': 'IMG_9725_1777823190358_n21b.jpg',
    '茉莉绿茶': 'IMG_9726_1777823189992_j15e.jpg',
    '茉莉红茶': 'IMG_9728_1777823189075_zw44.jpg',
    '茉莉银针': 'photo-1777823574781.jpg',
}

# 八签数据
SIGNS = [
    {
        'name': '童濛',
        'product': '白毫银针',
        'season': '春',
        'star': '★★★★☆',
        'yi': ['开始新事', '见老友', '喝第一泡'],
        'ji': ['犹豫不决', '故作老成'],
        'quote': '万物初生，不必清明',
        'story': '春山初醒，晨雾未散。露水从叶尖滑落，跌进泥土里，发出极轻的声响。有个孩子赤脚走过山径，衣襟上沾着青草的汁液，眼睛像刚洗过的天空。他看什么都新鲜，看什么都欢喜。山雀掠过，他仰头；野花绽放，他俯身。他叫童濛——是万物初生时的模样，是天地间第一缕干净的呼吸。',
        'maker': '政和白茶非遗传承人 吴文信',
    },
    {
        'name': '浮岚',
        'product': '福建高山绿茶',
        'season': '春',
        'star': '★★★☆☆',
        'yi': ['独处', '发呆', '出远门'],
        'ji': ['钻牛角尖', '追问到底'],
        'quote': '看得见就够了，握不住也没关系',
        'story': '午后，山谷里起了雾。不是浓得化不开的那种，而是轻薄的，游走的，像是山在呼吸。雾从溪面升起，绕过松林，在半山腰停住。有个少年站在雾里，衣袂被风轻轻吹起，看不清面容，只觉得他整个人都像是从云中长出来的。他叫浮岚——是山与天的交界，是看得见却握不住的轻盈。',
        'maker': '制茶工程师 吴文信',
    },
    {
        'name': '不器',
        'product': '白牡丹',
        'season': '夏',
        'star': '★★★★★',
        'yi': ['随性而为', '请客喝茶', '不设目标'],
        'ji': ['给自己贴标签', '非此即彼'],
        'quote': '君子不器，何必定义',
        'story': '夏日漫长，蝉声如织。树荫下坐着一个人，他面前摆着粗陶碗，碗里盛着清水。有人来问路，他指；有人来借火，他给；有人来闲谈，他听。他不拒绝任何人，也不强留任何人。他的性子温和，不偏不倚，像是山间的风，吹过就算了。他叫不器——君子不器，他什么都是，也什么都不是。',
        'maker': '政和白茶非遗传承人 吴文信',
    },
    {
        'name': '丹桂',
        'product': '桂花红茶',
        'season': '秋',
        'star': '★★★★☆',
        'yi': ['想念一个人', '写一封信', '收藏小东西'],
        'ji': ['贪多求全', '忽略细节'],
        'quote': '不必是全部，做那个让人惦记的部分',
        'story': '入秋之前，院子里那棵桂树先开了花。不是满树金黄，只是疏疏几簇，香气却已经藏不住了。有个女子在树下铺了竹匾，将落花拢在一起。她动作很轻，怕惊扰了那些细小的花瓣。她叫丹桂——不是秋天的全部，却是秋天最让人惦记的那一部分。',
        'maker': '制茶工程师 吴文信',
    },
    {
        'name': '履霜',
        'product': '工夫红茶',
        'season': '冬',
        'star': '★★★★☆',
        'yi': ['出门走走', '给家里打电话', '接受不完美'],
        'ji': ['逞强硬撑', '拒绝温暖'],
        'quote': '踩在冬天边缘的人，也带着火种',
        'story': '第一场霜落下来的时候，她来了。她穿着素色的衣裳，走路很轻，踩在霜叶上，发出细微的碎裂声。她带来一篮火红的果子，说是山里采的。屋里生了炭火，她坐在火边，影子被拉得很长。有人递给她一杯热水，她捧在手里，却没有喝，只是看着热气慢慢升起来。她叫履霜——是踩在冬天边缘的人，也是带来温暖的人。',
        'maker': '制茶工艺师 吴文信 手制',
    },
    {
        'name': '漱雪',
        'product': '茉莉绿茶',
        'season': '冬',
        'star': '★★★☆☆',
        'yi': ['安静做事', '赏花看雪', '少说话'],
        'ji': ['喧哗', '急躁', '赶路'],
        'quote': '南方有雪不易，安安静静就好',
        'story': '大雪封山之后，另一个女子出现了。她喜欢在雪地里走，留下一串浅浅的脚印。她走到梅树下，仰头看枝头的积雪。风吹过，雪落了她一身，她也不拂，只是站在那里，像是自己也成了一株梅。她叫漱雪——南方有雪不易。',
        'maker': '制茶工程师 吴文信',
    },
    {
        'name': '漱月',
        'product': '茉莉红茶',
        'season': '冬',
        'star': '★★★★☆',
        'yi': ['夜间独坐', '听音乐', '与月对饮'],
        'ji': ['太清醒', '事事讲道理'],
        'quote': '碎了的月亮，掬起来还会圆',
        'story': '月圆那夜，有人在溪边掬水。水里有月亮的倒影，她掬起来，月亮就碎了；再掬，又圆了。她一遍一遍地掬，像是在玩一个永远不会腻的游戏。她的影子落在水面上，和月亮混在一起，分不清哪个是她，哪个是月。她叫漱月——是用溪水洗月亮的人。',
        'maker': '制茶工程师 吴文信',
    },
    {
        'name': '莫离',
        'product': '茉莉银针',
        'season': '四时',
        'star': '★★★★★',
        'yi': ['陪伴', '长谈', '为一个人留一盏灯'],
        'ji': ['轻易说再见', '把花收太紧'],
        'quote': '不离开，就是最好的承诺',
        'story': '这些人来来去去，但总有一个人一直在。她住在山脚下那间小屋，屋前种着茉莉。花开的时候，满院子都是白的。她采花，晾花，然后把花收进瓷罐里，一层一层地铺好。有人问她为什么总是不离开，她指了指那罐花，又指了指自己。她叫莫离——花与人，都不分离。',
        'maker': '制茶工程师 吴文信',
    },
]

# ========== 样式定义 ==========
def create_styles():
    """创建所有样式"""
    styles = {}
    
    # 封面标题
    styles['cover_title'] = ParagraphStyle(
        'cover_title',
        fontName='WenQuanYiZenHei',
        fontSize=72,
        leading=80,
        alignment=TA_CENTER,
        textColor=CREAM_COLOR,
        spaceAfter=20,
    )
    
    # 封面副标题
    styles['cover_subtitle'] = ParagraphStyle(
        'cover_subtitle',
        fontName='WenQuanYiMicroHei',
        fontSize=18,
        leading=26,
        alignment=TA_CENTER,
        textColor=TEXT_DIM,
        spaceAfter=0,
    )
    
    # 开篇大文字
    styles['opening'] = ParagraphStyle(
        'opening',
        fontName='WenQuanYiZenHei',
        fontSize=28,
        leading=42,
        alignment=TA_CENTER,
        textColor=CREAM_COLOR,
        spaceAfter=0,
    )
    
    # 章节标题（制茶人）
    styles['section_title'] = ParagraphStyle(
        'section_title',
        fontName='WenQuanYiZenHei',
        fontSize=36,
        leading=44,
        alignment=TA_CENTER,
        textColor=CREAM_COLOR,
        spaceAfter=30,
    )
    
    # 制茶人名字
    styles['maker_name'] = ParagraphStyle(
        'maker_name',
        fontName='WenQuanYiZenHei',
        fontSize=24,
        leading=32,
        alignment=TA_CENTER,
        textColor=GOLD_COLOR,
        spaceAfter=20,
    )
    
    # 制茶人描述
    styles['maker_desc'] = ParagraphStyle(
        'maker_desc',
        fontName='WenQuanYiMicroHei',
        fontSize=14,
        leading=22,
        alignment=TA_CENTER,
        textColor=TEXT_DIM,
        spaceAfter=0,
    )
    
    # 签页山客名
    styles['sign_name'] = ParagraphStyle(
        'sign_name',
        fontName='WenQuanYiZenHei',
        fontSize=48,
        leading=56,
        alignment=TA_CENTER,
        textColor=CREAM_COLOR,
        spaceAfter=4,
    )
    
    # 签页茶品名
    styles['sign_product'] = ParagraphStyle(
        'sign_product',
        fontName='WenQuanYiMicroHei',
        fontSize=16,
        leading=22,
        alignment=TA_CENTER,
        textColor=TEXT_DIM,
        spaceAfter=0,
    )
    
    # 运势星级
    styles['sign_star'] = ParagraphStyle(
        'sign_star',
        fontName='WenQuanYiMicroHei',
        fontSize=20,
        leading=28,
        alignment=TA_CENTER,
        textColor=GOLD_COLOR,
        spaceAfter=0,
    )
    
    # 签语
    styles['sign_quote'] = ParagraphStyle(
        'sign_quote',
        fontName='WenQuanYiZenHei',
        fontSize=18,
        leading=28,
        alignment=TA_CENTER,
        textColor=CREAM_COLOR,
        spaceAfter=0,
    )
    
    # 宜忌标签
    styles['label'] = ParagraphStyle(
        'label',
        fontName='WenQuanYiZenHei',
        fontSize=12,
        leading=18,
        alignment=TA_CENTER,
        textColor=CREAM_COLOR,
        spaceAfter=0,
    )
    
    # 宜忌内容
    styles['yi_content'] = ParagraphStyle(
        'yi_content',
        fontName='WenQuanYiMicroHei',
        fontSize=11,
        leading=16,
        alignment=TA_LEFT,
        textColor=WARM_COLOR,
        spaceAfter=0,
    )
    
    styles['ji_content'] = ParagraphStyle(
        'ji_content',
        fontName='WenQuanYiMicroHei',
        fontSize=11,
        leading=16,
        alignment=TA_LEFT,
        textColor=COLD_COLOR,
        spaceAfter=0,
    )
    
    # 故事正文
    styles['story'] = ParagraphStyle(
        'story',
        fontName='WenQuanYiMicroHei',
        fontSize=12,
        leading=20,
        alignment=TA_LEFT,
        textColor=TEXT_LIGHT,
        spaceAfter=0,
    )
    
    # 制作人信息
    styles['maker_info'] = ParagraphStyle(
        'maker_info',
        fontName='WenQuanYiMicroHei',
        fontSize=9,
        leading=14,
        alignment=TA_CENTER,
        textColor=TEXT_DIM,
        spaceAfter=0,
    )
    
    # 尾页正文
    styles['ending'] = ParagraphStyle(
        'ending',
        fontName='WenQuanYiMicroHei',
        fontSize=13,
        leading=24,
        alignment=TA_CENTER,
        textColor=TEXT_LIGHT,
        spaceAfter=0,
    )
    
    return styles


# ========== 页面背景 ==========
def on_page(canvas_obj, doc):
    """绘制页面背景"""
    canvas_obj.saveState()
    canvas_obj.setFillColor(BG_COLOR)
    canvas_obj.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    canvas_obj.restoreState()


# ========== 内容生成函数 ==========
def get_image_path(product_name):
    """获取产品图片路径"""
    filename = PRODUCT_IMAGES.get(product_name, '')
    if filename:
        return os.path.join(IMAGE_DIR, filename)
    return None


def resize_image(img_path, max_width, max_height):
    """等比缩放图片"""
    if not img_path or not os.path.exists(img_path):
        return None
    
    try:
        with PILImage.open(img_path) as img:
            orig_w, orig_h = img.size
            ratio = min(max_width / orig_w, max_height / orig_h)
            new_w = orig_w * ratio
            new_h = orig_h * ratio
            return new_w, new_h
    except Exception as e:
        print(f"图片处理错误: {img_path}, {e}")
        return None


def create_cover_page(styles):
    """创建封面"""
    story = []
    
    # 顶部留白
    story.append(Spacer(1, 4 * cm))
    
    # 南山帖
    story.append(Paragraph('南山帖', styles['cover_title']))
    
    # 副标题
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph('今日你遇见哪位山客？', styles['cover_subtitle']))
    
    return story


def create_opening_page(styles):
    """创建开篇页"""
    story = []
    
    # 大量留白
    story.append(Spacer(1, 7 * cm))
    
    story.append(Paragraph('南山有四季，', styles['opening']))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph('四季有十二客。', styles['opening']))
    
    return story


def create_maker_page(styles):
    """创建制茶人页"""
    story = []
    
    # 留白
    story.append(Spacer(1, 5.5 * cm))
    
    story.append(Paragraph('制茶人', styles['section_title']))
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph('政和白茶非遗传承人', styles['maker_desc']))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph('吴文信', styles['maker_name']))
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph('以山为师，以时为法，以手传心', styles['maker_desc']))
    
    return story


def create_sign_page(sign, styles, page_num):
    """创建签页"""
    story = []
    
    # 顶部留白
    story.append(Spacer(1, 1.2 * cm))
    
    # 山客名 + 茶品名
    story.append(Paragraph(sign['name'], styles['sign_name']))
    story.append(Paragraph(sign['product'], styles['sign_product']))
    
    story.append(Spacer(1, 0.6 * cm))
    
    # 运势签区域边框
    sign_content = []
    
    # 运势星级
    sign_content.append(Paragraph(f'<font color="#C9A96E">运势</font>', styles['label']))
    story.append(Paragraph(f'<font color="#C9A96E">运势</font> <font color="#C9A96E">{sign["star"]}</font>', styles['sign_star']))
    
    story.append(Spacer(1, 0.4 * cm))
    
    # 宜
    yi_items = '  ·  '.join(sign['yi'])
    story.append(Paragraph(f'<font color="#C4956A">宜</font>  {yi_items}', styles['yi_content']))
    
    story.append(Spacer(1, 0.25 * cm))
    
    # 忌
    ji_items = '  ·  '.join(sign['ji'])
    story.append(Paragraph(f'<font color="#8B7D6B">忌</font>  {ji_items}', styles['ji_content']))
    
    story.append(Spacer(1, 0.4 * cm))
    
    # 签语
    story.append(Paragraph(f'「{sign["quote"]}」', styles['sign_quote']))
    
    story.append(Spacer(1, 0.5 * cm))
    
    # 产品图片
    img_path = get_image_path(sign['product'])
    if img_path and os.path.exists(img_path):
        # 获取图片尺寸
        img_size = resize_image(img_path, 8 * cm, 6 * cm)
        if img_size:
            img_w, img_h = img_size
            # 居中
            x = (PAGE_WIDTH - img_w) / 2
            story.append(Image(img_path, width=img_w, height=img_h))
            story.append(Spacer(1, 0.5 * cm))
    
    # 故事全文
    story.append(Paragraph(sign['story'], styles['story']))
    
    story.append(Spacer(1, 0.8 * cm))
    
    # 制作人信息
    story.append(Paragraph(sign['maker'], styles['maker_info']))
    
    return story


def create_ending_page(styles):
    """创建尾页"""
    story = []
    
    # 大量留白
    story.append(Spacer(1, 5 * cm))
    
    story.append(Paragraph('莫离在屋前煮水。水开了，她把水倒进碗里，热气升起来，模糊了她的脸。', styles['ending']))
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph('有人推门进来，问："今日喝什么？"', styles['ending']))
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph('她没有回答，只是指了指窗外。', styles['ending']))
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph('窗外，南山正青。', styles['ending']))
    
    return story


# ========== 主函数 ==========
def main():
    """主函数"""
    output_path = './白茶品牌/南山帖产品手册.pdf'
    
    # 创建文档
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )
    
    # 创建样式
    styles = create_styles()
    
    # 构建故事
    story = []
    
    # 第1页 - 封面
    story.extend(create_cover_page(styles))
    story.append(PageBreak())
    
    # 第2页 - 开篇
    story.extend(create_opening_page(styles))
    story.append(PageBreak())
    
    # 第3页 - 制茶人
    story.extend(create_maker_page(styles))
    story.append(PageBreak())
    
    # 第4-11页 - 八签
    for sign in SIGNS:
        story.extend(create_sign_page(sign, styles, len(story)))
        story.append(PageBreak())
    
    # 第12页 - 尾页
    story.extend(create_ending_page(styles))
    
    # 生成PDF
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    
    print(f"PDF已生成: {output_path}")
    return output_path


if __name__ == '__main__':
    main()
