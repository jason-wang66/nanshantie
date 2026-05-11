import base64, re, os, urllib.parse
from PIL import Image
import io

def compress_image(filepath, max_width=800, quality=70):
    img = Image.open(filepath)
    if img.width > max_width:
        ratio = max_width / img.width
        new_size = (max_width, int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=quality, optimize=True)
    return buf.getvalue()

with open('抽签.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 山客形象图片映射
portrait_map = {
    '童濛': '山客形象/童濛.jpg',
    '浮岚': '山客形象/浮岚.jpg',
    '不器': '山客形象/不器.jpg',
    '丹桂': '山客形象/丹桂.jpg',
    '履霜': '山客形象/履霜.jpg',
    '漱雪': '山客形象/漱雪.jpg',
    '漱月': '山客形象/漱月.jpg',
    '莫离': '山客形象/莫离.jpg',
}

# 产品图片映射 - 使用实际存在的文件
product_map = {
    'product_tongmeng': '../用户上传/IMG_9722_1777823187995_eidk.jpg',
    'product_fulan': '../用户上传/IMG_9723_1777823188319_wm8i.jpg',
    'product_buqi': '../用户上传/IMG_9724_1777823188682_g4mn.jpg',
    'product_dangui': '../用户上传/IMG_9725_1777823190358_n21b.jpg',
    'product_lvshuang': '../用户上传/IMG_9726_1777823189992_j15e.jpg',
    'product_shuxue': '../用户上传/IMG_9727_1777823189473_li4f.jpg',
    'product_shuyue': '../用户上传/IMG_9728_1777823189075_zw44.jpg',
    'product_moli': '../用户上传/photo-1777823574781.jpg',  # 莫离图片
}

# 微信二维码
wechat_qr = '../用户上传/photo-1777830978310.jpg'

# 替换山客形象图片
for name, filepath in portrait_map.items():
    encoded_name = urllib.parse.quote(name)
    pattern = f'images/{encoded_name}.jpg'
    if os.path.exists(filepath):
        compressed = compress_image(filepath, max_width=600, quality=70)
        b64 = base64.b64encode(compressed).decode('utf-8')
        html = html.replace(pattern, f'data:image/jpeg;base64,{b64}')
        print(f'Replaced portrait: {name}')
    else:
        print(f'NOT FOUND: {filepath}')

# 替换产品图片
for key, filepath in product_map.items():
    pattern = f'images/{key}.jpg'
    if os.path.exists(filepath):
        compressed = compress_image(filepath, max_width=800, quality=70)
        b64 = base64.b64encode(compressed).decode('utf-8')
        html = html.replace(pattern, f'data:image/jpeg;base64,{b64}')
        print(f'Replaced product: {key}')
    else:
        print(f'NOT FOUND: {filepath}')

# 替换微信二维码
if os.path.exists(wechat_qr):
    compressed = compress_image(wechat_qr, max_width=400, quality=75)
    b64 = base64.b64encode(compressed).decode('utf-8')
    html = html.replace('images/wechat_qr.jpg', f'data:image/jpeg;base64,{b64}')
    print('Replaced wechat_qr')
else:
    print(f'NOT FOUND: {wechat_qr}')

# 保存内联版
with open('抽签_内联版.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f'\nGenerated: 抽签_内联版.html')
print(f'File size: {len(html) / 1024 / 1024:.2f} MB')
