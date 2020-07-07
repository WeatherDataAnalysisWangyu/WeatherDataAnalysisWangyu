import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
import seaborn as sns
import datetime

import pmdarima as pm
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.tsa.stattools as st
from mod_timeseries.weather_model import ProcessData
import csv

# file_name = input("输入日期：")
# file_name = "temp-" + file_name + ".csv"
# data = pd.read_csv(file_name, parse_dates=['date'])
# datatype = input("输入数据类型：")
# datatype = 'tmin'
# dta = data[datatype]
# dta_year = data['date']

data = pd.read_csv('washed_data\\1-1.csv', parse_dates=['date'])
datatype = 'tmin'
dta = data[datatype]
dta_year = data['date']

# 得到开始年份和结束年份
begin_year = dta_year[0:1].dt.year
end_year = dta_year[-1:].dt.year
print(begin_year.values[0], end_year.values[0])

# 设置数据类型
dta = np.array(dta, dtype=np.float)
# 转换为Series类型的一位数组
dta = pd.Series(dta)
# 改索引为年份
dta.index = pd.Index(sm.tsa.datetools.dates_from_range(str(begin_year.values[0]), str(end_year.values[0])))
dta.plot(figsize=(10, 6))
plt.show()

# 1阶差分
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(111)
diff1 = dta.diff(1)
diff1.plot(ax=ax1)
plt.show()
diff1.dropna(inplace=True)  # 去除nan值
# 二阶差分
fig = plt.figure(figsize=(12, 8))
ax2 = fig.add_subplot(111)
diff2 = dta.diff(2)
diff2.plot(ax=ax2)
plt.show()
diff2.dropna(inplace=True)  # 去除nan值
# # 三阶差分
# fig = plt.figure(figsize=(12, 8))
# ax3 = fig.add_subplot(111)
# diff3 = dta.diff(3)
# diff3.plot(ax=ax3)
# plt.show()
# diff3.dropna(inplace=True)  # 去除nan值



# 输出原数据 差分数据
# print(dta)
# print(diff1)
# print(diff2)
# print(diff3)

# 用单位根检验确定参数d
print(sm.tsa.stattools.adfuller(dta))  # 原数据进行单位根检验
print(sm.tsa.stattools.adfuller(diff1))  # 一阶单位根检验
print(sm.tsa.stattools.adfuller(diff2))  # 二阶单位根检验
# print(sm.tsa.stattools.adfuller(diff3))  # 三阶单位根检验
# 确定d
d = int(input("输入d："))
final_data = dta
if d == 0:
    final_data = dta
elif d == 1:
    final_data = diff1
else:
    final_data = diff2

# 检验ACF PACF 图

fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(final_data, lags=30, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(final_data, lags=30, ax=ax2)
plt.show()

# 利用标准BIC（贝叶斯信息准备）找出标准的最优参数p，q
import itertools

p_min = 0
d_min = 0
q_min = 0
p_max = 8
d_max = 0
q_max = 8
# Initialize a DataFrame to store the results
results_bic = pd.DataFrame(index=['AR{}'.format(i) for i in range(p_min, p_max + 1)],
                           columns=['MA{}'.format(i) for i in range(q_min, q_max + 1)])
for p, d, q in itertools.product(range(p_min, p_max + 1),
                                 range(d_min, d_max + 1),
                                 range(q_min, q_max + 1)):
    if p == 0 and d == 0 and q == 0:
        results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = np.nan
        continue

    # 这里修改数据，即选择原数据还是n阶差分数据
    try:
        model = sm.tsa.ARIMA(final_data, order=(p, d, q),
                             # enforce_stationarity=False,
                             # enforce_invertibility=False,
                             )
        results = model.fit()
        results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = results.bic
    except:
        continue
results_bic = results_bic[results_bic.columns].astype(float)
print(results_bic)
# 给出参数检验图像,确定选择参数
fig, ax = plt.subplots(figsize=(10, 8))
ax = sns.heatmap(results_bic,
                 mask=results_bic.isnull(),
                 ax=ax,
                 annot=True,
                 fmt='.2f',
                 )
ax.set_title('BIC')
plt.show()



#自动判定最佳pq值
model = pm.auto_arima(dta, start_p=1, start_q=1,
                      start_P=1,start_Q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=30, max_q=30, # maximum p and q
                      max_P=30,max_Q=30,
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=False,   # No Seasonality
                      # start_P=0,
                      D=0,
                      max_D=5,
                      trace=True,
                      error_action='ignore',
                      suppress_warnings=True,
                      stepwise=False)

print(model.summary())


# 使用模型ARMA
# 给p q 赋值
# p = int(input("输入p："))
# q = int(input("输入q："))
p=7
q=6
arma_mod76 = sm.tsa.ARMA(final_data, (p, q)).fit(disp=False)
print("arma_mod76:", arma_mod76.aic, arma_mod76.bic, arma_mod76.hqic)
# arma_mod71 = sm.tsa.ARMA(diff2, (0, 1)).fit(disp=False)
# print("arma_mod71:", arma_mod71.aic, arma_mod71.bic, arma_mod71.hqic)
# arma_mod86 = sm.tsa.ARMA(diff2, (8, 0)).fit(disp=False)
# print("arma_mod86:", arma_mod86.aic, arma_mod86.bic, arma_mod86.hqic)


# 模型检验
# 在指数平滑模型下，观察ARIMA模型的残差是否是标准正态分布  N（0，1）
# 同时观察连续残差是否（自）相关。
# 这里对ARMA（7，6）的残差做自相关图
resid = arma_mod76.resid
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=30, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(resid, lags=30, ax=ax2)
plt.show()

# 观察残差是否符合正态分布
# 使用QQ图，它用于直观验证一组数据是否来自某个分布，或者验证某两组数据是否来自同一（族）分布。
# 看点是否集中在一条线上
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
fig = qqplot(resid, line='q', ax=ax, fit=True)
plt.show()

# 未来10年同一天的预测数据
predict_year = 10
predict_end_year = end_year.values[0] + predict_year
predict_dta = arma_mod76.predict(str(end_year.values[0]), str(predict_end_year), dynamic=True)
# print(type(predict_dta))
print(predict_dta)
dta.plot(figsize=(10, 6))
predict_dta.plot(figsize=(10, 6))
plt.show()

# #生成可靠区间（置信区间）图
# fig, ax = plt.subplots(figsize=(12, 8))
# ax = dta.ix[str(begin_year.values[0]):].plot(ax=ax)
# fig = arma_mod71.plot_predict(str(end_year.values[0]), str(predict_end_year), dynamic=True, ax=ax, plot_insample=False)
# plt.show()

p = ProcessData(data, 10, 'min', 7, 6)
p.process_minmax()




