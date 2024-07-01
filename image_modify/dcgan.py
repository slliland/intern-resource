import os
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import skimage.transform
import imageio

# 获取所有图片路径
datas = glob(os.path.join('/Users/songyujian/Downloads/img_align_celeba/', '*.jpg'))
output_directory = '/Users/songyujian/Downloads/mypretrain_data'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 显示图像的函数
def display_images(dataset, figsize=(4, 4), denomalize=True):
    fig, axes = plt.subplots(3, 3, sharex=True, sharey=True, figsize=figsize)
    for ii, ax in enumerate(axes.flatten()):
        img = dataset[ii, :, :, :]
        if denomalize:
            img = ((img + 1) * 255 / 2).astype(np.uint8)  # Scale back to 0-255
        ax.imshow(img)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()

# 图像读取和预处理函数
def get_image(image_path, image_size, is_crop=True):
    return transform(imageio.imread(image_path).astype(np.float32), image_size, is_crop)

def transform(image, npx=64, is_crop=True):
    if is_crop:
        cropped_image = center_crop(image, npx)
    else:
        cropped_image = image
    return np.array(cropped_image) / 127.5 - 1.

def center_crop(x, crop_h, crop_w=None, resize_w=64):
    if crop_w is None:
        crop_w = crop_h
    h, w = x.shape[:2]
    j = int(round((h - crop_h) / 2.))
    i = int(round((w - crop_w) / 2.))
    return skimage.transform.resize(x[j:j+crop_h, i:i+crop_w], [resize_w, resize_w], anti_aliasing=True)

# 将图像转换为低分辨率
def convert_to_lower_resolution():
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
#     images = glob(os.path.join('/kaggle/working/cars_train/cars_train/', '*.jpg'))
    i = 0
    size = (64, 64)
    for image in datas:
        im = Image.open(image)
        im_resized = im.resize(size, Image.ANTIALIAS)
        im_resized.save(f"/Users/songyujian/Downloads/mypretrain_data/{i}.jpg")
        i += 1

# 验证单个图像的预处理
image_path = datas[0]  # 选择第一张图像
preprocessed_image = get_image(image_path, 64)  # 应用预处理
plt.imshow((preprocessed_image + 1) / 2)  # 将图像数据范围从[-1,1]转换回[0,1]以显示
plt.title("Preprocessed Image")
plt.axis('off')
plt.show()

# 批量处理和显示
test_images = np.array([get_image(path, 64) for path in datas[:9]])  # 处理9张图像
display_images(test_images)  # 显示这些图像

# 转换为低分辨率并检查结果
convert_to_lower_resolution()

# 检查低分辨率图像是否已保存
if not os.path.exists(output_directory):
    print("输出路径不存在，请检查路径。")
else:
    print("输出路径存在。")
    low_res_images = glob(os.path.join(output_directory, '*.jpg'))
    print(f"找到了 {len(low_res_images)} 张低分辨率图像。")

    # 显示一些低分辨率图像
    for image_path in low_res_images[:9]:
        img = Image.open(image_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()