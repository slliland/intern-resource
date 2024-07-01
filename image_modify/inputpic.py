from PIL import Image, ImageDraw, ImageFont

# 加载图片
image_path = '/Users/songyujian/Downloads/newcopy1.png'  # 替换为你的图片文件路径
original_image = Image.open(image_path)

# 确保原始图片是450x450像素
if original_image.size != (450, 450):
    original_image = original_image.resize((450, 450))

# 设置标题栏的高度
title_height = 50  # 你可以根据需要调整这个高度

# 创建一个新的图片，宽度与原图片相同，高度为原图片的高度加上标题栏的高度
new_image = Image.new('RGB', (450, 450 + title_height), 'white')

# 创建ImageDraw对象
draw = ImageDraw.Draw(new_image)

# 设置字体（这里使用默认的字体，你可以替换为其他字体路径）
try:
    # 尝试加载系统字体（例如在Windows上）
    font = ImageFont.truetype("/Users/songyujian/Downloads/Songti.ttc", size=40)
except IOError:
    # 如果上面失败了，使用Pillow的默认字体
    font = ImageFont.load_default()

# 设置文本内容和颜色
text = "输入图像"
text_color = "black"

# 计算文本大小和位置
text_width, text_height = draw.textsize(text, font=font)
text_x = (new_image.width - text_width) / 2  # 居中
text_y = (title_height - text_height) / 2  # 在标题栏垂直居中

# 在标题栏上绘制文本
draw.text((text_x, text_y), text, fill=text_color, font=font)

# 把原始图片粘贴到新图片的下方
new_image.paste(original_image, (0, title_height))

# 保存或显示图片
new_image.save('/Users/songyujian/Downloads/output_3.png')
# 或者
new_image.show()