import pandas as pd

# 加载CSV文件
file_path = '/Users/songyujian/Downloads/skin.csv'  # 请替换为你的文件路径
df = pd.read_csv(file_path)

# 定义一个将描述转换为疑问句的函数
def to_question_chinese(desc):
    return f"面霜消费群体在{desc}方面有什么特点？"

# 修改原先的第一列，并替换成问题形式
df.iloc[:, 0] = df.iloc[:, 0].apply(to_question_chinese)

# 合并后两列作为新表格的第二列，使用fillna('')来确保空值被替换成空字符串
df['Merged Description'] = df.iloc[:, -2].fillna('').astype(str) + ' ' + df.iloc[:, -1].fillna('').astype(str)
# 过滤掉纯空白的结果
# df['Merged Description'] = df['Merged Description'].apply(lambda x: x.strip())
# 如果合并后的结果为空字符串，则用NaN代替，以便之后可以进行过滤
# df['Merged Description'].replace('', pd.NA, inplace=True)

# 删除原始表格中除了新第一列和新第二列之外的所有列
df = df.iloc[:, [0, -1]]  # 只保留新的第一列（问题）和最后一列（合并后的描述）

# 删除那些'Merged Description'仍然是NaN的行
# df.dropna(subset=['Merged Description'], inplace=True)

# 将修改后的DataFrame保存到新的CSV文件中
new_file_path = 'modified_skin.csv'  # 请替换为你希望保存的文件名
df.to_csv('/Users/songyujian/Downloads/' + new_file_path, index=False)  # 请替换为你希望保存文件的路径

print(f"Modified CSV file saved as: {new_file_path}")
