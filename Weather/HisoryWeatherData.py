# encoding=utf-8
import codecs
import requests
import json
import pymongo
import time

def request(year, month,idNumber):
    url = "http://d1.weather.com.cn/calendar_new/"+ year+ "/" +str(idNumber)+"_"+year+month+".html?_=1495685758174"
    print(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        "Referer": "http://www.weather.com.cn/weather40d/101280701.shtml",
    }
    return requests.get(url,headers=headers)

def parse(res):
    time.sleep(10)
    json_str = res.content.decode(encoding='utf-8')[11:] #获取数据
    print(json_str)
    return json.loads(json_str)  ##解析json数据

def save(list):
    subkey = {'date': '日期','hmax': '最高温度', 'hmin': '最低温度', 'hgl': '湿度', 'wk': '星期', 'time': '发布时间'}  ##, 'fe': '节日'
    CityInfo={'城市ID': idNumber,'城市名称': idName}

    for dict in list:
        subdict = {value: dict[key] for key, value in subkey.items()}   #提取原字典中部分键值对，并替换key为中文
        subdict.update(CityInfo)  #加入城市ID
        forecast.insert_one(subdict)      #插入mongodb数据库

def getInfo():
    year = "2018"
    month = "01"  ##增量数据收集，手动修改月份

    # #全量收集，直接打开月份注释即可
    # month=1
    # for i in range(month, 13):
    #     month = str(i) if i > 9 else "0" + str(i)  # 小于10的月份要补0
    save(parse(request(year, month,idNumber)))




if __name__ == '__main__':

    # client = pymongo.MongoClient('172.28.171.13', 27017)   # 连接mongodb,端口27017 正式数据库
    client = pymongo.MongoClient('localhost', 27017)   # 连接mongodb,端口27017
    test = client['WeatherData']                              # 创建数据库文件test
    forecast = test['HistoryData2018']                        # 创建表forecast
    inforead = codecs.open("list_CityId.txt", 'r', 'utf-8')   ##打开城市ID列表文件
    idNumber = inforead.readline().rstrip('\r\n')   ##读城市列表
    nameforead = codecs.open("list_CityName.txt", 'r', 'utf-8')  ##打开城市名称列表文件
    idName = nameforead.readline().rstrip('\r\n')  ##读城市名称

    while idNumber != "":
        idNumber = idNumber.rstrip('\r\n')
        idName=idName.rstrip('\r\n')
        try:
            getInfo()
            time.sleep(3)
        except :
            print('IP被封1，程序休息当前ID为：' + idNumber)
            time.sleep(600)
            try:
                getInfo()
                time.sleep(3)
            except :
                print('IP被封2，程序休息当前ID为：' + idNumber)
                time.sleep(3600)
                try:
                    getInfo()
                    time.sleep(3)
                except :
                    pass
                    print("IP被封"+ idNumber)
        idNumber=inforead.readline()
        idName=nameforead.readline()