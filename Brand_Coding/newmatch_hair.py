import pandas as pd

# 读取 Excel 文件
df1 = pd.read_excel('/Users/songyujian/Downloads/new_brandlist.xlsx', sheet_name='skincare')
df2 = pd.read_excel('/Users/songyujian/Downloads/skincaretest.xlsx')

# 对 df2 进行迭代
for index, row in df2.iterrows():
    label = row['label']  # 假设第一列为 'label'
    code = row['coding']  # 假设第二列为 'coding'

    # 检查 label 是否存在于 df1 的 'label' 列中
    match_indices = df1[df1['label'] == label].index

    if not match_indices.empty:
        # 如果找到匹配，在 df1 的 'coding' 列中更新或添加 code 值
        for i in match_indices:
            existing_code = df1.at[i, 'coding']
            if pd.isnull(existing_code):
                df1.at[i, 'coding'] = code
            else:
                df1.at[i, 'coding'] += '|' + code
    else:
        # 如果没有找到匹配，创建新行并加入到 df1 中
        new_row_data = {column: None for column in df1.columns}
        new_row_data['label'] = label
        new_row_data['coding'] = code
        new_row = pd.DataFrame([new_row_data])
        # 使用 concat 方法来添加新行
        df1 = pd.concat([df1, new_row], ignore_index=True)

# 将更新后的 DataFrame 保存回 Excel 文件
df1.to_excel('/Users/songyujian/Downloads/skincare_test_updated.xlsx', index=False)
