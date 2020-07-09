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


# 读取文件
def read_file(area, month, day):
    # file_name = 'washed_data\\'
    # file_name = file_name + area + '-' + str(month) + '-' + str(day) + ".csv"
    file_name = 'washed_data\\washed_data.csv'
    # print(file_name)
    data = pd.read_csv(file_name, parse_dates=['date'])
    return data



# 从事先确定好的pq文件中读取相应pq
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


# 预测2020年的指定日期
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

    # 获得pdq
    temp = readPQ('pq\\'+area + '-pq-' + type + '.txt')
    p = int(temp[str(month) + '-' + str(day)]) // 10
    q = int(temp[str(month) + '-' + str(day)]) % 10
    arma_mod = sm.tsa.ARMA(dta, (p, q)).fit(disp=False)

    # 未来10年同一天的预测数据
    predict_year = 10
    predict_end_year = end_year.values[0] + predict_year
    predict_dta = arma_mod.predict(str(end_year.values[0]), str(predict_end_year), dynamic=True)
    return predict_dta[9]


# 转换成json格式并写入文件
def json_transfer(temp, type):
    with open("predict_file\\" + type + "-record.json", "w") as f:
        j = json.dumps(temp)
        f.write(j)
        # print("加载入文件完成...")
    f.close()


# 保存图片
def pic_save(data, type):
    plt.cla()
    temp = pd.Series(data)
    temp.plot(figsize=(10, 6))
    plt.savefig("predict_file\\" + type + '-one_week.png', dpi=100)
    # plt.show()


# 最终接口，前端只需要调用这个。即可生成未来最低温最高温数据
def predict_7_days(area_cn, month, day):
    area_dic={'北京':'Beijing','长春':'Changchun','杭州':'Hangzhou','哈尔滨':'Harbin','呼和浩特':'Hohhot','济南':'Jinan','兰州':'Lanzhou'
                 ,'上海':'Shanghai','沈阳':'Shenyang','石家庄':'Shijiazhuang','太原':'Taiyuan','乌鲁木齐':'Wulumuqi','银川':'Yinchuan','长沙':'Changsha'
                 ,'成都':'Chengdu','福州':'Fuzhou','广州':'Guangzhou','贵阳':'Guiyang','海口':'Haikou','合肥':'Hefei','昆明':'Kunming','拉萨':'Lhasa'
                 ,'南昌':'Nanchang','南京':'Nanjing','南宁':'Nanning','武汉':'Wuhan','西安':'Xian','西宁':'Xining','郑州':'Zhengzhou'}
    area=area_dic[area_cn]
    # 最低温
    time_ = datetime.datetime(2020, month, day)
    predict = {}
    for i in range(1, 8):
        temp = time_ + datetime.timedelta(days=i)
        predict[str(temp.date())] = get_predict(area, int(temp.month), int(temp.day), 'tmin')
    print(predict)
    json_transfer(predict, 'tmin')
    pic_save(predict, 'tmin')

    # 最高温
    time_ = datetime.datetime(2020, month, day)
    predict = {}
    for i in range(1, 8):
        temp = time_ + datetime.timedelta(days=i)
        predict[str(temp.date())] = get_predict(area, int(temp.month), int(temp.day), 'tmax')
    print(predict)
    json_transfer(predict, 'tmax')
    pic_save(predict, 'tmax')

