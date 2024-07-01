from PIL import Image, ImageDraw, ImageFont

def generate_positions_list(number_of_images=6, new_size=(360, 360)):
    # 六张图片的初始位置
    initial_positions = [
        (0, 0), (new_size[0], 0),  # 第一行两张图片的位置
        (0, new_size[1]), (new_size[0], new_size[1]),  # 第二行两张图片的位置
        (0, 2 * new_size[1]), (new_size[0], 2 * new_size[1])  # 第三行两张图片的位置
    ]

    positions_list = [initial_positions]  # 将初始配置加入列表

    for i in range(1, number_of_images):
        # 每次循环都基于初始位置创建新的排列
        new_positions = initial_positions[-i:] + initial_positions[:-i]
        positions_list.append(new_positions)

    return positions_list


# positions_list = generate_positions_list()
# for i, positions in enumerate(positions_list):
#     print(f"Positions for iteration {i+1}: {positions}")

def add_text_to_image(image, text, font_path, font_size=30):
    # 创建一个可以在上面绘制文本的ImageDraw对象
    draw = ImageDraw.Draw(image)

    # 加载一个TrueType或OpenType字体文件，并创建一个字体对象
    font = ImageFont.truetype(font_path, font_size)

    # 使用textbbox获取文本大小
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # 计算文本位置（水平居中，底部）
    text_x = (image.width - text_width) / 2
    text_y = image.height - text_height - 10  # 留出一定间隔

    # 在指定位置添加文本
    draw.text((text_x, text_y), text, font=font, fill="black")

    return image


def create_collage(images_paths, texts, positions, output_path, new_size=(360, 360)):
    # 创建一个新的图像，大小是两张新尺寸图片宽度和三张新尺寸图片高度
    collage_width = 2 * new_size[0]
    collage_height = 3 * new_size[1]
    collage = Image.new('RGB', (collage_width, collage_height), "white")  # 背景设置为黑色

    # 字体路径
    font_path = "/Users/songyujian/Library/Fonts/SimHei.ttf"

    # 读取图片，裁剪并拼接到指定位置，并添加文字
    for image_path, position, text in zip(images_paths, positions, texts):
        img = Image.open(image_path)
        img = img.resize(new_size, Image.LANCZOS)

        img_with_text = add_text_to_image(img, text, font_path=font_path)

        # 拼接图片到指定位置
        collage.paste(img_with_text, position)

    # 保存拼接后的图片
    collage.save(output_path)


# 图片路径列表
images_paths = [
    '/Users/songyujian/Downloads/1.jpg',
    '/Users/songyujian/Downloads/2.JPG',
    '/Users/songyujian/Downloads/3.jpg',
    '/Users/songyujian/Downloads/4.jpg',
    '/Users/songyujian/Downloads/5.jpg',
    '/Users/songyujian/Downloads/6.jpg'
]

texts = [
    '14.5元/100g',
    '22.1元/100g',
    '11.9元/100g',
    '11.8元/100g',
    '16.9元/100g',
    '13.9元/100g'
]


new_image_size = (360, 360)

# 根据新尺寸生成六种组合方式
positions_list = generate_positions_list(number_of_images=6, new_size=new_image_size)

# 对每种组合方式进行操作
for i, positions in enumerate(positions_list, start=1):
    output_path = f'/Users/songyujian/Downloads/牙膏包装2_{i}.jpg'
    create_collage(images_paths, texts, positions, output_path)

print("All collages created.")
