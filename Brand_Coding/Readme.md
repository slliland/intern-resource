# 品牌匹配处理脚本

## 概述

此脚本用于处理与品牌相关的调研数据，具体涉及“Makeup（化妆品）”、“Hair（头发护理）”、“Skincare（护肤）”和“Perfume（香水）”四个品类。脚本执行三个主要任务：

1. **数据转置**：将调研数据从宽格式转换为长格式，每一行代表一个受访者对某一品牌的回答。
2. **初步匹配**：将转置后的数据与品牌码表进行比对，生成初步匹配结果。
3. **AI辅助验证**：使用AI服务（KIMI AI）确保没有遗漏任何匹配，并生成最终输出结果。

## 环境要求

- 系统中安装了Python 3.x。
- 安装了Pandas库（`pip install pandas`）。
- 安装了OpenAI库（`pip install openai`）。
- 拥有KIMI AI API的有效API密钥。

## 设置

在运行脚本之前，请确保更新脚本中以下变量：

- `input_path`：包含原始调研数据的Excel文件路径。
- `tmp_output_path`：临时转置数据将被保存的路径。
- `mapping_output_path`：初步匹配结果将被保存的路径。
- `final_output_path`：在AI验证后最终输出结果将被保存的路径。
- `brand_list_path`：包含品牌码表的Excel文件路径。

此外，请在以下行中替换为你实际的Moonshot AI API密钥：

```python
client = OpenAI(api_key="你的API密钥", base_url="https://api.moonshot.cn/v1")
```
## 运行脚本

该脚本包含三个对应于处理步骤的函数：

- 要进行数据转置，请取消注释并运行：
```python
trans(input_path, tmp_output_path)
```
- 要执行初步匹配，请取消注释并运行：
```python
mapping()
```
- 要执行AI辅助验证并生成最终输出，请取消注释并运行：
```python
update_labels(file_path, unique_labels_df, brand_list_path)
```
- 请确保按顺序运行这些函数，因为每个步骤都依赖于前一个步骤的输出。

## 数据处理流程
```python
trans() 函数：
```
- 从Excel文件读取原始调研数据。
- 将数据转换成长格式。
- 将这些中间数据保存到新的Excel文件中。
```python
mapping() 函数：
```
- 从Excel文件加载转置后的数据。 
- 将每个条目与另一个包含品牌代码列表的Excel文件中的条目进行比对。 
- 标记匹配项并将初步结果保存到另一个Excel文件中。
```python
update_labels() 函数：
```
- 从Excel文件读取初步匹配结果。 
- 对于没有匹配项的条目，向Moonshot AI发送请求进行验证。 
- 根据AI响应更新条目，并将最终结果保存到Excel文件中。
## 注意事项

- 请确保您选择了正确的原始数据中的品类sheet。
- 每次运行只处理一个品类的数据，如果要选择新品类并重新运行，请更改所有相关的sheet名和表格名。