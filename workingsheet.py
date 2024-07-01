import pandas as pd


# 读取Excel文件
sheetname = '舒肤佳｜每句洗手吃饭，都是家的守护-广告片&#58;快消产品视'
df = pd.read_excel('/Users/songyujian/Downloads/video_results_frame-by-frame.xlsx', sheet_name=sheetname)


# 定义一个函数，用于将datetime.time对象向下舍入到最近的秒
def floor_time_to_second(time_obj):
    # 返回一个新的datetime.time对象，只包含小时、分钟和秒
    return time_obj.replace(microsecond=0)


# 应用函数，创建一个新的列用于分组
df['Rounded_Timestamp'] = df['Timestamp'].apply(floor_time_to_second)
# 按照向下舍入的时间戳分组，并计算Cognitive Demand和Focus的平均值
result = df.groupby('Rounded_Timestamp')[['Cognitive Demand', 'Focus']].mean().reset_index()


# 将时间格式从HH:MM:SS更改为MM:SS
def format_minutes_and_seconds(time_obj):
    total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    return '{:02d}:{:02d}'.format(total_seconds // 60, total_seconds % 60)


result['Rounded_Timestamp'] = result['Rounded_Timestamp'].apply(format_minutes_and_seconds)
# 将结果写入新的Excel文件
outpath = str(sheetname + '_output.xlsx')
result.to_excel(outpath, index=False)