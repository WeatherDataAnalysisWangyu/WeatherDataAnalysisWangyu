
import pandas as pd
from datetime import datetime
from dateutil import parser

def clean():
    # 读取数据
    data_raw = pd.read_csv('2199220.csv', encoding='utf-8')

    # data_raw['name']= data_raw['NAME']

    data_raw['date'] = data_raw['DATE'].apply(parser.parse)  # 把DATE列解析成日期格式

    data_raw['tmax'] = data_raw['TMAX'].astype(float)#变量转换为float

    data_raw['tmin'] = data_raw['TMIN'].astype(float)

    # data_raw['tavg'] = data_raw['TAVG'].astype(float)

    # 得到数据后,过滤空值

    data = data_raw.loc[:, ['date', 'tmax', 'tmin']]  # 筛选出需要的三个列
    # data = data_raw.loc[:, ['name','date', 'tmax', 'tmin','tavg']]  # 筛选出需要的三个列

    # 过滤空值
    data = data[(pd.Series.notnull(data['tmax'])) & (pd.Series.notnull(data['tmin']))]
    return data



#测试,获取每年6.1的最高最低气温
data =clean()

data = data[(data['date'] >= datetime(1981, 1, 1)) & (data['date'] <= datetime(2020, 1, 1))]

data.query("date.dt.day ==1 & date.dt.month==7",inplace =True)#得到历史上每年6.1的数据

#把最终结果写入csv文件
data.to_csv('temp-7-1.csv',index=None)