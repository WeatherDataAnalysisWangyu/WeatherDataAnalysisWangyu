import json

import pandas as pd
import numpy as np
from pmdarima.arima import auto
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
from clean.data_wash import clean_appointed_day


def read_file(area, month, day):
    file_name = 'washed_data\\'
    file_name = file_name + area + '-' + str(month) + '-' + str(day) + ".csv"
    # print(file_name)
    data = pd.read_csv(file_name, parse_dates=['date'])
    return data


def get_p_d_q(dta):
    min_bic = 10000
    min_p = 0
    min_q = 0
    for p in range(2, 5):
        for q in range(2, 5):
            try:
                arma_mod = sm.tsa.ARMA(dta, (p, q)).fit(disp=False)
                print(p, q, arma_mod.bic)
                if arma_mod.bic < min_bic:
                    min_bic = arma_mod.bic
                    min_p = p
                    min_q = q
            except:
                print('跳过')
    print(min_p, min_q, min_bic)
    # p=5
    # q=5
    # for i in range(1,10):
    #     try:
    #         arma_mod = sm.tsa.ARMA(dta, (p, q)).fit(disp=False)
    #
    #         break;
    #     except:
    #         p=p+1
    #         print('跳过')

    return min_p, 0, min_q


# 计算所有日期的pq值并记录
def save_pq(area, month, day, type):
    clean_appointed_day(area, month, day)
    # 读文件 初始化
    data = read_file(area, month, day)
    datatype = type
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
    print(dta)

    # 获得pdq
    p_q_d = get_p_d_q(dta)
    filename = area + '-pq-' + datatype + '.txt'
    with open(filename, 'a') as file_object:
        file_object.write(str(month) + "-" + str(day) + " " + str(p_q_d[0]) + " " + str(p_q_d[2]) + "\n")
    file_object.close()


def readPQ(filename):
    dic = {}

    with open(filename, 'r') as f:
        while 1:
            read_data = f.readline()
            if not read_data:
                break;
            result = read_data.split()
            # print(result)
            dic[result[0]] = str(result[1]) + str(result[2])
    f.close()
    # print(dic)
    return dic


# 预测2020年一天
def get_predict(area, month, day, type):
    clean_appointed_day(area, month, day)
    # 读文件 初始化
    data = read_file(area, month, day)
    datatype = type
    dta = data[datatype]
    dta_year = data['date']

    # 得到开始年份和结束年份
    begin_year = dta_year[0:1].dt.year
    end_year = dta_year[-1:].dt.year
    # print(begin_year.values[0], end_year.values[0])

    # 设置数据类型
    dta = np.array(dta, dtype=np.float)
    # 转换为Series类型的一位数组
    dta = pd.Series(dta)
    # 改索引为年份
    dta.index = pd.Index(sm.tsa.datetools.dates_from_range(str(begin_year.values[0]), str(end_year.values[0])))
    # print(dta)

    # # 1阶差分
    # diff1 = dta.diff(1)
    # diff1.dropna(inplace=True)  # 去除nan值
    # # 二阶差分
    # diff2 = dta.diff(2)
    # diff2.dropna(inplace=True)  # 去除nan值

    # 获得pdq
    temp = readPQ(area + '-pq-' + type + '.txt')
    p = int(temp[str(month) + '-' + str(day)]) // 10
    q = int(temp[str(month) + '-' + str(day)]) % 10
    arma_mod = sm.tsa.ARMA(dta, (p, q)).fit(disp=False)

    # 未来10年同一天的预测数据
    predict_year = 10
    predict_end_year = end_year.values[0] + predict_year
    predict_dta = arma_mod.predict(str(end_year.values[0]), str(predict_end_year), dynamic=True)
    return predict_dta[9]


def predict_7_days(area, month, day, type):
    # 生成一个现在时间日期类型
    time_ = datetime.datetime(2020, month, day)
    predict = {}
    for i in range(1, 8):
        temp = time_ + datetime.timedelta(days=i)
        # print(int(temp.month), int(temp.day))
        # predict.append(get_predict('Beijing', int(temp.month), int(temp.day), type))
        predict[str(temp.date())]=get_predict('Beijing', int(temp.month), int(temp.day), type)
    print(predict)
    json_transfer(predict,type)
    pic_save(predict,type)

def json_transfer(temp,type):
    with open("predict_file\\"+type+"-record.json", "w") as f:
        j = json.dumps(temp)
        f.write(j)
        print("加载入文件完成...")
    f.close()
def pic_save(data,type):
    temp = pd.Series(data)
    temp.plot(figsize=(10, 6))
    plt.savefig("predict_file\\"+type+'-one_week.png', dpi=100)
    plt.show()


predict_7_days('Beijing',7,1,'tmin')
predict_7_days('Beijing',7,1,'tmax')




# #31  1 3 5 7 8 10 12
# for i in range(1,32):
#     save_pq('Beijing',1,i,'tmax')
# for i in range(1, 29):
#     save_pq('Beijing', 2, i, 'tmax')
# for i in range(1, 32):
#     save_pq('Beijing', 3, i, 'tmax')
# for i in range(1,31):
#     save_pq('Beijing',4,i,'tmax')
# for i in range(1,32):
#     save_pq('Beijing',5,i,'tmax')
# for i in range(1,31):
#     save_pq('Beijing',6,i,'tmax')
# for i in range(1,32):
#     save_pq('Beijing',7,i,'tmax')
# for i in range(1,32):
#     save_pq('Beijing',8,i,'tmax')
# for i in range(1,31):
#     save_pq('Beijing',9,i,'tmax')
# for i in range(1,32):
#     save_pq('Beijing',10,i,'tmax')
# for i in range(1,31):
#     save_pq('Beijing',11,i,'tmax')
# for i in range(1,32):
#     save_pq('Beijing',12,i,'tmax')
