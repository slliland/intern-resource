# -*- coding: utf-8 -*-
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, stop_after_attempt, wait_random_exponential
import pandas as pd
from openai import OpenAI
import time
import requests

# 加载环境变量
api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('url')

# 初始化OpenAI客户端
client = OpenAI(api_key=api_key, base_url=base_url)

# 指定文件路径
file_path = '/Users/songyujian/Downloads/Raw data_品牌开放题示例V_minghui.xlsx'
# 指定工作表名称
makeup_sheet = 'MAKEUP Brand list(SC)'

# 读取回答品牌数据
df_answers = pd.read_excel('/Users/songyujian/Downloads/test_output.xlsx')
# 读取品牌列表数据
df_brands = pd.read_excel('/Users/songyujian/Downloads/Raw data_品牌开放题示例V_minghui.xlsx',
                          sheet_name='SKINCARE Brand list 2023', usecols="B", skiprows=2)
# 读取Excel文件的B和C列，并跳过前两行
df_makeup = pd.read_excel(
    file_path,
    sheet_name=makeup_sheet,
    usecols="B:E",  # 指定只读取B和C列
    skiprows=2
)

# 删除包含空值的行
df_brands.dropna(inplace=True)

# 将数据以行为单位存储到列表中
rows_list = df_makeup.values.tolist()

# 打印结果，查看列表内容
for row in rows_list:
    print(row)
# # 将品牌列表转换成集合，便于快速查找
# brand_set = set(df_brands.iloc[:, 0].dropna())
#
# class TokenBucket:
#     def __init__(self, tokens_per_interval, interval=1.0):
#         self.capacity = float(tokens_per_interval)
#         self._tokens = self.capacity
#         self.interval = interval
#         self.lock = threading.Lock()
#         self.last_time = time.time()
#
#     def consume(self, tokens=1):
#         with self.lock:
#             now = time.time()
#             lapse = now - self.last_time
#             # 添加新令牌
#             increment = lapse * (self.capacity / self.interval)
#             self._tokens += increment
#             if self._tokens > self.capacity:
#                 self._tokens = self.capacity
#             # 记录上次添加令牌的时间
#             self.last_time = now
#
#             if tokens <= self._tokens:
#                 # 消耗令牌并允许操作
#                 self._tokens -= tokens
#                 return True
#             return False
#
# # 每分钟请求的最大数量
# MAX_REQUESTS_PER_MINUTE = 40
#
# # 创建一个每分钟生成MAX_REQUESTS_PER_MINUTE个令牌的桶实例
# bucket = TokenBucket(MAX_REQUESTS_PER_MINUTE, 60)
# MAX_RETRIES = 3
# @retry(wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(MAX_RETRIES))
# def check_brand_match(brand):
#     global bucket
#
#     # 等待直到获取足够的令牌进行API调用
#     while not bucket.consume():
#         time.sleep(0.1)  # 短暂休眠后重试
#     try:
#         print(f"Attempting API call for brand: {brand}")
#         # 尝试执行API调用
#         completion = client.chat.completions.create(
#             model="moonshot-v1-8k",
#             messages=[
#                 {"role": "system", "content": "你是一名评论内容标注专家。"},
#                 {"role": "user",
#                  "content": f"请问'{brand}'是否在下面这个品牌列表中？完全匹配到品牌列表中的品牌名称的中文，注意，一定是每一个字都匹配，有一个字不一样或者比品牌列表中的品牌少一个字都判定为否）？{list(brand_set)}你的回答的格式为：是或否 品牌列表中的品牌名"}
#             ],
#             temperature=0.3,
#         )
#         response_content = completion.choices[0].message.content.strip()
#
#         match = re.search(r'\b是\b', response_content)
#         if match:
#             return brand, '是'
#
#         # 如果没有完全匹配，则进行相似度查询
#         follow_up_completion = client.chat.completions.create(
#             model="moonshot-v1-8k",
#             messages=[
#                 {"role": "system", "content": "你是一名评论内容标注专家。"},
#                 {"role": "user",
#                  "content": f"在下面这个品牌列表中，哪个品牌名称最接近'{brand}'？{list(brand_set)}你的回答为：品牌列表中的品牌名（没有特别接近的就输出无）"}
#             ],
#             temperature=0.3
#         )
#
#         follow_up_content = follow_up_completion.choices[0].message.content.strip()
#         return follow_up_content if follow_up_content in brand_set else "", '否'
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         time.sleep(25)
#         raise  # 重新抛出异常以触发重试机制
#
#
# # 创建一个长度和df_answers['回答品牌']相同、初始值为None的列表
# matched_brand = [None] * len(df_answers['回答品牌'])
# is_matched = [None] * len(df_answers['回答品牌'])
#
# # 创建线程池执行并行处理
# with ThreadPoolExecutor(max_workers=5) as executor:
#     # 提交任务到线程池，并记录每个任务对应df_answers中的索引
#     future_to_index = {executor.submit(check_brand_match, brand): index for index, brand in
#                        enumerate(df_answers['回答品牌'])}
#
#     # 收集结果，并根据索引放入正确位置
#     for future in as_completed(future_to_index):
#         index = future_to_index[future]
#         try:
#             brand, match_result = future.result()
#             matched_brand[index] = brand
#             is_matched[index] = match_result
#             print(f"Brand: {brand}, Match: {match_result}")
#         except Exception as e:
#             print(f"Error processing brand match: {e}")
#
# # 添加新列到DataFrame中
# df_answers['输出品牌（AI输出结果，只输出目标品类品牌）'] = matched_brand
# df_answers['是否与品牌list匹配（是否在给到的品牌清单中）'] = is_matched
#
# # 保存至Excel文件
# output_file_path = 'test_output_processed.xlsx'
# with pd.ExcelWriter(output_file_path, engine='openpyxl', mode='w') as writer:
#     df_answers.to_excel(writer, index=False)
