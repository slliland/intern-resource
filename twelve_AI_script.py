import pandas as pd
import requests
import time
from requests.exceptions import Timeout, RequestException

# 读取Excel文件
excel_path = '/Users/songyujian/Downloads/AI 脚本/AI script.xlsx'  # 请替换为您的用户名和正确的路径
df = pd.read_excel(excel_path)

# 初始化一个空列表来存储所有响应
responses_list = []

# 设置最大重试次数和重试间隔时间
max_retries = 5
retry_interval = 10  # 10秒

# 请求之间的延迟时间，设置为5秒以避免超出频率限制
delay_between_requests = 5

# Excel文件中的第一列是rsrc_id，第二列是prompt，第三列是video_id
# 遍历每一行数据
for index, row in df.iterrows():
    rsrc_id = row[0]
    prompt = row[1]
    video_id = row[2]

    # API请求的变量
    BASE_URL = "https://api.twelvelabs.io/v1.2"
    api_key = "tlk_2W0791D3WMWHFN2YFVRR92Q94PST"
    data = {
        "prompt": prompt,
        "video_id": video_id
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

    # 打印开始信息
    print(f"已开始第 {index + 1} 条数据, rsrc_id为 {rsrc_id}，prompt：{prompt}")

    # 初始化response变量为空，用于后续检查是否请求成功
    response = None

    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{BASE_URL}/generate",
                json=data,
                headers=headers,
                timeout=90  # 设置超时时间
            )
            # 检查HTTP状态码是否表示成功
            if response.status_code == 200:
                print(f"请求成功: {response.text}")
                break

            elif response.status_code == 429:
                retry_after = response.headers.get('Retry-After', delay_between_requests)
                print(f"请求太频繁, 等待 {retry_after} 秒后重试...")
                time.sleep(float(retry_after))
                continue

            else:
                print(f"请求失败，状态码: {response.status_code}")

        except (Timeout, RequestException) as e:
            print(f"请求出现问题: {e}, 正在尝试第 {attempt + 1} 次重试...")

        # 如果没有达到频率限制，则在下次请求前暂停执行指定延迟时间。
        time.sleep(delay_between_requests)

    if response is None or response.status_code != 200:
        print(f"全部重试完成，但请求未成功。")
        responses_list.append([rsrc_id, ''])
    else:
        responses_list.append([rsrc_id, response.text])

    # 打印完成信息（如果有响应）
    if response:
        print(f"已完成第 {index + 1} 条数据, rsrc_id为{rsrc_id}, 输出内容：{response.text}")

# 将列表转换为DataFrame
responses_df = pd.DataFrame(responses_list, columns=['rsrc_id', 'text'])

# 将所有响应保存到新的Excel文件
output_path = '/Users/songyujian/Downloads/AI 脚本/Output.xlsx'  # 请替换为您的用户名和想要保存的路径
responses_df.to_excel(output_path, index=False)

print("所有数据已经处理完成。")
