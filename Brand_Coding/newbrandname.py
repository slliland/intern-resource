import pandas as pd

# 定义文件路径
file_path = '/Users/songyujian/Downloads/【AI coding结果_反馈0607】Raw data_品牌开放题_第一批 0605【skincare+makeup+perfume+hair】.xlsx'

# 读取两个工作表
matched_df = pd.read_excel(file_path, sheet_name='匹配结果表')
unmatched_df = pd.read_excel(file_path, sheet_name='未匹配结果去重表', skiprows=2)  # 跳过前两行

# 准备收集数据的列表
results = []

# 遍历未匹配结果去重表
for index, row in unmatched_df.iterrows():
    category = row[0]  # 第一列 - Category
    brand_standard_name = row[1]  # 第二列 - Brand Standard Name

    # 在匹配结果表中查找相同的 Category 和 Brand Standard Name
    matched_rows = matched_df[
        (matched_df['Category'] == category) &
        (matched_df['品牌标准名称'] == brand_standard_name)
        ]

    # 收集所有回答品牌并用 '|' 连接
    answer_brands = '|'.join(matched_rows['回答品牌'].dropna().unique())

    # 收集所有 Respondent.Serial 并用 '|' 连接
    respondent_serials = '|'.join(matched_rows['Respondent.Serial'].astype(str).dropna().unique())

    # 将每行数据作为字典添加到结果列表中
    results.append({
        'Category': category,
        'Brand Standard Name': brand_standard_name,
        'Respondent.Serial': respondent_serials,
        'Answer Brands': answer_brands
    })

# 将结果列表转换为 DataFrame
result_df = pd.DataFrame(results)

# 输出到新的 Excel 文件中
output_file_path = '/Users/songyujian/Downloads/newmatched_results.xlsx'
result_df.to_excel(output_file_path, index=False)
