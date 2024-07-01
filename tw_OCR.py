import requests

# 假设你知道视频的总时长
total_duration = 15  # 例如视频总共1200秒
batch_size = 5  # 每次请求15秒
url_template = "https://api.twelvelabs.io/v1.2/indexes/664b075a1c2d1584da1ad458/videos/6655860dd22b3a3c97bef944/text-in-video?start={}&end={}"

headers = {
    "accept": "application/json",
    "x-api-key": "tlk_1PXAPG820HTJZP2732E4821DMCX4",
    "Content-Type": "application/json"
}

# 存储OCR文本和文件名
ocr_texts = []
filename = 'unknown'  # 如果API响应中包含文件名，请替换此值

# 分批请求OCR数据
for start in range(0, total_duration, batch_size):
    end = min(start + batch_size, total_duration)
    url = url_template.format(start, end)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # 假设返回的JSON结构包含一个字段 'text' 包含OCR文本
        ocr_texts.append(data.get('text', ''))
        # 如果API响应中包含文件名，请从响应中提取并更新filename变量
        # filename = data.get('filename', filename)
    else:
        print(f"Error fetching data for range {start}-{end}: {response.text}")

# 合并所有文本片段
full_ocr_text = ' '.join(ocr_texts)

# 输出结果
print(f"Filename: {filename}")
print(f"OCR Text: {full_ocr_text}")