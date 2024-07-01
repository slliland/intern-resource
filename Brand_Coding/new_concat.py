import pandas as pd
import re
"""
【AI coding 结果】添加到 brandlist 列表
"""
#
# # 定义文件路径和工作表名称
# file_path = '/Users/songyujian/Downloads/mybrandlist.xlsx'
# sheet_name = 'perfume'
#
# # 读取 Excel 文件
# df = pd.read_excel(file_path, sheet_name=sheet_name)
#
# # 处理 label 列，并将结果存储到 coding 列
# # 只在第一个空格后面加上 '|'
# df['coding'] = df['label'].apply(lambda x: x.replace(' ', '|', 1) if pd.notnull(x) else x)
#
# # 将更改保存回 Excel 文件
# df.to_excel('/Users/songyujian/Downloads/newbrand.xlsx', sheet_name=sheet_name, index=False)

# 加载Excel文件
file_path = '/Users/songyujian/Downloads/【AI coding结果】Raw data_品牌开放题_第二批0619【perfume+men+skincare+hair】 反馈0628.xlsx'
sheet_name = 'SKINCARE brand list 更新'

# 读取特定Sheet中的数据
df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=2)


def transform_label(label):
    # 确保label是字符串
    if not isinstance(label, str):
        return label  # 如果不是字符串，可能是NaN或其他数据类型，直接返回原值

    # 替换斜杠 '/' 为竖线 '|'
    label = label.replace('/', '|')

    # 使用正则表达式找到所有的中文字符
    chinese_parts = re.findall(r'[\u4e00-\u9fff]+', label)

    # 使用正则表达式找到所有英文单词（包括连续单词和特殊字符）
    english_parts = re.findall(r'[A-Za-z\'’]+(?:\s+[A-Za-z\'’]+)*', label)

    # 分别合并中文和英文部分
    chinese_combined = '|'.join(chinese_parts)
    english_combined = ' '.join(english_parts)

    # 构建新标签
    new_label_parts = []

    if chinese_combined:
        new_label_parts.append(chinese_combined)

    if english_combined:
        new_label_parts.append(english_combined)

    new_label = '|'.join(new_label_parts)

    return new_label


# 应用转换函数到Brand label列，并创建新的coding列
df['coding'] = df['Brand label'].apply(transform_label)

# 创建新DataFrame以匹配新格式
new_df = df.rename(columns={'Brand label': 'label', 'B3 code': 'code', 'Price Tier NET': 'segment'})

# 重新排列列顺序
new_df = new_df[['label', 'code', 'segment', 'coding']]

# 写入新的Excel文件
output_file_path = '/Users/songyujian/Downloads/temp_skincare.xlsx'
new_df.to_excel(output_file_path, index=False)

print("The transformation has been completed and the file has been saved to:", output_file_path)