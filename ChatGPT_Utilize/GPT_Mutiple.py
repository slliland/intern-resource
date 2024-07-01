# -*- coding: utf-8 -*-
import openai
import os
import pandas as pd
from collections import defaultdict
import re
from concurrent.futures import ThreadPoolExecutor

openai.api_key = os.getenv('OPENAI_API_KEY')  # 必填，如果没有微软的key，可以用申请给到的hash key  # 必填,若应用可使用默认api_key,则可以填空字符串
openai.api_base = os.getenv("OPENAI_API_BASE")  # 必填,代理url
prompt = "你是一个内容标注专家，这是一条用户开放题回答，请帮我从亲情主题、故事情节、创意、品牌、产品、画面、场景、色调、人物、音乐、时长、广告语这12个维度提取回答中的对应信息，返回的信息必须只有python的字典数据类型，其中 key为维度名称，value为原回答中的内容，若没有就返回'无'。一定在回答中不能有```python或```json这样的字，key值和value值需要加双引号。"


def openai_create_chat_completions(content):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ],
        app_id="uOv9nxRzGmJtONU5",  # 必填,申请后提供
        app_secret="Rc9jy3Tdo0teTUrVYSv6rRf7EvMTvoeW",  # 必填,申请后提供
        user_email="songyj@foxmail.com",  # 必填,自己的邮箱
        tag="2400159201"  # 选填，应用或项目名称
    )
    return completion.choices[0].message['content']


# 合并每条回答
def merge_dicts(*dicts):
    merged_dict = defaultdict(list)
    for d in dicts:
        for key, value in d.items():
            if isinstance(value, list):
                merged_dict[key].extend(value)
            else:
                merged_dict[key].append(value)
    return dict(merged_dict)


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


df = pd.read_excel('/Users/songyujian/Downloads/likes.xlsx')
texts = df["text"].tolist()
col_len = len(df["text"])

res = {}
# 并行处理
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_text, text) for text in texts]
    for future in futures:
        result = future.result()
        if isinstance(result, dict):
            res = merge_dicts(res, result)
        else:
            print(f"Syntax error encountered: {result}")
print(res)
new_df = pd.DataFrame(res)
print(new_df)
new_df.to_csv('likeres1.csv',mode='w', header=True, index=False)