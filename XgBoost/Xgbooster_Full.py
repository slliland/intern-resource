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
Xtrain.to_excel('Xtrain.xlsx')
Xtest.to_excel('Xtest.xlsx')
print('train,test已保存')

# 如果有明确的训练集和验证机 用这块
# train = pd.read_excel('Xtrain.xlsx',header=0)
# test = pd.read_excel('Xtest.xlsx',header=0)
# Trainindex = train.iloc[:,0]
# Testindex = test.iloc[:,0]
# Xtrain =X[X.index.isin(Trainindex)]
# Xtest =X[X.index.isin(Testindex)]
# Ytrain =Y[Y.index.isin(Trainindex)]
# Ytest =Y[Y.index.isin(Testindex)]



train_matrix = xgb.DMatrix(data=Xtrain, label=Ytrain)

best_mae = 1
best_mae_index = 0

# 有明确调优后的参数用这个，并且不需要循环
# best_param={'max_depth': 6, 'eta': 0.09, 'n_estimators': 100, 'gamma': 0.2, 'subsample': 0.65, 'colsample_bytree': 0.6, 'min_child_weight': 7, 'max_delta_step': 9, 'seed': 33, 'objective': 'reg:logistic', 'eval_metric': 'mae'}
# for i in range(1):

# 调参验证  有明确参数以后可以不需要调参
best_param={}
for i in range(10000):
    params = {
        'max_depth': np.random.randint(5, 16),
        'eta': np.random.uniform(0.01, 0.3),
        'n_estimators': np.random.randint(10, 300),
        'gamma': np.random.uniform(0.0, 0.2),
        'subsample': np.random.uniform(0.6, 0.9),
        'colsample_bytree': np.random.uniform(0.5, 0.8),
        'min_child_weight': np.random.randint(1, 41),
        'max_delta_step': np.random.randint(1, 11),
        'seed': 2023,
        'objective':'reg:logistic',
        'eval_metric':'mae'
    }
    params = best_param
    # eta ： 默认是0.3，别名是 leanring_rate，更新过程中用到的收缩步长，在每次提升计算之后，算法会直接获得新特征的权重。 eta通过缩减特征的权重使提升计算过程更加保守；
    # gamma：默认是0，别名是 min_split_loss，在节点分裂时，只有在分裂后损失函数的值下降了（达到gamma指定的阈值），才会分裂这个节点。gamma值越大，算法越保守（越不容易过拟合）；
    # max_depth：默认是6，树的最大深度，值越大，越容易过拟合；
    # min_child_weight：默认是1，决定最小叶子节点样本权重和，加权和低于这个值时，就不再分裂产生新的叶子节点。当它的值较大时，可以避免模型学习到局部的特殊样本。但如果这个值过高，会导致欠拟合。
    # max_delta_step：默认是0，这参数限制每颗树权重改变的最大步长。如果是 0 意味着没有约束。如果是正值那么这个算法会更保守，通常不需要设置。
    # subsample：默认是1，这个参数控制对于每棵树，随机采样的比例。减小这个参数的值算法会更加保守，避免过拟合。但是这个值设置的过小，它可能会导致欠拟合。
    # colsample_bytree：默认是1，用来控制每颗树随机采样的列数的占比；
    # colsample_bylevel：默认是1，用来控制的每一级的每一次分裂，对列数的采样的占比；
    # lambda：默认是1，别名是reg_lambda，L2 正则化项的权重系数，越大模型越保守；
    # alpha：默认是0，别名是reg_alpha，L1 正则化项的权重系数，越大模型越保守；
    # seed：随机数种子，相同的种子可以复现随机结果，用于调参！
    # n_estimators：弱学习器的数量

    cv_nround = 1000
    cv_nfold = 5
    xgb_cv = xgb.cv(dtrain=train_matrix, params=params, num_boost_round=cv_nround, nfold=cv_nfold,
                    verbose_eval=True, early_stopping_rounds=5, maximize=False, metrics='mae')

    min_mae_index = xgb_cv['test-mae-mean'].idxmin()
    min_mae = xgb_cv['test-mae-mean'][min_mae_index]

    print('min_mae_index',min_mae_index)
    print('min_mae',min_mae)

    if min_mae < best_mae:
        best_mae = min_mae
        best_mae_index = min_mae_index
        best_param = params


nround = best_mae_index

print(best_param)

f.write(str(best_param)+ '\r\n')
f.close()


bst_model = xgb.train(params=best_param, dtrain=train_matrix, num_boost_round=nround)
bst_model.save_model('AI_BL_xgb.model')
print('AI_BL_xgb已保存')



bst = xgb.Booster(model_file='AI_BL_xgb.model')
dtest = xgb.DMatrix(Xtest)
y_pred = bst.predict(dtest)

Ytest = Ytest.reset_index(drop=True).assign(pred_result=pd.Series(y_pred))


mae = np.mean(np.abs(Ytest[ListY[0]] - Ytest['pred_result']))
print('MAE（平均绝对误差）',mae)

from sklearn.metrics import mean_squared_error
rmse = np.sqrt(mean_squared_error(Ytest[ListY[0]], Ytest['pred_result']))
print('RMSE (均方根误差):', rmse)


gain_score = bst.get_score(importance_type='gain')
cover_score = bst.get_score(importance_type='cover')
freq_score = bst.get_score(importance_type='weight')

df_gain = pd.DataFrame.from_dict(gain_score, orient='index', columns=['gain'])
df_cover = pd.DataFrame.from_dict(cover_score, orient='index', columns=['cover'])
df_freq = pd.DataFrame.from_dict(freq_score, orient='index', columns=['frequency'])
df_result = pd.concat([df_gain, df_cover, df_freq], axis=1)

df_result.to_excel('importance.xlsx')


Ytest['pred_result'] = Ytest['pred_result'].apply(np.expm1)
Ytest['pred_result'] = Ytest['pred_result']*(max_Y[0] - min_Y[0]) + min_Y[0]
Ytest[ListY[0]] = Ytest[ListY[0]].apply(np.expm1)
Ytest[ListY[0]] = Ytest[ListY[0]]*(max_Y[0] - min_Y[0]) + min_Y[0]


Ytest.to_excel('report.xlsx')
print('importance已保存')
print('report已保存')

import shap
explainer = shap.Explainer(bst)
shap_values = explainer.shap_values(Xtest)
df_shap = pd.DataFrame(shap_values, columns=Xtest.columns)
df_shap.to_excel('df_shap.xlsx')
print('df_shap已保存')

import matplotlib.pyplot as plt
import seaborn as sns
# 绘制散点图并保存为PNG文件（类似于R代码中ggplot2的绘图）
plt.figure(figsize=(10, 8))
sns.scatterplot(data=Ytest, x=ListY[0], y='pred_result')
plt.title('散点图: 真实值 vs 预测值')
plt.xlabel('真实值')
plt.ylabel('预测值')
sns.regplot(x=ListY[0], y='pred_result', data=Ytest, scatter=False, color='blue')
plt.savefig('scatter_plot.png') # 将图表保存到文件中
print('散点图已保存为 scatter_plot.png')
features_list = ['logo出现时长_解析', '品牌提及次数', '明星系数', '广告语字数']

# 遍历特征列表，为每个特征绘制散点图
for feature in features_list:
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=Ytest, x=feature, y='pred_result')
    sns.regplot(x=feature, y='pred_result', data=Ytest, scatter=False, color='blue')  # 添加趋势线
    plt.title(feature)
    plt.xlabel(feature)
    plt.ylabel('Predicted Value')
    plt.savefig(f'{feature}.png')  # 将文件保存为PNG格式
    plt.close()  # 关闭当前图形，避免重叠绘制



