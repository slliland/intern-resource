import pandas as pd
import numpy as np
import xgboost as xgb
import codecs
from matplotlib import font_manager

def dummies_Sp(data,list,_sep):
    df_tmp = data[list].str.get_dummies(sep=_sep).add_prefix(list+'_')
    data = pd.concat([data, df_tmp], axis=1)
    data = data.drop(columns=[list])
    return data


f = codecs.open('log.txt','w','utf-8')

ExcelPath = './data.xlsx'
data = pd.read_excel(ExcelPath,sheet_name='Sheet1', skiprows=lambda x: x in [0])

ListX = ['logo出现时长_解析','品牌提及次数','明星系数','广告语字数']

ListY = ['品牌回忆指数']

X = data[ListX]
Y = data[ListY]

train = pd.read_excel('Xtrain.xlsx',header=0)
test = pd.read_excel('Xtest.xlsx',header=0)
Trainindex = train.iloc[:,0]
Testindex = test.iloc[:,0]
Xtrain =X[X.index.isin(Trainindex)]
Xtest =X[X.index.isin(Testindex)]
Ytrain =Y[Y.index.isin(Trainindex)]
Ytest =Y[Y.index.isin(Testindex)]

bst = xgb.Booster(model_file='AI_BL_xgb.model')
dtest = xgb.DMatrix(Xtest)
y_pred = bst.predict(dtest)

Ytest = Ytest.reset_index(drop=True).assign(pred_result=pd.Series(y_pred))


mae = np.mean(np.abs(Ytest[ListY[0]] - Ytest['pred_result']))
print('MAE（平均绝对误差）',mae)

from sklearn.metrics import mean_squared_error
rmse = np.sqrt(mean_squared_error(Ytest[ListY[0]], Ytest['pred_result']))
print('RMSE (均方根误差):', rmse)

import matplotlib.pyplot as plt
import seaborn as sns
# 设置中文字体
font_path = "/System/Library/Fonts/PingFang.ttc"
my_font = font_manager.FontProperties(fname=font_path)

# 绘制散点图并保存为PNG文件（类似于R代码中ggplot2的绘图）
plt.figure(figsize=(10, 8))
sns.scatterplot(data=Ytest, x=ListY[0], y='pred_result')
plt.title('散点图: 真实值 vs 预测值', fontproperties=my_font)
plt.xlabel('真实值', fontproperties=my_font)
plt.ylabel('预测值', fontproperties=my_font)
sns.regplot(x=ListY[0], y='pred_result', data=Ytest, scatter=False, color='blue')
plt.savefig('scatter_plot.png') # 将图表保存到文件中
print('散点图已保存为 scatter_plot.png')
features_list = ['logo出现时长_解析', '品牌提及次数', '明星系数', '广告语字数']

print(Ytest)
