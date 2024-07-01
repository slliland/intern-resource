import pandas as pd

# 读取xlsx文件
def convert_xlsx_to_csv(xlsx_file_path, csv_file_path):
    # 使用pandas读取xlsx文件
    df = pd.read_excel(xlsx_file_path)

    # 将DataFrame保存为CSV文件，指定UTF-8编码
    df.to_csv(csv_file_path, index=False, encoding='utf-8')

# 设置源xlsx文件路径和目标csv文件路径
source_xlsx = '/Users/songyujian/Downloads/testinput.xlsx'  # 这里改为你的.xlsx文件路径
target_csv = '/Users/songyujian/Downloads/testinput.csv'    # 这里改为你想要保存的.csv文件路径

# 调用函数进行转换
convert_xlsx_to_csv(source_xlsx, target_csv)
