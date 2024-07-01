import pandas as pd

# 定义文件路径
input_file_path = '/Users/songyujian/Downloads/Raw data_品牌开放题_第一批 0529v3【Hair+Female skincare+Perfume】.xlsx'
output_file_path = '/Users/songyujian/Downloads/Processed_Brand_List.xlsx'

# 读取Excel文件中指定的sheet
df = pd.read_excel(input_file_path, sheet_name='MEN')

# 获取B列和E列的内容
b_column = df.iloc[:, 0]  # 假设B列是第二列
e_column = df.iloc[:, 1]  # 假设E列是第五列

# 创建一个新列表用于存储拼接后的结果
combined_results = []

# 遍历DataFrame中的每一行
for index, row in df.iterrows():
    b_data = row[b_column.name]
    e_data = row[e_column.name]

    # 检查两个单元格是否都非空
    if pd.notna(b_data) and pd.notna(e_data):
        combined_results.append(f"{b_data}|{e_data}")
    elif pd.notna(b_data):
        combined_results.append(f"{b_data}")
    elif pd.notna(e_data):
        combined_results.append(f"{e_data}")
    # 如果两个单元格都是空的，则不做任何操作（即跳过这一行）

# 将结果保存到新的DataFrame中
result_df = pd.DataFrame(combined_results, columns=['Combined'])

# 将结果写入新的Excel文件中
result_df.to_excel(output_file_path, index=False)

print('The data has been processed and saved to', output_file_path)
