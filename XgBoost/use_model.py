import pandas as pd
import numpy as np
import xgboost as xgb
import codecs

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


X = pd.get_dummies(X)

min_Y, max_Y = Y[list].min(), Y[list].max()  # 求出'C'列数据的最小值和最大值
Y[list] = (Y[list] - min_Y[0]) / (max_Y[0] - min_Y[0])  # 进行最小-最大标准化
Y[list] = Y[list].apply(np.log1p)


from sklearn.model_selection import train_test_split

# 随机抽取训练集和验证集
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.3, random_state=0)

# 加载模型
loaded_model = xgb.XGBClassifier()
loaded_model.load_model('AI_BL_xgb.model')

# 使用模型进行预测
loaded_model.predict(Xtest)

# params = {
#         'max_depth': np.random.randint(5, 16),
#         'eta': np.random.uniform(0.01, 0.3),
#         'n_estimators': np.random.randint(10, 300),
#         'gamma': np.random.uniform(0.0, 0.2),
#         'subsample': np.random.uniform(0.6, 0.9),
#         'colsample_bytree': np.random.uniform(0.5, 0.8),
#         'min_child_weight': np.random.randint(1, 41),
#         'max_delta_step': np.random.randint(1, 11),
#         'seed': 2023,
#         'objective':'reg:logistic',
#         'eval_metric':'mae'
#     }
#
# bst = xgb.Booster(params)
# bst.load_model('AI_BL_xgb.model')