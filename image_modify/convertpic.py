from PIL import Image, ImageDraw, ImageFont
import os

# 定义文件夹路径
prepic_folder = '/Users/songyujian/Documents/np'
newpic_folder = '/Users/songyujian/Documents/nn'

# 定义目标图片大小和间隔
target_size = (450, 450)
spacing = 10  # 图片之间的空白
title_spacing = 30  # 标题和图片之间的空白
font_size = 64  # 字体大小

# 获取两个文件夹内的所有png文件名，并按数字顺序排序
prepic_files = sorted([f for f in os.listdir(prepic_folder) if f.endswith('.png')], key=lambda x: int(x.split('.')[0]))
newpic_files = sorted([f for f in os.listdir(newpic_folder) if f.endswith('.png')], key=lambda x: int(x.split('.')[0]))

# 裁剪或缩放图片为目标大小
def process_images(files, folder):
    images = []
    for file in files:
        img = Image.open(os.path.join(folder, file))
        if img.size[0] < target_size[0] or img.size[1] < target_size[1]:
            img = img.resize(target_size, Image.ANTIALIAS)
        width, height = img.size
        left = (width - target_size[0])/2
        top = (height - target_size[1])/2
        right = (width + target_size[0])/2
        bottom = (height + target_size[1])/2
        img = img.crop((left, top, right, bottom))
        images.append(img)
    return images

prepic_images = process_images(prepic_files, prepic_folder)
newpic_images = process_images(newpic_files, newpic_folder)

# 计算总宽度
total_width = (target_size[0] + spacing) * max(len(prepic_images), len(newpic_images)) - spacing

# 创建一张新图像，大小足以容纳两行图片、间隔和标题
output_image = Image.new('RGB', (total_width, 2 * target_size[1] + 3 * spacing + 2 * title_spacing + 2 * font_size), 'white')

# 添加文本的函数
def add_text(draw, text, position, font):
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (output_image.width - text_width) // 2
    text_y = position
    draw.text((text_x, text_y), text, font=font, fill="black")

# 准备绘制文本
font_path = '/Users/songyujian/Downloads/Songti.ttc'
font = ImageFont.truetype(font_path, font_size)
draw = ImageDraw.Draw(output_image)

# 在上方添加标题
add_text(draw, "生成的最佳假照片", spacing, font)

# 将图片按顺序粘贴到新图像上，添加间隔
current_width = 0
for image in prepic_images:
    output_image.paste(image, (current_width, spacing + title_spacing + font_size))
    current_width += target_size[0] + spacing

# 在中间添加第二个标题
add_text(draw, "生成的修复图片", target_size[1] + 2 * spacing + title_spacing + font_size, font)

current_width = 0
for image in newpic_images:
    output_image.paste(image, (current_width, 2 * spacing + 2 * title_spacing + 2 * font_size + target_size[1]))
    current_width += target_size[0] + spacing

# 保存最终的图片
output_image.save('/Users/songyujian/Documents/output3.png')

# 显示最终的图片（可选）
output_image.show()
