import re
import time

import pandas as pd
from openai import OpenAI

# 原始数据路径
input_path = '/Users/songyujian/Downloads/Raw data_品牌开放题_第二批 0614【skincare+hair+perfume+men】.xlsx'
# 品牌列表，注意此处要替换为实际使用的sheet_name（品类）
brand_list_path = pd.read_excel('/Users/songyujian/Downloads/new_brandlist.xlsx', sheet_name='men')
# 结果表格输出地址
final_output_path = '/Users/songyujian/Downloads/coding2/brandcoding_fin/final_men.xlsx'
mapping_output_path = '/Users/songyujian/Downloads/coding2/brandcoding_map/Map_men.xlsx'
tmp_output_path = '/Users/songyujian/Downloads/coding2/brandcoding_tmp/Tmp_men.xlsx'

'''
第一步：转置表格，生成TMP（中间表 data转置后的数据存根）
输入：某一品类的原始数据
输出：某一品类的TMP数据存根
'''


def split_brands(brand_string):
    # 确保 brand_string 是一个字符串
    if isinstance(brand_string, str):
        split_pattern = r'、|，|,|。|(?<=[\u4e00-\u9fff])\s(?=[\u4e00-\u9fff])'
        return re.split(split_pattern, brand_string)
    else:
        # 如果 brand_string 不是字符串，则返回空列表
        return []



def trans(input_path, tmp_output_path, sheetname):
    df = pd.read_excel(input_path, sheet_name=sheetname)

    # 将DataFrame从宽格式转换为长格式
    long_df = df.melt(id_vars=['Respondent.Serial'],
                      var_name='Question_Brand_Number',
                      value_name='Brand')

    # 过滤掉值为空的行
    long_df.dropna(subset=['Brand'], inplace=True)

    if sheetname == 'HAIR Raw data':
        # 对于特定 Respondent.Serial 应用 split_brands 函数
        def apply_split(row):
            if row['Question_Brand_Number'] == 'BB_Loop[{_10101}].B3':
                return split_brands(row['Brand'])
            else:
                return [row['Brand']]

        # 应用拆分函数，并展开结果为多行
        long_df['Brand'] = long_df.apply(apply_split, axis=1)
        long_df = long_df.explode('Brand').reset_index(drop=True)

    # 去除拆分后内容为空的单元格所在的行
    long_df.dropna(subset=['Brand'], inplace=True)

    # 提取回答品牌序号
    long_df['题号'] = long_df['Question_Brand_Number']

    # 重命名列
    long_df.rename(columns={'Brand': '回答品牌'}, inplace=True)

    # 调整列顺序
    long_df = long_df[['Respondent.Serial', '题号', '回答品牌']]

    # 根据 Respondent.Serial 和 题号 排序
    long_df.sort_values(by=['Respondent.Serial', '题号'], inplace=True)

    # 输出到Excel文件中
    long_df.to_excel(tmp_output_path, index=False)


'''
第二步：初步匹配，将转置后的数据逐个与品牌码表的数据比对，生成初步匹配结果
输入：TMP表、品牌列表
输出：初步匹配结果
'''


from multiprocessing import Pool

def normalize_text(text):
    return re.sub(r'[\s\t\n]+', '', text).lower()

def check_match(brand, coding_fields):
    brand_normalized = normalize_text(brand)
    for field in coding_fields:
        if field and not pd.isnull(field):
            keywords = [normalize_text(keyword) for keyword in field.split('|')]
            if brand_normalized in keywords:
                return True
    return False

# 这是一个工作函数，它将被映射到每一行上
def process_row(row):
    brand_to_check = row['回答品牌']
    for _, brand_list_row in brand_list_path.iterrows():
        if check_match(brand_to_check, [brand_list_row['coding'], brand_list_row['coding2']]):
            return ('是', brand_list_row['code'], brand_list_row['label'], brand_list_row['segment'])
    return ('否', None, None, None)

def mapping():
    # 加载数据
    data1 = pd.read_excel(tmp_output_path)

    data1['回答品牌'] = data1['回答品牌'].astype(str)
    brand_list_path['coding'] = brand_list_path['coding'].astype(str)
    brand_list_path['coding2'] = brand_list_path['coding2'].astype(str)

    # 新增列初始化
    data1[['是否匹配', 'code', 'label', 'segment']] = None

    # 创建进程池并映射 process_row 函数到每一行
    with Pool(processes=4) as pool:  # processes 的数量
        results = pool.map(process_row, [row for _, row in data1.iterrows()])

    # 将结果更新回data1
    for index, (match, code, label, segment) in enumerate(results):
        data1.at[index, '是否匹配'] = match
        data1.at[index, 'code'] = code
        data1.at[index, 'label'] = label
        data1.at[index, 'segment'] = segment

    # 保存更新后的文件
    data1.to_excel(mapping_output_path, index=False)


'''
第三步：将初步匹配结果中，没有匹配的结果再次用AI检查，确保没有遗漏，生成最终输出结果
输入：初步匹配结果、品牌列表
输出：最终匹配结果
'''
# 设置AI检查的API客户端
client = OpenAI(
    api_key="sk-l6r0OoY09uVet8ybar31YrnIpQaJ0DiDsn4z8enRVTEqUslc",  # 替换为你的Moonshot API密钥
    base_url="https://api.moonshot.cn/v1",
)


# 返回AI判断的品牌正确名称
def get_brand_name(label):
    # 发送问题到Moonshot AI
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": "你是一个人工智能品牌专家。以下是被访者回答的一个品牌名称，请仅提供品牌的正确标准名称或者‘无匹配品牌’，不要添加任何额外的解释或文字。"},
            {"role": "user", "content": f"品牌：'{label}'，请问对应的正确品牌名称是什么？"}
        ]
        ,
        temperature=0.3,
    )
    # 获取并返回回答内容
    response = completion.choices[0].message.content
    return response


# 返回AI判断的品牌是否属于该品类
def get_type_name(label):
    # 发送问题到Moonshot AI
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你是一个人工智能品牌专家。以下是被访者回答的一个品牌名称，请仅判断该品牌是否有Skincare （护肤品）、Makeup （彩妆）、Haircare （护发品）、Hair coloration （染发）、Perfume （香水）类的产品，你的回答只能是'是'或'否'，不要添加任何额外的解释或文字。"},
            {"role": "user", "content": f"品牌：'{label}'，请问该品牌是否有Skincare （护肤品）、Makeup （彩妆）、Haircare （护发品）、Hair coloration （染发）、Perfume （香水）类的产品？"}
        ]
        ,
        temperature=0.3,
    )
    # 获取并返回回答内容
    response = completion.choices[0].message.content
    return response


# 读取Excel文件
df = pd.read_excel(mapping_output_path)
# 过滤出 '是否匹配' 列值为 '否' 的行
filtered_df = df[df['是否匹配'] == '否']
# 对 '回答品牌' 列去重
unique_labels_df = filtered_df.drop_duplicates(subset=['回答品牌'])


# 处理大小写
def normalize_text(text):
    if pd.isna(text):
        return ''  # 或者根据需要返回其他合适的默认值
    return re.sub(r'[\s\t\n]+', '', str(text)).lower()


# 检查是否匹配品牌列表
def check_match(brand, coding_fields):
    brand_normalized = normalize_text(brand)
    for field in coding_fields:
        if field and not pd.isnull(field):
            keywords = [normalize_text(keyword) for keyword in field.split('|')]
            if brand_normalized in keywords:
                return True
    return False


# 更新输出品牌
def update_labels(unique_labels_df, brand_list_df):
    # 加载原始数据
    original_df = pd.read_excel(mapping_output_path)

    # 在内存中进行所有更新操作
    for index, row in unique_labels_df.iterrows():
        label = row['回答品牌']
        print(label)
        if pd.isna(label):
            continue

        # 假设 get_brand_name 和 get_type_name 是已经定义好的函数
        brand_response = get_brand_name(label)
        type_response = get_type_name(label)

        print(brand_response + type_response)

        if type_response == '是' or type_response == '是。':
            type_response = '是'
        elif type_response == '否' or type_response == '否。':
            type_response = '否'

        # 初始化new_label
        new_label = None
        new_code = None
        new_segment = None

        if "无匹配品牌" not in brand_response and brand_response:
            formatted_response = normalize_text(brand_response.strip())
            # 遍历brand_list_df中每一行，检查是否有匹配项
            for _, data2_row in brand_list_df.iterrows():
                if check_match(formatted_response, [data2_row['coding'], data2_row['coding2']]):
                    new_label = data2_row['label']
                    new_code = data2_row['code']
                    new_segment = data2_row['segment']
                    break  # 找到匹配项后停止遍历

        # 如果没有找到匹配项，则将响应设为空字符串
        if new_label is None:
            new_label = ''
        if new_code is None:
            new_code = ''
        if new_label is None:
            new_label = ''
        '''
        二次判断：此处二次检查第一次AI判断为"无匹配品牌"的品牌，并且更新品牌标准名称、品牌是否有标准名称、品牌是否属于该类别等信息
        '''
        if brand_response == '无匹配品牌':
            second_brand_match = get_brand_name(label)
            time.sleep(0.1)
            if second_brand_match == '无匹配品牌':
                original_df.loc[
                    original_df['回答品牌'].apply(normalize_text) == normalize_text(label), '品牌标准名称'] = label
                original_df.loc[original_df['回答品牌'].apply(normalize_text) == normalize_text(label), '品牌是否有标准名称'] = '否'
            else:
                type_response = get_type_name(second_brand_match)
                if type_response == '是' or type_response == '是。':
                    type_response = '是'
                elif type_response == '否' or type_response == '否。':
                    type_response = '否'
                time.sleep(0.05)
                original_df.loc[
                    original_df['回答品牌'].apply(normalize_text) == normalize_text(label), '品牌标准名称'] = second_brand_match
                original_df.loc[original_df['回答品牌'].apply(normalize_text) == normalize_text(label), '品牌是否有标准名称'] = '是'
        else:
            original_df.loc[original_df['回答品牌'].apply(normalize_text) == normalize_text(label), '品牌是否有标准名称'] = '是'
            original_df.loc[
                original_df['回答品牌'].apply(normalize_text) == normalize_text(label), '品牌标准名称'] = brand_response

        # 更新 'label' 列的值，仅对当前行有效
        original_df.loc[original_df['回答品牌'].apply(normalize_text) == normalize_text(label), '品牌是否属于该类别'] = type_response
        original_df.loc[original_df['回答品牌'].apply(normalize_text) == normalize_text(label), 'label'] = new_label
        original_df.loc[original_df['回答品牌'].apply(normalize_text) == normalize_text(label), 'code'] = new_code
        original_df.loc[original_df['回答品牌'].apply(normalize_text) == normalize_text(label), 'segment'] = new_segment

        # 确保不会超出API的TPM限额
        time.sleep(0.25)

    # 保存更改回文件
    original_df.to_excel(final_output_path, index=False)


# update_labels(file_path, unique_labels_df, brand_list_path)
if __name__ == '__main__':
    # 先跑trans() 用于数据转置，把调研的宽格式转换为长格式(一个品牌一个被访者一行) 输出为TMP.xlsx
    # print('数据转置')
    # 调用函数，需要提供输入和输出文件路径
    # trans(input_path, tmp_output_path, 'Men rawdata')
    # 再跑mapping() 用转换后的TMP数据跟码表进行匹配
    # print('数据匹配')
    # mapping()
    # 最后更新品牌，查漏补缺
    update_labels(unique_labels_df, brand_list_path)