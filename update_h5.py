#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新南山帖H5抽签页中的风味笔记和收藏价值文案
"""

import re
import os

# 基础路径
BASE_PATH = '/app/data/所有对话/主对话/白茶品牌'

# 读取修订文案
def read_revision_content():
    with open(os.path.join(BASE_PATH, '南山帖_手册文案修订.md'), 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按茶名分割
    sections = re.split(r'\n---\n|\n---', content)
    
    products = {}
    current_name = None
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        # 检查是否是茶名标题 (### 开头)
        title_match = re.match(r'### (.+)', section)
        if title_match:
            current_name = title_match.group(1).strip()
            products[current_name] = {
                'flavor': '',
                'value': '',
                'grade': ''
            }
            # 移除标题部分
            section = re.sub(r'### [^\n]+\n', '', section)
        
        if current_name and section:
            # 提取风味笔记
            flavor_match = re.search(r'\*\*风味笔记\*\*\s*\n(.+?)(?=\n\*\*|$)', section, re.DOTALL)
            if flavor_match:
                products[current_name]['flavor'] = flavor_match.group(1).strip()
            
            # 提取藏养
            value_match = re.search(r'\*\*藏养\*\*\s*\n(.+?)(?=\n\*\*|$)', section, re.DOTALL)
            if value_match:
                products[current_name]['value'] = value_match.group(1).strip()
            
            # 提取品第
            grade_match = re.search(r'\*\*品第\*\*\s*\n(.+)', section, re.DOTALL)
            if grade_match:
                products[current_name]['grade'] = grade_match.group(1).strip()
    
    return products

# 读取HTML文件
def read_html():
    with open(os.path.join(BASE_PATH, '抽签_内联版_final.html'), 'r', encoding='utf-8') as f:
        return f.read()

# 茶名映射：HTML中的name -> 完整名称
NAME_MAPPING = {
    '童濛': '童濛 白毫银针 ·春·',
    '浮岚': '浮岚 福建高山绿茶 ·春·',
    '不器': '不器 白牡丹 ·夏·',
    '丹桂': '丹桂 桂花红茶 ·秋·',
    '履霜': '履霜 工夫红茶 ·冬·',
    '漱雪': '漱雪 茉莉绿茶 ·冬·',
    '漱月': '漱月 茉莉红茶 ·冬·',
    '莫离': '莫离 茉莉银针 ·四时·',
    '桂兰': '桂兰 肉桂 ·秋·',
    '步止': '步止 12年白茶饼 ·传说·',
    '听枞': '听枞 老枞 ·秋·',
    '天香': '天香 大红袍 ·秋·',
    '无羁': '无羁 17年白茶饼 ·传说·',
    '南山': '南山 马年茶饼 ·传说·',
    '半见': '半见 陈皮白茶 ·四时·'
}

def update_html_content(html_content, products):
    """更新HTML中的产品数据"""
    
    # CSS样式 - 添加印章/方印样式
    seal_style = """
        .grade-seal {
            margin-top: 20px;
            padding: 12px 16px;
            border: 2px solid #8B4513;
            border-radius: 4px;
            background: linear-gradient(135deg, #FFF8F0 0%, #F5E6D3 100%);
            text-align: center;
            position: relative;
        }
        .grade-seal::before {
            content: '';
            position: absolute;
            top: 4px;
            left: 4px;
            right: 4px;
            bottom: 4px;
            border: 1px solid #8B4513;
            border-radius: 2px;
            pointer-events: none;
        }
        .grade-label {
            font-size: 12px;
            color: #8B4513;
            margin-bottom: 6px;
            font-weight: bold;
            letter-spacing: 2px;
        }
        .grade-text {
            font-size: 14px;
            color: #A0522D;
            font-style: italic;
            line-height: 1.5;
        }
    """
    
    # 将样式插入到</style>标签之前
    html_content = html_content.replace('</style>', seal_style + '\n    </style>')
    
    # 更新HTML模板中的"收藏价值"标签为"藏养"
    html_content = html_content.replace('收藏价值', '藏养')
    
    # 在HTML模板中添加品第显示区域
    grade_html = '''                    <div class="grade-seal">
                        <div class="grade-label">品 第</div>
                        <div class="grade-text" id="productGrade"></div>
                    </div>'''
    
    # 在</div>闭合藏养区域后添加品第
    html_content = re.sub(
        r'(<div class="value-text" id="productValue"></div>\s*</div>\s*</div>)',
        r'\1\n' + grade_html,
        html_content
    )
    
    # 在JavaScript中添加品第显示逻辑
    grade_js = """
                if (product.grade) {
                    document.getElementById('productGrade').innerHTML = product.grade;
                    document.querySelector('.grade-seal').style.display = 'block';
                }"""
    
    html_content = re.sub(
        r"(document\.getElementById\('productValue'\)\.innerHTML = product\.value;)",
        r"\1" + grade_js,
        html_content
    )
    
    # 更新每个产品的flavor、value、grade字段
    for html_name, full_name in NAME_MAPPING.items():
        if full_name not in products:
            print(f"警告: 未找到修订文案中的茶 '{full_name}'")
            continue
        
        data = products[full_name]
        flavor = data['flavor']
        value = data['value']
        grade = data['grade']
        
        # 使用正则表达式替换该产品的字段
        # 匹配从该产品name开始到下一个产品name之前的内容
        # 找到name位置
        name_pattern = f'name: "{html_name}"'
        name_match = re.search(re.escape(name_pattern), html_content)
        if not name_match:
            print(f"未找到产品: {html_name}")
            continue
        
        name_start = name_match.start()
        
        # 找到下一个产品的name（或文件末尾）
        next_name_pattern = r'name:\s*"(' + '|'.join([re.escape(n) for n in NAME_MAPPING.keys()]) + r')"'
        next_matches = list(re.finditer(next_name_pattern, html_content[name_start + len(name_pattern):]))
        if next_matches:
            next_name_start = name_start + len(name_pattern) + next_matches[0].start()
        else:
            next_name_start = len(html_content)
        
        # 提取该产品块
        product_block = html_content[name_start:next_name_start]
        
        # 替换flavor值
        if flavor:
            flavor = flavor.replace('\n', ' ')
            flavor_re = r'(flavor:\s*")[^"]*(")'
            flavor_match = re.search(flavor_re, product_block)
            if flavor_match:
                product_block = re.sub(flavor_re, r'\g<1>' + flavor.replace('"', '\\"') + r'\g<2>', product_block, count=1)
        
        # 替换value值（藏养）
        if value:
            value = value.replace('\n', ' ')
            value_re = r'(value:\s*")[^"]*(")'
            value_match = re.search(value_re, product_block)
            if value_match:
                product_block = re.sub(value_re, r'\g<1>' + value.replace('"', '\\"') + r'\g<2>', product_block, count=1)
        
        # 添加grade字段
        if grade:
            # 在tags字段前添加grade
            grade_escaped = grade.replace('"', '\\"')
            tags_re = r'(,\s*tags:\s*\[)'
            grade_insert = f',\n                    grade: "{grade_escaped}"'
            if re.search(tags_re, product_block):
                product_block = re.sub(tags_re, grade_insert + r'\g<1>', product_block, count=1)
        
        # 替换回原内容
        html_content = html_content[:name_start] + product_block + html_content[next_name_start:]
        
        print(f"已更新: {html_name}")
    
    return html_content

def main():
    print("开始更新南山帖H5页面...")
    
    # 读取修订文案
    print("读取修订文案...")
    products = read_revision_content()
    print(f"共解析到 {len(products)} 款茶")
    
    # 读取HTML
    print("读取HTML文件...")
    html_content = read_html()
    
    # 更新内容
    print("更新内容...")
    html_content = update_html_content(html_content, products)
    
    # 保存文件
    output_path = os.path.join(BASE_PATH, '抽签_内联版_final.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"文件已保存: {output_path}")
    print("更新完成!")

if __name__ == '__main__':
    main()
