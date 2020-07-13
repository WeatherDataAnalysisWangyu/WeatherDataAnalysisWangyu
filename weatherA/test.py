import json
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import datetime
from data_wash import clean_appointed_day
import warnings#*****
warnings.filterwarnings("ignore")#*****


# 读取文件
def read_file(area, month, day):

    file_name = 'D:\\weatherDataAnalysis\\mod_timeseries\\washed_data\\washed_data.csv'
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
    temp = readPQ('D:\\weatherDataAnalysis\\mod_timeseries\\pq\\'+area + '-pq-' + type + '.txt')
    p = int(temp[str(month) + '-' + str(day)]) // 10
    q = int(temp[str(month) + '-' + str(day)]) % 10
    arma_mod = sm.tsa.ARMA(dta, (p, q)).fit(disp=False)

    # 未来10年同一天的预测数据
    predict_year = 10
    predict_end_year = end_year.values[0] + predict_year
    predict_dta = arma_mod.predict(str(end_year.values[0]), str(predict_end_year), dynamic=True)
    # print(predict_dta[8])
    predict_dta[8]=(predict_dta[8]-32)/1.8
    # print(predict_dta[8])
    return predict_dta[8]#*****


# 转换成json格式并写入文件
def json_transfer(temp, type, area):
    # *****
    if area=='0':
        filename="E:\\weatherA\\src\\main\\resources\\static\\json\\" + type + "-record.json"
    else:
        filename="E:\\weatherA\\src\\main\\resources\\static\\json\\" +type+"\\"+ type + "-"+area+".json"

    with open(filename, "w") as f:
        j = json.dumps(temp)

        f.write(j)
        # print("加载入文件完成...")
    f.close()


# 保存图片
def pic_save(data, type):
    plt.cla()
    temp = pd.Series(data)
    temp.plot(figsize=(10, 6))
    plt.savefig("D:\\weatherDataAnalysis\\mod_timeseries\\predict_file\\" + type + '-one_week.png', dpi=100)
    plt.show()




# 最终接口，前端只需要调用这个。即可生成未来最低温最高温数据
# def predict_7_days(area_cn, month, day, type):
#     area_dic={'北京':'Beijing','长春':'Changchun','杭州':'Hangzhou','哈尔滨':'Harbin','呼和浩特':'Hohhot','济南':'Jinan','兰州':'Lanzhou'
#                  ,'上海':'Shanghai','沈阳':'Shenyang','石家庄':'Shijiazhuang','太原':'Taiyuan','乌鲁木齐':'Wulumuqi','银川':'Yinchuan','长沙':'Changsha'
#                  ,'成都':'Chengdu','福州':'Fuzhou','广州':'Guangzhou','贵阳':'Guiyang','海口':'Haikou','合肥':'Hefei','昆明':'Kunming','拉萨':'Lhasa'
#                  ,'南昌':'Nanchang','南京':'Nanjing','南宁':'Nanning','武汉':'Wuhan','西安':'Xian','西宁':'Xining','郑州':'Zhengzhou'}
#     area=area_dic[area_cn]
#     # 最低温
#     time_ = datetime.datetime(2020, month, day)
#     predict = []
#     mon_day=[]
#     for i in range(1, 8):
#         temp = time_ + datetime.timedelta(days=i)
#         mon_day.append(str(temp.month)+'-'+str(temp.day))
#         predict.append(get_predict(area, int(temp.month), int(temp.day), type))
#     print(predict)
#     record = {'temperature': predict, 'date': mon_day}
#     print(record)
#     json_transfer(record, type, '0')              #*****
#     # pic_save(predict, 'tmin')
#     #
#     # # 最高温
#     # time_ = datetime.datetime(2020, month, day)
#     # predict = []
#     # mon_day = []
#     # for i in range(1, 8):
#     #     temp = time_ + datetime.timedelta(days=i)
#     #     mon_day.append(str(temp.month)+'-'+str(temp.day))
#     #     predict.append(get_predict(area, int(temp.month), int(temp.day), 'tmax'))
#     # record = {'temperature': predict, 'date': mon_day}
#     # json_transfer(record, 'tmax', '0')  # *****
#     # # pic_save(predict, 'tmin')

def predict_7_days(area_cn, month, day):
    area_dic={'北京':'Beijing','长春':'Changchun','杭州':'Hangzhou','哈尔滨':'Harbin','呼和浩特':'Hohhot','济南':'Jinan','兰州':'Lanzhou'
                 ,'上海':'Shanghai','沈阳':'Shenyang','石家庄':'Shijiazhuang','太原':'Taiyuan','乌鲁木齐':'Wulumuqi','银川':'Yinchuan','长沙':'Changsha'
                 ,'成都':'Chengdu','福州':'Fuzhou','广州':'Guangzhou','贵阳':'Guiyang','海口':'Haikou','合肥':'Hefei','昆明':'Kunming','拉萨':'Lhasa'
                 ,'南昌':'Nanchang','南京':'Nanjing','南宁':'Nanning','武汉':'Wuhan','西安':'Xian','西宁':'Xining','郑州':'Zhengzhou'}
    area=area_dic[area_cn]
    # 最低温
    time_ = datetime.datetime(2020, month, day)
    predict = []
    mon_day=[]
    for i in range(1, 8):
        temp = time_ + datetime.timedelta(days=i)
        mon_day.append(str(temp.month)+'-'+str(temp.day))
        predict.append(get_predict(area, int(temp.month), int(temp.day), 'tmin'))
    print(predict)
    record = {'temperature': predict, 'date': mon_day}
    print(record)
    json_transfer(record, 'tmin', '0')              #*****
    # pic_save(predict, 'tmin')

    # 最高温
    time_ = datetime.datetime(2020, month, day)
    predict = []
    mon_day = []
    for i in range(1, 8):
        temp = time_ + datetime.timedelta(days=i)
        mon_day.append(str(temp.month)+'-'+str(temp.day))
        predict.append(get_predict(area, int(temp.month), int(temp.day), 'tmax'))
    record = {'temperature': predict, 'date': mon_day}
    json_transfer(record, 'tmax', '0')  # *****
    # pic_save(predict, 'tmin')


# 由于跑14个模型不够快，所以采取折中的办法。即服务器每天把当天之后一礼拜的数据跑完记录，这样在获得不同city的一周预测就快了。
# 假设要查询其他日期的就再调用predict_7_days函数实时演算
#*****
def test(area_cn, month, day):
    area_dic = {'北京': 'Beijing', '长春': 'Changchun', '杭州': 'Hangzhou', '哈尔滨': 'Harbin', '呼和浩特': 'Hohhot', '济南': 'Jinan',
                '兰州': 'Lanzhou'
        , '上海': 'Shanghai', '沈阳': 'Shenyang', '石家庄': 'Shijiazhuang', '太原': 'Taiyuan', '乌鲁木齐': 'Wulumuqi',
                '银川': 'Yinchuan', '长沙': 'Changsha'
        , '成都': 'Chengdu', '福州': 'Fuzhou', '广州': 'Guangzhou', '贵阳': 'Guiyang', '海口': 'Haikou', '合肥': 'Hefei',
                '昆明': 'Kunming', '拉萨': 'Lhasa'
        , '南昌': 'Nanchang', '南京': 'Nanjing', '南宁': 'Nanning', '武汉': 'Wuhan', '西安': 'Xian', '西宁': 'Xining',
                '郑州': 'Zhengzhou'}
    area = area_dic[area_cn]
    # 最低温
    time_ = datetime.datetime(2020, month, day)
    predict = []
    mon_day = []
    for i in range(1, 8):
        temp = time_ + datetime.timedelta(days=i)
        mon_day.append(str(temp.month) + '-' + str(temp.day))
        predict.append(get_predict(area, int(temp.month), int(temp.day), 'tmin'))
    record = {'temperature': predict, 'date': mon_day}
    print(record)
    json_transfer(record, 'tmin', area)  # *****
    # pic_save(predict, 'tmin')

    # 最高温
    time_ = datetime.datetime(2020, month, day)
    predict = []
    mon_day = []
    for i in range(1, 8):
        temp = time_ + datetime.timedelta(days=i)
        mon_day.append(str(temp.month) + '-' + str(temp.day))
        predict.append(get_predict(area, int(temp.month), int(temp.day), 'tmax'))
    record = {'temperature': predict, 'date': mon_day}
    print(record)
    json_transfer(record, 'tmax', area)  # *****
    # pic_save(predict, 'tmin')
#*****
def daily_once():
    month=datetime.datetime.now().month
    day=datetime.datetime.now().day
    print(month,day)
    area=['北京','长春','杭州','哈尔滨','呼和浩特','济南','兰州'
        ,'上海','沈阳','石家庄','太原','乌鲁木齐','银川','长沙'
        ,'成都','福州','广州','贵阳','海口','合肥','昆明','拉萨'
        ,'南昌','南京','南宁','武汉','西安','西宁','郑州']
    problem=[]
    for i in area:
        try:
            test(i,month,day)
            print(i,'完成')
        except:
            print(i,':有问题')
            problem.append(i)
    print(problem)


if __name__ == '__main__':
    a = []
    for i in range(1, len(sys.argv)):
        a.append(sys.argv[i])
    # predict_7_days(a[0], int(a[1]), int(a[2]), 'tmin')
    predict_7_days(a[0], int(a[1]), int(a[2]))
    # predict_7_days('太原', 7, 9, 'tmin')
# daily_once()
# test('乌鲁木齐',7,10)
# predict_7_days('北京', 7, 11)
# predict_7_days('北京', 7, 11, 'tmax')
