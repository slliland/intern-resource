from PIL import Image

def crop_and_concatenate_images(image_path1, image_path2, output_path, output_size):
    # 打开两张图片
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    # 裁剪图片：上35px，下左右各45px
    crop_box = (45, 37, image1.width - 45, image1.height - 45)
    image1_cropped = image1.crop(crop_box)
    image2_cropped = image2.crop(crop_box)

    # 确定新图片的宽度和高度
    new_width = image1_cropped.width + image2_cropped.width
    new_height = max(image1_cropped.height, image2_cropped.height)

    # 创建新图片并粘贴裁剪后的原有图片，背景设为白色
    new_image = Image.new('RGB', (new_width, new_height), 'white')
    new_image.paste(image1_cropped, (0, 0))
    new_image.paste(image2_cropped, (image1_cropped.width, 0))

    # 调整图片大小到指定尺寸（例如：500x417）
    new_image_resized = new_image.resize(output_size)

    # 保存新图片
    new_image_resized.save(output_path)

# 图片路径
image_path_1 = '/Users/songyujian/Downloads/20240621-111013.jpeg'
image_path_2 = '/Users/songyujian/Downloads/20240621-111016.jpeg'
output_image_path = '/Users/songyujian/Downloads/combined_image2.jpeg'

# 拼接、调整大小并保存图片
crop_and_concatenate_images(image_path_1, image_path_2, output_image_path, (500, 417))