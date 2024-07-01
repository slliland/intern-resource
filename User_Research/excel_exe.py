import pandas as pd

# # 指定 Excel 文件路径
# excel_file_path = '/Users/songyujian/Downloads/Material Used for AI-Bot/Pratical seeker/CultureBank_Practical Seeker.xlsx'
# # 指定输出 CSV 文件路径
# csv_file_path = '/Users/songyujian/Downloads/CultureBank_Practical Seeker.csv'
#
# # 读取 Excel 文件
# df = pd.read_excel(excel_file_path, header=0)
#
# # 去除全为空的列和行
# df.dropna(axis=1, how='all', inplace=True)  # 去除空列
# df.dropna(axis=0, how='all', inplace=True)  # 去除空行

# # 按照 A 列的值进行分组，并将每个分组的其他列数据合并为一行
# def concat_rows(x):
#     # 将每一行转换为字符串，然后过滤掉 NaN 值，最后使用逗号拼接非 NaN 的值
#     concatenated = x.apply(lambda row: ','.join(row.dropna().astype(str)), axis=1)
#     return ' '.join(concatenated)
#
# # 应用上述函数到每个分组，并重置索引以便后续保存到 CSV
# grouped = df.groupby(df.iloc[:, 0]).apply(concat_rows).reset_index(name='concatenated')
#
# print(grouped)
#
# # 保存结果到 CSV 文件
# grouped.to_csv(csv_file_path, index=False)
# df.to_csv(csv_file_path, index=False)
# print(f'Excel file {excel_file_path} has been converted to {csv_file_path}')


# 指定 CSV 文件路径
csv_file_path = '/Users/songyujian/Downloads/CultureBank_Practical Seeker.csv'

# 读取 CSV 文件
df = pd.read_csv(csv_file_path)

# 假设我们已经知道了列名，并且它们分别是 'Column2' 和 'Column3'
column_2_name = df.columns[1]  # 或者直接使用列名字符串
column_3_name = df.columns[2]  # 或者直接使用列名字符串

# 使用 apply 函数自定义合并逻辑
def custom_merge(row):
    if pd.isna(row[column_3_name]) or row[column_3_name] == '':
        return row[column_2_name]
    else:
        return f"{row[column_2_name]}{row[column_3_name]}"

df['Merged_Column'] = df.apply(custom_merge, axis=1)

# 删除原先的第二和第三列
df.drop([column_2_name, column_3_name], axis=1, inplace=True)

# 保存结果到新的 CSV 文件
output_file_path = '/Users/songyujian/Downloads/Merged_Columns.csv'
df.to_csv(output_file_path, index=False)

print(f'Merged file saved: {output_file_path}')
