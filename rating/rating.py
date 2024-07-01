# -*- coding: utf-8 -*-
import openai
import os
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor
import time
from openai.error import RateLimitError

openai.api_key = os.getenv('OPENAI_API_KEY')  # 必填，如果没有微软的key，可以用申请给到的hash key  # 必填,若应用可使用默认api_key,则可以填空字符串
openai.api_base = os.getenv("OPENAI_API_BASE")  # 必填,代理url
prompt = "你是一个内容打分专家，这是一条用户开放题回答得分和该得分的评价依据，请帮我将这个评分放缩到0-2之间，结果保留两位小数，返回的信息必须只有python的浮点数据类型，其中数值为你放缩后的评分。一定在回答中不能有```python或```json这样的字"

def openai_create_chat_completions(content, retries=5, delay=25):
    for i in range(retries):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content}
                ],
                app_id="uOv9nxRzGmJtONU5",
                app_secret="Rc9jy3Tdo0teTUrVYSv6rRf7EvMTvoeW",
                user_email="songyj@foxmail.com",
                tag="2400159201"
            )
            return completion.choices[0].message['content']
        except RateLimitError as e:
            if i < retries - 1:  # 如果不是最后一次重试，等待后再次尝试
                time.sleep(delay)
            else:
                raise e  # 如果重试次数用完，抛出异常


# 每行数据处理
def process_text(text):
    wrong_str = re.compile('```json|```python|```')     # 排除干扰项
    completion = openai_create_chat_completions(text)
    try:
        if re.search(wrong_str, completion) is None:
            print(completion)
            return eval(completion)
        else:
            print(completion)
            return eval(re.sub(wrong_str, '', completion))
    except SyntaxError as e:
        return f"SyntaxError: {e}"


df = pd.read_excel('/Users/songyujian/Downloads/Book2.xlsx')
# 筛选出project_id特定值的行
df_16942 = df[df['project_id'] == 16942]
df_16949 = df[df['project_id'] == 16949]
df_16950 = df[df['project_id'] == 16950]
texts_16942 = df_16942["text"].tolist()
texts_16949 = df_16949["text"].tolist()
texts_16950 = df_16950["text"].tolist()

res_16942 = []
res_16949 = []
res_16950 = []


# 并行处理
def rating(texts, res):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_text, text) for text in texts]
        for future in futures:
            result = future.result()
            res.append(result)


rating(texts_16942, res_16942)
print(res_16942)
rating(texts_16949, res_16949)
print(res_16949)
rating(texts_16950, res_16950)
print(res_16950)

new_df_16942 = pd.DataFrame(res_16942)
new_df_16949 = pd.DataFrame(res_16949)
new_df_16950 = pd.DataFrame(res_16950)

new_df_16942.to_csv('res_16942.csv',mode='w', header=True, index=False)
new_df_16949.to_csv('res_16949.csv',mode='w', header=True, index=False)
new_df_16950.to_csv('res_16950.csv',mode='w', header=True, index=False)

max_len = max(len(res_16942), len(res_16949), len(res_16950))

# 如果列表长度不同，可以通过添加None来扩展它们
res_16942.extend([None] * (max_len - len(res_16942)))
res_16949.extend([None] * (max_len - len(res_16949)))
res_16950.extend([None] * (max_len - len(res_16950)))

# 创建一个DataFrame
df_all = pd.DataFrame({
    '16942': res_16942,
    '16949': res_16949,
    '16950': res_16950
})

# 计算每列的总和，忽略None值
totals = df_all.sum(skipna=True)

# 将总和作为新的一行添加到DataFrame的底部
df_all.loc['Total'] = totals

# 输出DataFrame到CSV文件
df_all.to_csv('result_all.csv', mode='w', header=True, index=True)