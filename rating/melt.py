import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

num_iterations = 10000  # 指定的次数

all_scores = []  # 存储所有的分数

for _ in range(num_iterations):
    test_arr = np.random.randint(0, 150, size=15)
    np.random.shuffle(test_arr)
    test_arr.sort()

    test_median = np.median(test_arr)
    test_tf = np.percentile(test_arr, 25)
    test_sf = np.percentile(test_arr, 75)

    z, o, t, th = 0, 0, 0, 0

    for i in test_arr:
        if i <= test_tf:
            z += 1
        elif test_tf < i <= test_median:
            o += 1
        elif test_median < i <= test_sf:
            t += 1
        else:
            th += 1

    mean = (150 - (-50)) / 2 + (-20)  # 区间中点
    std_dev = (150 - mean) / 3  # 假设约有99.7%的数据应该落在-20到150之间
    size = 15

    # 使用numpy生成正态分布的随机数
    random_normal_array = np.random.normal(mean, std_dev, size)

    # 将生成的数值四舍五入并转换为整数
    random_integer_array = np.round(random_normal_array).astype(int)

    score = 0
    for j in range(15):
        if j < z:
            score += random_integer_array[j] * 0
        elif z <= j < o:
            score += random_integer_array[j] * 1
        elif o <= j < t:
            score += random_integer_array[j] * 2
        else:
            score += random_integer_array[j] * 3

    # # 假设共有150条用户评论
    # score = score/150
    all_scores.append(score)

# 统计得分出现的次数
score_counter = Counter(all_scores)

# 计算统计特征
min_score = min(all_scores)
max_score = max(all_scores)
median_score = np.median(all_scores)
std_score = np.std(all_scores)
mean_score = np.mean(all_scores)

# 可视化分数分布
plt.figure(figsize=(10, 6))

# 直方图
plt.subplot(1, 2, 1)
plt.hist(all_scores, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Histogram of Scores')
plt.xlabel('Score')
plt.ylabel('Frequency')

# 盒图
plt.subplot(1, 2, 2)
plt.boxplot(all_scores)
plt.title('Boxplot of Scores')
plt.ylabel('Score')

plt.tight_layout()
plt.show()

# 输出统计特征
print("Statistics of Scores:")
print(f"Minimum Score: {min_score}")
print(f"Maximum Score: {max_score}")
print(f"Median Score: {median_score}")
print(f"Standard Deviation Score: {std_score}")
print(f"Mean Score: {mean_score}")