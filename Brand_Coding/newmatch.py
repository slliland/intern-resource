import pandas as pd
import re


"""
使用方法：
1、修改文件路径
2、根据所处理的产品类别，使用匹配该类别的部分代码，注释掉处理其他类别的代码
3、在test_path中查看匹配结果
"""

"""
文件路径选择部分
"""
# 定义文件路径
# 替换为要进行coding的某类别产品文件路径（格式：第一列为某类别产品反馈；第二列为某类别产品的品牌标准名称/用户回答），也可修改代码，改为指定反馈表格中的某行某列
target_type_path = '/Users/songyujian/Downloads/brandcoding_tmp/tmp_brandlist/raw_brandlist.xlsx'
# 替换为brandlist表格路径
raw_data_path = '/Users/songyujian/Downloads/new_brandlist.xlsx'
# 输出的匹配结果路径（避免直接修改原始brandlist，暂存中间文件）
test_path = '/Users/songyujian/Downloads/men_test.xlsx'

# 加载数据：修改sheetname为你要处理的产品类别（如skincare、hair等）
target_type_df = pd.read_excel(target_type_path, sheet_name='men')
raw_data_df = pd.read_excel(raw_data_path, sheet_name='men')

"""
skincare、makeup表匹配：此时以label作为匹配标准
"""
# # 遍历数据
# for index, row in target_type_df.iterrows():
#     first_col_value = row[0]
#     second_col_value = row[1]
#
#     # 查找匹配项
#     match = raw_data_df[raw_data_df.iloc[:, 0] == first_col_value]
#
#     if not match.empty:
#         # 如果存在匹配项，检查第四列值
#         fourth_col_values = match.iloc[0, 3].split('|')
#
#         # 确保 second_col_value 是字符串
#         second_col_str = str(second_col_value)
#
#         if second_col_str not in fourth_col_values:
#             # 如果第二列值不在里面，则添加进去
#             new_fourth_col_value = match.iloc[0, 3] + '|' + second_col_str
#             raw_data_df.at[match.index[0], raw_data_df.columns[3]] = new_fourth_col_value
#     else:
#         # 创建一个与原始 DataFrame 列数相同的空列表
#         new_row_values = [None] * len(raw_data_df.columns)
#         # 根据原始 DataFrame 的结构设置第一列和第四列的值
#         new_row_values[0] = first_col_value  # 假设第一列是要匹配的值
#         new_row_values[3] = second_col_value  # 假设第四列是要更新的值
#
#         # 创建新行 DataFrame 并且指定其列名
#         new_row = pd.DataFrame([new_row_values], columns=raw_data_df.columns)
#
#         # 使用 pd.concat() 合并原始 DataFrame 和新行 DataFrame
#         raw_data_df = pd.concat([raw_data_df, new_row], ignore_index=True)

"""
perfume列表匹配：此时以code作为匹配标准
"""
# 遍历数据
# for index, row in target_type_df.iterrows():
#     first_col_value = row[0]
#     second_col_value = row[1]
#
#     # 查找匹配项
#     match = raw_data_df[raw_data_df.iloc[:, 1] == first_col_value]
#
#     if not match.empty:
#         # 如果存在匹配项，检查第四列值
#         fourth_col_values = match.iloc[0, 3].split('|')
#
#         # 确保 second_col_value 是字符串
#         second_col_str = str(second_col_value)
#
#         if second_col_str not in fourth_col_values:
#             # 如果第二列值不在里面，则添加进去
#             new_fourth_col_value = match.iloc[0, 3] + '|' + second_col_str
#             raw_data_df.at[match.index[0], raw_data_df.columns[3]] = new_fourth_col_value
#     else:
#         # 创建一个与原始 DataFrame 列数相同的空列表
#         new_row_values = [None] * len(raw_data_df.columns)
#         # 根据原始 DataFrame 的结构设置第二列和第四列的值
#         new_row_values[1] = first_col_value  # 假设第二列是要匹配的值
#         new_row_values[3] = second_col_value  # 假设第四列是要更新的值
#
#         # 创建新行 DataFrame 并且指定其列名
#         new_row = pd.DataFrame([new_row_values], columns=raw_data_df.columns)
#
#         # 使用 pd.concat() 合并原始 DataFrame 和新行 DataFrame
#         raw_data_df = pd.concat([raw_data_df, new_row], ignore_index=True)

"""
hair表的特殊处理
"""
# def split_values(value):
#     # 使用正则表达式来拆分含有中文顿号、|符号、逗号等的字符串
#     if pd.notnull(value):
#         return re.split('[、|,]', value)
#     else:
#         return []
#
#
# # 在 add_invalid_row 函数中
# def add_invalid_row(df, invalid_value):
#     # 查找是否已经存在一个标记为“无效”的行
#     df_invalid_row = df[df.iloc[:, 0] == '无效']
#
#     if not df_invalid_row.empty:
#         # 如果存在，则更新该行的第四列值
#         current_value = df_invalid_row.iloc[0, 3]
#         current_value = '' if pd.isnull(current_value) else current_value
#         new_fourth_col_value = current_value + '|' + invalid_value if current_value else invalid_value
#         df.at[df_invalid_row.index[0], df.columns[3]] = new_fourth_col_value
#     else:
#         # 如果不存在，则创建一个新行，并将其添加到 DataFrame 中
#         # 确保提供与 df.columns 相同数量的元素
#         new_row_values = ['无效'] + [None] * (len(df.columns) - 2) + [invalid_value]
#         new_row = pd.DataFrame([new_row_values], columns=df.columns)
#         df = pd.concat([df, new_row], ignore_index=True)
#
#     return df
#
#
#
#
# # 修改 process_matching 函数以正确处理有效内容
# def process_matching(df, first_col_value, second_col_value):
#     # 如果标记为“有效”，则进行匹配检查
#     if first_col_value == '有效':
#         # 将字符串转换为列表，以便可以迭代每个可能的值
#         second_col_values = split_values(second_col_value)
#
#         for value in second_col_values:
#             # 检查是否有匹配项
#             match = df[df.iloc[:, 0] == value]
#
#             if not match.empty:
#                 # 匹配成功，更新第四列
#                 current_value = match.iloc[0, 3]
#                 current_value = '' if pd.isnull(current_value) else current_value
#                 fourth_col_values = current_value.split('|') if current_value else []
#                 if pd.notnull(match.iloc[0, 3]):
#                     fourth_col_values = match.iloc[0, 3].split('|')
#                 else:
#                     fourth_col_values = []
#
#                 if value not in fourth_col_values:
#                     new_fourth_col_value = value if not fourth_col_values else match.iloc[0, 3] + '|' + value
#                     df.at[match.index[0], df.columns[3]] = new_fourth_col_value
#             else:
#                 # 匹配失败，创建新行并复制到第一列和第四列
#                 new_row_values = [value] + [None] * (len(df.columns) - 2) + [value]
#                 new_row = pd.DataFrame([new_row_values], columns=df.columns)
#                 df = pd.concat([df, new_row], ignore_index=True)
#
#     elif first_col_value == '无效':
#         # 对于“无效”，调用 add_invalid_row 函数处理
#         df = add_invalid_row(df, second_col_value)
#     else:
#         # 如果既不是“有效”也不是“无效”
#         match = df[df.iloc[:, 0] == first_col_value]
#
#         if not match.empty and pd.notnull(match.iloc[0, 3]):
#             fourth_col_values = match.iloc[0, 3].split('|')
#
#             if second_col_value not in fourth_col_values:
#                 new_fourth_col_value = str(second_col_value) if not fourth_col_values else match.iloc[0, 3] + '|' + str(
#                     second_col_value)
#                 df.at[match.index[0], df.columns[3]] = new_fourth_col_value
#         else:
#             new_row_values = [first_col_value] + [None] * (len(df.columns) - 2) + [second_col_value]
#             new_row = pd.DataFrame([new_row_values], columns=df.columns)
#             df = pd.concat([df, new_row], ignore_index=True)
#
#     return df
#
#
# # 遍历数据
# for index, row in target_type_df.iterrows():
#     first_col_values = []
#     second_col_value = row[1]
#
#     # 规则 1 和规则 2 的处理
#     if '有效：“' in row[0] or '在品牌列表中：' in row[0]:
#         # 提取引号之间的内容但不包含引号本身和“或”字符
#         extracted_value = re.search('“([^”]*)”|：([^；]*)', row[0])
#         if extracted_value:
#             # 确保从正确的捕获组提取内容
#             matched_group = extracted_value.group(1) if extracted_value.group(1) else extracted_value.group(2)
#             # 移除可能存在的“或”字符并拆分
#             clean_values = [val.strip('“”') for val in split_values(matched_group) if '或' not in val]
#             first_col_values.extend(clean_values)
#
#     # 规则 3 的处理
#     elif '无效' in row[0] or '有效' in row[0]:
#         invalid_match = re.search('“([^”]*)”无效', row[0])
#         valid_match = re.search('“([^”]*)”有效', row[0])
#
#         if invalid_match:
#             # 添加无效行到 raw_data_df
#             invalid_value = invalid_match.group(1).strip('“”')
#             raw_data_df = add_invalid_row(raw_data_df, invalid_value)
#
#         if valid_match:
#             valid_value = valid_match.group(1).strip('“”')
#             first_col_values.extend(split_values(valid_value))
#
#     # 如果没有特殊规则，则直接将值添加到列表中
#     if not first_col_values:
#         first_col_values.append(row[0])
#
#     for value in first_col_values:
#         raw_data_df = process_matching(raw_data_df, value, second_col_value)

"""
men列表特殊处理
"""
# 遍历 target_type_df 数据
for outer_index, row in target_type_df.iterrows():
    first_col_value = str(row[0])
    second_col_value = str(row[1])

    matched_in_raw_data = False  # 标记是否在 raw_data_df 中找到匹配

    # 检查是否包含关键字"有效"
    if "有效" in first_col_value:
        # 正则匹配“”内的内容
        valid_content = re.findall(r'[“"”](.*?)["“”]', first_col_value)
        if valid_content:
            # 拆分并遍历结果
            for content in valid_content[0].split('|'):
                escaped_content = re.escape(content)
                pattern = rf'\b{escaped_content}\b'  # 使用单词边界确保完整匹配
                # 遍历 raw_data_df 的第四列进行匹配
                for inner_index, raw_row in raw_data_df.iterrows():
                    fourth_col_values = str(raw_row[3]).split('|')
                    if any(re.fullmatch(pattern, val) for val in fourth_col_values):
                        matched_in_raw_data = True  # 找到匹配，更新标记
                        # 如果找到匹配，则附加 target_type_df 第二列的值
                        new_values = '|'.join(filter(None, [raw_row[3], second_col_value]))
                        raw_data_df.at[inner_index, raw_data_df.columns[3]] = new_values

            if not matched_in_raw_data:
                # 如果没有找到匹配项，则在 raw_data_df 中添加新行
                new_index = len(raw_data_df)
                raw_data_df.loc[new_index, raw_data_df.columns[0]] = second_col_value
                raw_data_df.loc[new_index, raw_data_df.columns[3]] = '|'.join(valid_content[0].split('|'))

    # 检查是否包含关键字"在品牌列表中"
    elif "在品牌列表中" in first_col_value:
        # 提取数字
        numbers = re.findall(r'\d+', first_col_value)
        for number in numbers:
            matches = raw_data_df[raw_data_df.iloc[:, 1].astype(str).str.contains(r'\b' + number + r'\b', na=False)]
            for match_index in matches.index:
                # 如果找到匹配，则附加 target_type_df 第二列的值，同时确保不重复添加相同值
                existing_values = str(raw_data_df.at[match_index, raw_data_df.columns[3]])
                if second_col_value not in existing_values.split('|'):
                    new_values = '|'.join(filter(None, [existing_values, second_col_value]))
                    raw_data_df.at[match_index, raw_data_df.columns[3]] = new_values

    # 检查是否为"无效回答"
    elif "无效回答" == first_col_value:
        invalid_matches = raw_data_df[raw_data_df.iloc[:, 0] == "无效回答"]
        for match_index in invalid_matches.index:
            existing_values = str(raw_data_df.at[match_index, raw_data_df.columns[3]])
            if second_col_value not in existing_values.split('|'):
                new_values = '|'.join(filter(None, [existing_values, second_col_value]))
                raw_data_df.at[match_index, raw_data_df.columns[3]] = new_values

# 将更新后的 DataFrame 写回 Excel 文件
raw_data_df.to_excel(test_path, index=False)
