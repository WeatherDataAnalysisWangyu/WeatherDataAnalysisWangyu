import pandas as pd
from datetime import datetime
from dateutil import parser


def clean(area):
    # 读取数据
    data_raw = pd.read_csv('D:\\Python Code\\PycharmProjects\\weatherDataAnalysis\\clean\\'+area+'.csv', encoding='utf-8')

    # data_raw['name']= data_raw['NAME']

    data_raw['date'] = data_raw['DATE'].apply(parser.parse)  # 把DATE列解析成日期格式

    data_raw['tmax'] = data_raw['TMAX'].astype(float)  # 变量转换为float

    data_raw['tmin'] = data_raw['TMIN'].astype(float)

    # data_raw['tavg'] = data_raw['TAVG'].astype(float)

    # 得到数据后,过滤空值

    data = data_raw.loc[:, ['date', 'tmax', 'tmin']]  # 筛选出需要的三个列
    # data = data_raw.loc[:, ['name','date', 'tmax', 'tmin','tavg']]  # 筛选出需要的三个列

    # 过滤空值
    data = data[(pd.Series.notnull(data['tmax'])) & (pd.Series.notnull(data['tmin']))]
    return data


# 筛选出1981到2012的日期
def init(area):
    dta = clean(area)
    dta = dta[(dta['date'] >= datetime(1981, 1, 1)) & (dta['date'] <= datetime(2012, 12, 31))]
    return dta

#清洗所有数据
def cleanAll():
    area='Beijing'
    month = range(1, 13)
    day = range(1, 32)
    for i in range(0, 12):
    # print(type(month[i]))
        choose_month = month[i]
        if choose_month in [1, 3, 5, 7, 8, 10, 12]:
            for j in range(0, 31):
                data = init(area)
                choose_day = day[j]
                print(choose_month, '-', choose_day)
                temp = "date.dt.day ==" + str(choose_day) + " & date.dt.month==" + str(choose_month)
                data.query(temp, inplace=True)  # 得到历史上每年6.1的数据
                # 把最终结果写入csv文件
                filename = "washed_data\\" + str(choose_month) + "-" + str(choose_day) + ".csv"
                data.to_csv(filename, index=None)
        elif choose_month in [4, 6, 9, 11]:
            for j in range(0, 30):
                data = init(area)
                choose_day = day[j]
                print(choose_month, '-', choose_day)
                temp = "date.dt.day ==" + str(choose_day) + " & date.dt.month==" + str(choose_month)
                data.query(temp, inplace=True)  # 得到历史上每年6.1的数据
                # 把最终结果写入csv文件
                filename = "washed_data\\" + str(choose_month) + "-" + str(choose_day) + ".csv"
                data.to_csv(filename, index=None)
        else:
            for j in range(0, 28):
                data = init(area)
                choose_day = day[j]
                print(choose_month, '-', choose_day)
                temp = "date.dt.day ==" + str(choose_day) + " & date.dt.month==" + str(choose_month)
                data.query(temp, inplace=True)  # 得到历史上每年6.1的数据
                # 把最终结果写入csv文件
                filename = "washed_data\\" + str(choose_month) + "-" + str(choose_day) + ".csv"
                data.to_csv(filename, index=None)
# 清洗指定数据
def clean_appointed_day(area,month,day):
    data =init(area)
    temp = "date.dt.day ==" + str(day) + " & date.dt.month==" + str(month)
    data.query(temp, inplace=True)  # 得到历史上每年month.day的数据
    filename = "..\\mod_timeseries\\washed_data\\" + area + '-' + str(month) + "-" + str(day) + ".csv"
    data.to_csv(filename, index=None)
# data.query("date.dt.day ==28 & date.dt.month==7",inplace =True)#得到历史上每年6.1的数据
#
# #把最终结果写入csv文件
# data.to_csv('washed_data\\temp-7-28.csv',index=None)

# clean_appointed_day('Beijing',1,1)