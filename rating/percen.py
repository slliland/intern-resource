import numpy as np

# test_arr = np.array([0, 1, 3, 8, 13, 17, 14, 20, 31, 21, 29, 34, 33, 29, 43])
#
# test_median = np.median(test_arr)
# test_tf = np.percentile(test_arr, 25)
# test_sf = np.percentile(test_arr, 75)
#
# print("%25: ", test_tf, " %50: ", test_median, " %75: ", test_sf)
# import numpy as np
#
# # 假设原始数据数组为 original_data
# original_data = np.array([1143,1000,3533,3488,3353])  # 这里填入您的数据
#
# # 原始数据的最小值和最大值
# a = -5000
# b = 5000
#
# # 新范围的最小值和最大值
# c = 0
# d = 150
#
# # 应用线性映射公式
# mapped_data = c + ((original_data - a) * (d - c) / (b - a))
#
# # 打印映射后的数据
# print(mapped_data)
#
# import numpy as np
#
# def single_value_nonlinear_to_linear_mapping(value, old_min, old_max, new_min, new_max, exponent):
#     # 非线性映射 - 幂律变换
#     value_nonlinear_mapped = np.power(value, exponent)
#     # print(value_nonlinear_mapped)
#     # 线性映射到新的范围
#     nonlinear_min, nonlinear_max = np.power(old_min, exponent), np.power(old_max, exponent)
#     value_linear_mapped = new_min + (new_max - new_min) * (value_nonlinear_mapped - nonlinear_min) / (nonlinear_max - nonlinear_min)
#     return value_linear_mapped
#
# # 预估的原始数据的最小值和最大值
# old_min, old_max = 0, 5500
#
# # 映射到50到150的范围
# new_min, new_max = 0, 150
#
# # 选择一个小于1的指数来增加较大数值之间的差异
# exponent = 0.2  # 开方映射
#
# # 测试
# original_data = np.array([926, 1194, 1252, 1242, 1165, 898])
# for i in original_data:
#     mapped_value = single_value_nonlinear_to_linear_mapping(i, old_min, old_max, new_min, new_max, exponent)
#     print(np.round(mapped_value, 0))
#     # print(mapped_value)


def tanh_stretch(x, stretch_factor=1):
    # 双曲正切函数进行非线性拉伸
    return np.tanh(x * stretch_factor)

def nonlinear_to_linear_mapping(value, old_min, old_max, new_min, new_max, non_linear_func, non_linear_param):
    # 将原始值归一化到[0,1]区间
    normalized_value = (value - old_min) / (old_max - old_min)
    # 应用非线性拉伸函数
    value_nonlinear_mapped = non_linear_func(normalized_value, non_linear_param)
    # 线性映射到新的范围
    value_linear_mapped = new_min + (new_max - new_min) * value_nonlinear_mapped
    return value_linear_mapped

# 估计的数据最小值和最大值
estimated_old_min, estimated_old_max = 0, 3000

# 映射范围
new_min, new_max = 50, 150

# 使用tanh函数拉伸
# 测试数据
original_data = np.array([926, 1194, 1252, 1242, 1165, 898, 2000, 1000, 800, 1200, 3000, 4000, 500])
tanh_mapped_values = []
for i in original_data:
    mapped_value = nonlinear_to_linear_mapping(i, estimated_old_min, estimated_old_max, new_min, new_max, tanh_stretch, 1.5)
    tanh_mapped_values.append(np.round(mapped_value, 0))
print("Tanh mapped values:", tanh_mapped_values)








