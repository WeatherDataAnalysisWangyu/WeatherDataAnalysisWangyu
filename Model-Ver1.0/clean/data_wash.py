import pandas as pd
from datetime import datetime
from dateutil import parser


def clean(area):
    # 读取数据
    data_raw = pd.read_csv('D:\\Python Code\\PycharmProjects\\weatherDataAnalysis\\mod_timeseries\\origin_data\\' + area + '.csv',
                           encoding='utf-8')

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



def clean_appointed_day(area, month, day):
    data = init(area)
    temp = "date.dt.day ==" + str(day) + " & date.dt.month==" + str(month)
    data.query(temp, inplace=True)  # 得到历史上每年month.day的数据
    filename = "..\\mod_timeseries\\washed_data\\washed_data.csv"
    data.to_csv(filename, index=None)

# clean_appointed_day("Shanghai",1,5)