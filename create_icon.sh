#!/bin/bash

# 创建必要的目录
mkdir icon.iconset

# 使用 Python 和 PIL 库生成基础图标
python3 - << EOF
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size):
    # 创建一个正方形图像，使用深蓝色背景
    img = Image.new('RGB', (size, size), '#2B5B84')
    draw = ImageDraw.Draw(img)
    
    # 绘制一个圆形
    padding = size // 8
    draw.ellipse([padding, padding, size-padding, size-padding], fill='#FFFFFF')
    
    # 在圆形中绘制 "RT" 文字
    try:
        # 尝试使用系统字体
        font_size = size // 2
        font = ImageFont.truetype('/System/Library/Fonts/SFCompact.ttf', font_size)
    except:
        # 如果找不到指定字体，使用默认字体
        font = ImageFont.load_default()
    
    text = "RT"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    draw.text((x, y), text, fill='#2B5B84', font=font)
    
    return img

# 生成不同尺寸的图标
sizes = [16, 32, 64, 128, 256, 512, 1024]
for size in sizes:
    icon = create_icon(size)
    # 保存普通尺寸
    icon.save(f'icon.iconset/icon_{size}x{size}.png')
    # 保存 @2x 尺寸（如果不是最大尺寸）
    if size * 2 <= 1024:
        icon_2x = create_icon(size * 2)
        icon_2x.save(f'icon.iconset/icon_{size}x{size}@2x.png')
EOF

# 使用 iconutil 将图标集转换为 .icns 文件
iconutil -c icns icon.iconset

# 清理临时文件
rm -rf icon.iconset

# 设置图标到应用程序
echo "Icon created successfully as icon.icns" 