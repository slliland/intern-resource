import numpy as np
import pandas as pd
from matplotlib import font_manager
import matplotlib.pyplot as plt

# 读取Excel文件
df = pd.read_excel('/Users/songyujian/Downloads/Book2.xlsx')

# 筛选出project_id特定值的行
df_16942 = df[df['project_id'] == 16942]
df_16949 = df[df['project_id'] == 16949]
df_16950 = df[df['project_id'] == 16950]

# 选择数据
column_data_16942 = df_16942['开放题得分']
column_data_16949 = df_16949['开放题得分']
column_data_16950 = df_16950['开放题得分']

# 将pandas序列转换为numpy数组，并确保数据类型为整数
array_16942 = column_data_16942.to_numpy().astype(int)
array_16949 = column_data_16949.to_numpy().astype(int)
array_16950 = column_data_16950.to_numpy().astype(int)
print("16942原始总分:", np.sum(array_16942))
print("16949原始总分:", np.sum(array_16949))
print("16950原始总分:", np.sum(array_16950))

def standardize(array):
    # 首先将数据标准化到均值为0，标准差为1
    array_standardized = (array - np.mean(array)) / np.std(array)
    # 使用tanh函数进行非线性变换
    array_tanh = np.tanh(array_standardized)
    # 将tanh的输出范围从(-1, 1)变换到(0, 2)
    array_scaled = (array_tanh + 1) * (2 / (1 + 1))
    # 确保数据类型为浮点数
    array_scaled = array_scaled.astype(float)
    # 计算映射后的总分
    total_score_tanh = np.sum(array_scaled)

    return array_scaled, total_score_tanh


data_16942, total_16942 = standardize(array_16942)
data_16949, total_16949 = standardize(array_16949)
data_16950, total_16950 = standardize(array_16950)

# 打印映射后的总分
print("16942映射后总分:", total_16942)
print("16949映射后总分:", total_16949)
print("16950映射后总分:", total_16950)

# 设置中文字体
font_path = "/System/Library/Fonts/PingFang.ttc"
my_font = font_manager.FontProperties(fname=font_path)


# 修改绘制散点图函数，添加字体设置
def plot_scatter(data, title):
    plt.figure(figsize=(10, 5))
    plt.scatter(range(len(data)), data)
    plt.title(title, fontproperties=my_font)
    plt.xlabel('样本索引', fontproperties=my_font)
    plt.ylabel('分数', fontproperties=my_font)
    plt.ylim(0, 2)  # 固定Y轴的数据范围
    plt.show()


# 绘制评分散点图
plot_scatter(data_16942, '16942映射后的评分散点图')
plot_scatter(data_16949, '16949映射后的评分散点图')
plot_scatter(data_16950, '16950映射后的评分散点图')

# 绘制总分柱状图
def plot_total_scores_bar(total_scores, labels):
    plt.figure(figsize=(8, 5))
    plt.bar(labels, total_scores, color=['blue', 'green', 'red'])
    plt.title('总分比较', fontproperties=my_font)
    plt.xlabel('Project ID', fontproperties=my_font)
    plt.ylabel('映射后总分', fontproperties=my_font)
    plt.show()

# 调用函数绘制总分柱状图
total_scores = [total_16942, total_16949, total_16950]
project_ids = ['16942', '16949', '16950']
plot_total_scores_bar(total_scores, project_ids)

# 绘制每条数据评分对比图
def plot_score_comparison(data_arrays, labels):
    plt.figure(figsize=(10, 5))
    for i, data in enumerate(data_arrays):
        plt.scatter(range(len(data)), data, label=labels[i])
    plt.title('评分对比', fontproperties=my_font)
    plt.xlabel('样本索引', fontproperties=my_font)
    plt.ylabel('分数', fontproperties=my_font)
    plt.legend(prop=my_font)
    plt.ylim(0, 2)  # 固定Y轴的数据范围
    plt.show()

# 调用函数绘制每条数据评分对比图
data_arrays = [data_16942, data_16949, data_16950]
plot_score_comparison(data_arrays, project_ids)


