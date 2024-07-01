# import pandas as pd
# import re
#
# # 定义文件路径
# new_brandlist_path = '/Users/songyujian/Downloads/new_brandlist.xlsx'
# output_path = '/Users/songyujian/Downloads/processed_brandlist.xlsx'
#
# # 读取工作表
# brandlist_df = pd.read_excel(new_brandlist_path, sheet_name='men')
#
# # 处理第一列的函数
# def process_first_column(value):
#     if pd.isnull(value):  # 检查是否为空值，如果为空则直接返回
#         return value
#     # 将 '/' 替换为 '|'
#     value = value.replace('/', '|')
#     # 在中文和英文之间插入 '|'
#     value = re.sub(r'([a-zA-Z])([\u4e00-\u9fa5])', r'\1|\2', value)
#     value = re.sub(r'([\u4e00-\u9fa5])([a-zA-Z])', r'\1|\2', value)
#     return value
#
# # 对整个第一列应用处理函数
# brandlist_df.iloc[:, 0] = brandlist_df.iloc[:, 0].apply(process_first_column)
#
# # 拼接处理后的第一列和原始第四列的值，并更新第四列
# brandlist_df.iloc[:, 3] = brandlist_df.apply(
#     lambda row: f"{row.iloc[0]}|{row.iloc[3]}" if pd.notnull(row.iloc[3]) else row.iloc[0],
#     axis=1
# )
#
# # 将处理后的 DataFrame 写入新的 Excel 文件中
# brandlist_df.to_excel(output_path, sheet_name='men', index=False)
import pandas as pd
import re

# 定义文件路径
processed_brandlist_path = '/Users/songyujian/Downloads/processed_brandlist.xlsx'
output_path = '/Users/songyujian/Downloads/final_brandlist.xlsx'

# 读取工作表
brandlist_df = pd.read_excel(processed_brandlist_path)  # 确保使用正确的 sheet 名称

# 添加后缀的函数
def add_suffixes(segment):
    new_segments = []
    for seg in segment.split('|'):
        # 检查是否为纯汉字
        if re.fullmatch(r'[\u4e00-\u9fa5]+', seg):
            new_segments.append(seg + '男士')
        # 如果没有汉字，则添加 ' man'
        elif not re.search(r'[\u4e00-\u9fa5]', seg):
            new_segments.append(seg + ' man')
        else:
            new_segments.append(seg)  # 如果既包含汉字也包含其他字符，则保持不变
    return '|'.join(new_segments)

# 处理第四列，保留原始值并添加新的文本
def process_fourth_column(row):
    original_text = row.iloc[3] if pd.notnull(row.iloc[3]) else ""
    processed_text = add_suffixes(str(row.iloc[0]))
    # 如果原始第四列有值，则在其后面添加处理过的新文本，否则只返回处理过的新文本
    return f"{original_text}|{processed_text}" if original_text else processed_text

# 应用处理函数到 DataFrame 的每一行，并更新第四列
brandlist_df.iloc[:, 3] = brandlist_df.apply(process_fourth_column, axis=1)

# 将处理后的 DataFrame 写入新的 Excel 文件中
brandlist_df.to_excel(output_path, sheet_name='Sheet1', index=False)