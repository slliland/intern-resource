import matplotlib.pyplot as plt
import numpy as np
import imageio
import os


def display_gif_frames_horizontally(gif_images, output_filename, figsize=(20, 20)):
    # 确定所有GIF中帧数最多的帧数
    max_frames = max(len(gif) for gif in gif_images)

    # 创建一个足够大的子图网格
    fig, axes = plt.subplots(len(gif_images), max_frames, figsize=figsize)

    # 如果只有一个GIF，确保axes是二维的
    if len(gif_images) == 1:
        axes = np.expand_dims(axes, axis=0)

    # 遍历每个GIF图像
    for row_idx, gif in enumerate(gif_images):
        # 遍历每一帧
        for col_idx, frame in enumerate(gif):
            # 显示图像
            ax = axes[row_idx, col_idx]
            ax.imshow(frame)
            ax.axis('off')

        # 如果某个GIF的帧数不是最多的，剩余的子图应该关闭
        for col_idx in range(len(gif), max_frames):
            axes[row_idx, col_idx].axis('off')

    # 调整子图之间的间距
    plt.subplots_adjust(wspace=0.05, hspace=0.05)

    # 保存图像到文件
    plt.savefig(output_filename, bbox_inches='tight')

    # 显示图像
    plt.show()


# 你可以在这里指定输出文件的名称和路径
filename = 't3'
output_filename = str('/Users/songyujian/Documents/毕设用图/'+filename+'.png')


# 假设 gif_frames 是一个包含了GIF每帧图像的列表
# display_gif_frames(gif_frames)


# 定义一个函数来读取一个目录下的所有GIF文件
def read_gifs_from_directory(directory):
    gif_files = [f for f in os.listdir(directory) if f.endswith('.gif')]
    gif_images = []
    for gif_file in gif_files:
        gif_path = os.path.join(directory, gif_file)
        gif_images.append(imageio.mimread(gif_path))
    return gif_images

# 使用上面定义的函数来读取GIF文件
# 这里假设你的GIF文件都在'path_to_gif_directory'这个目录下
gif_directory = str('/Users/songyujian/Documents/毕设ppt用图/'+filename)
gif_images = read_gifs_from_directory(gif_directory)

# 确保我们有九个GIF图像，如果不足或过多，需要适当调整
gif_images = gif_images[:9]  # 只取前九个GIF

# 使用之前定义的函数来显示这些GIF图像的帧
display_gif_frames_horizontally(gif_images, output_filename)
