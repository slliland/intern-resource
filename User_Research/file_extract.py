import os
from docx import Document
from openai import OpenAI
from pathlib import Path

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="sk-l6r0OoY09uVet8ybar31YrnIpQaJ0DiDsn4z8enRVTEqUslc",
    base_url="https://api.moonshot.cn/v1",
)

# 指定输出目录路径和最终汇总文件路径
output_base_directory_path = '/Users/songyujian/Downloads/深访_精华眼霜用户研究/output'
final_summary_doc_path = '/Users/songyujian/Downloads/深访_精华眼霜用户研究/final_summary.docx'

# 创建新文档对象
final_summary_doc = Document()

# 遍历输出目录中的所有子文件夹
for subdir, dirs, files in os.walk(output_base_directory_path):
    for filename in files:
        if filename.endswith('.docx'):
            file_path = Path(subdir) / filename

            # 使用 OpenAI API 提取文件内容
            try:
                with open(file_path, 'rb') as file_stream:
                    file_object = client.files.create(file=file_stream, purpose="file-extract")
                    file_content = client.files.content(file_id=file_object.id).text

                    # 构建消息列表
                    messages = [
                        {
                            "role": "system",
                            "content": "你是一个消费品调查专家和内容概括高手。"
                        },
                        {
                            "role": "system",
                            "content": file_content,
                        },
                        {
                            "role": "user",
                            "content": ("以下是一个抗老护肤品入户深访笔录，请基于主持人的提问内容和被访者的回答内容，"
                                        "帮我做一个内容汇总，把被访者回答出的所有信息根据不同主题归纳成一整段话，"
                                        "用第一人称，需要非常全面且具体，任何被访者说的话都不要遗漏。最终给到我每个主题和对应内容。")
                        }
                    ]

                    # 获取汇总结果
                    completion = client.chat.completions.create(
                        model="moonshot-v1-8k",
                        messages=messages,
                        temperature=0.3,
                    )

                    # 将结果添加到文档中
                    summary_text = completion.choices[0].message['content']
                    final_summary_doc.add_paragraph(summary_text)

            except Exception as e:
                print(f"An error occurred while processing {filename}: {e}")

# 保存最终汇总文档到磁盘
final_summary_doc.save(final_summary_doc_path)

print(f"内容提取和汇总完成！所有结果已保存至 {final_summary_doc_path}")