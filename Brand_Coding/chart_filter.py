import pandas as pd

# 统计哪个题号下的回答
selected_header = 'A2_LOCAL BRAND'  # 'A2_LOCAL BRAND', 'A2_W BRAND', 或 'A2_JP BRAND'

# 读取Excel文件
df = pd.read_excel('/Users/songyujian/Downloads/testad.xlsx')

# 获取列名映射到所选题号
columns_mapping = {
    'A2_LOCAL BRAND': df.columns[1:11],  # B-K列
    'A2_W BRAND': df.columns[11:21],  # L-U列
    'A2_JP BRAND': df.columns[21:31]  # V-AE列
}

# 获取所选题号对应的列名
selected_columns = columns_mapping[selected_header]

# 初始化输出DataFrame
output_df = pd.DataFrame(columns=['Respondent.Serial', '题号', '回答品牌序号', '回答品牌'])

# 遍历每一行数据，统计品牌提及情况
for index, row in df.iterrows():
    if index == 0:  # 跳过第一行数据
        continue
    respondent_serial = row.iloc[0]
    mentioned_brands = row[selected_columns].dropna()  # 获取提及的品牌并去除空值

    for col_index, brand in enumerate(mentioned_brands, start=1):  # 使用enumerate从1开始计数获取相对位置（序号）
        if pd.notna(brand):  # 如果该单元格有品牌名字，则创建一个新的DataFrame来存储信息
            new_row = pd.DataFrame({
                'Respondent.Serial': [respondent_serial],
                '题号': [selected_header],
                '回答品牌序号': [col_index],
                '回答品牌': [brand]
            })
            output_df = pd.concat([output_df, new_row], ignore_index=True)

# 输出到新的Excel表格
output_df.to_excel('/Users/songyujian/Downloads/output_brands.xlsx', index=False)