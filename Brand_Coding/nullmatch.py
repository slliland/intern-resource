import pandas as pd

# 定义文件路径
matched_results_path = '/Users/songyujian/Downloads/matched_results.xlsx'
new_brandlist_path = '/Users/songyujian/Downloads/new_brandlist copy.xlsx'

# 读取两个工作表
matched_df = pd.read_excel(matched_results_path, sheet_name='skincare')
brandlist_df = pd.read_excel(new_brandlist_path, sheet_name='skincare')

# 创建一个映射字典，键为 Brand Standard Name 去除空格并转换为小写，值为对应的 Answer Brands
brand_to_answers = pd.Series(
    matched_df['Answer Brands'].values,
    index=matched_df['Brand Standard Name'].str.replace(' ', '').str.lower()
).to_dict()


# 更新 brandlist_df 的 'coding' 列
def update_coding(label, existing_coding):
    # 将 label 转换为小写并去除空格，用于匹配
    modified_label = label.replace(' ', '').lower()

    # 如果找到匹配且已有 coding 值，则在前面加上 '|'
    if modified_label in brand_to_answers and brand_to_answers[modified_label]:
        answer_brands = brand_to_answers[modified_label]
        return f"{existing_coding}|{answer_brands}" if existing_coding else answer_brands
    else:
        # 如果没有找到匹配或 Answer Brands 为空，则返回原有 coding 值
        return existing_coding


# 应用函数并更新 'coding' 列
brandlist_df['coding'] = brandlist_df.apply(lambda row: update_coding(row['label'], row['coding']), axis=1)

# 将更新后的 DataFrame 写回 Excel 文件中
with pd.ExcelWriter(new_brandlist_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    brandlist_df.to_excel(writer, sheet_name='skincare', index=False)
