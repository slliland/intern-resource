import os
import glob
import openpyxl
import csv

# 设置源文件夹路径
source_folder = '/Users/songyujian/Downloads/AI提取'

# 切换到源文件夹路径
os.chdir(source_folder)

# 搜索文件夹中所有的xlsx文件
xlsx_files = glob.glob('*.xlsx')

# 遍历所有找到的xlsx文件
for xlsx_file in xlsx_files:
    # 打开xlsx工作簿
    workbook = openpyxl.load_workbook(xlsx_file)
    # 默认转换第一个工作表
    sheet = workbook.active

    # 创建CSV文件名（与xlsx相同的名称）
    csv_file = os.path.splitext(xlsx_file)[0] + '.csv'

    # 打开新的CSV文件，并写入内容
    with open(csv_file, 'w', newline="", encoding='utf-8') as f:
        c = csv.writer(f)
        for r in sheet.iter_rows():
            c.writerow([cell.value for cell in r])

print("转换完成！")
