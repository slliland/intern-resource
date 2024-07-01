import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor
from xgboost import plot_importance

# 读取数据

datax = pd.read_excel("data.xlsx")

# 数据预处理（根据您提供的R代码进行了简化）
full = datax.copy()

# 直接赋值的字段
full['rsrcid'] = datax['rsrc_id']
full['benefit命中百分比'] = datax['benefit命中百分比']
full['明星名人'] = datax['明星名人']
full['是否为核心产品'] = datax['是否为核心产品']
full['产品类型'] = datax['产品类型']
full['ckprimarycategoryname'] = datax['ck_primary_category_name']
full['cksecondarycategoryname'] = datax['ck_secondary_category_name']
full['cksubcategoryname'] = datax['ck_sub_category_name']
full['pgprimarycategoryname'] = datax['pg_primary_category_name']
full['pgsecondarycategoryname'] = datax['pg_secondary_category_name']
full['pgsubcategoryname'] = datax['pg_sub_category_name']
full['producer'] = datax['producer']
full['ckproducer'] = datax['ck_producer']
full['branddomesticorinternational'] = datax['brand_domestic_or_international']
full['brandname'] = datax['brand_name']
full['ckbrandname'] = datax['ck_brand_name']
full['adsname'] = datax['ads_name']
full['ckadsname'] = datax['ck_ads_name']
full['adstype'] = datax['ads_type']
full['adsduration'] = datax['ads_duration']
full['isusequestion'] = datax['is_use_question']
full['isrtb'] = datax['is_rtb']

# 需要除以100的百分比字段
for column in ['完看率', '跳过率', '复播广告后问正确提及品牌', '复播广告前问正确提及品牌', '购买意向']:
    full[column] = full[column] / 100

# 继续处理剩余字段
# 注意：以下是假设所有其他字段都是直接赋值。如果有些字段需要特殊处理，请添加逻辑。
fields_to_copy_directly = [
    'is_digital_testimony',
    'is_frame',
    'frame_position',
    'is_splitscreen',
    'visual_center',
    'protagonist_num',
    'is_introduce_product',
    'scene_num',
    'protagonist_nationality'
]

for field in fields_to_copy_directly:
    full[field] = full[field]

# 特殊处理的字段（例如需要除以100等）
# 这里已经处理了“完看率”等几个百分比字段，如果还有其他需要特殊处理的字段，请在这里添加

# 处理分类变量
categorical_fields_to_convert = [
    # 填入需要转换为分类变量的列名列表
]

for field in categorical_fields_to_convert:
    full[field] = full[field].astype('category')

# 请根据实际情况填写上面两个列表，并继续添加其他所有剩余的变量。

# 创建稀疏矩阵 (请注意，这里可能需要根据实际情况调整)
categorical_features = full.columns[9:11].tolist() + full.columns[27:34].tolist() + ['其他分类特征']
full_categorical = full[categorical_features]
ohe = OneHotEncoder(sparse=True)
oh_encoded = ohe.fit_transform(full_categorical)

# 将稀疏矩阵与其他特征合并（这里假设其他特征已经是数值型）
numerical_features = full.columns[36].tolist() + full.columns[59:67].tolist() + ['其他数值型特征']
full_numerical = full[numerical_features]
x = csr_matrix(pd.concat([full_numerical, oh_encoded], axis=1))

# 分割数据集为训练集和测试集
y = full['完看率'].values
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=20221218)

# 训练XGBoost模型（参数调整可以使用GridSearchCV或者RandomizedSearchCV）
model = XGBRegressor(objective='reg:logistic', eval_metric='mae')
model.fit(X_train, y_train)

# 预测和评估模型性能
preds = model.predict(X_test)
mae = np.mean(np.abs(preds - y_test))
mse = np.mean((preds - y_test) ** 2)
rmse = np.sqrt(mse)

# 输出结果到CSV文件
importance_df = pd.DataFrame(model.feature_importances_, index=ohe.get_feature_names_out())
importance_df.to_csv('importance.csv')

predictions_df = pd.DataFrame({'pred': preds, 'rate': y_test})
predictions_df.to_csv('report.csv')

# 打印评价指标结果
print(f'MAE: {mae}, MSE: {mse}, RMSE: {rmse}')

# 可视化特征重要性（如果需要）
plot_importance(model)
