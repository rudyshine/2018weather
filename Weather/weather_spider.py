import requests
import csv
import time
import codecs
import pymongo

def get_infor(idNumber,ProgramTime):
    url='http://www.weather.com.cn/data/sk/'+str(idNumber)+'.html'
    r = requests.get(url)
    r.encoding = 'utf-8'
    city=r.json()['weatherinfo']['city']
    cityid=r.json()['weatherinfo']['cityid']
    temp=r.json()['weatherinfo']['temp']
    WD=r.json()['weatherinfo']['WD']
    WS=r.json()['weatherinfo']['WS']
    SD=r.json()['weatherinfo']['SD']
    time=r.json()['weatherinfo']['time']
    print(city, cityid, temp, WD, WS, SD, time,ProgramTime)
    info_weather.insert({'城市': city, "城市ID": cityid, '温度': temp, '风向': WD, '风力': WS, '湿度': SD, '发布时间': time,'程序运行时间': ProgramTime })



if __name__ == '__main__':

    client = pymongo.MongoClient('localhost', 27017)
    WeatherData = client['WeatherData']
    info_weather = WeatherData['info_weather']
    # set = WeatherData.info_weather

    ProgramTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    #文件操作读写信息
    print('Read idNumber:')
    inforead = codecs.open("urllist_ID.txt", 'r', 'utf-8')
    idNumber = inforead.readline()
    while idNumber != "":
        idNumber = idNumber.rstrip('\r\n')
        try:
            get_infor(idNumber,ProgramTime)
        except:
            print('IP被封1，程序休息当前ID为：' + idNumber)
            time.sleep(600)
            try:
                get_infor(idNumber, ProgramTime)
            except:
                print('IP被封2，程序休息当前ID为：' + idNumber)
                time.sleep(3600)
                try:
                    get_infor(idNumber, ProgramTime)
                except:
                    print("IP被封"+ idNumber)
        idNumber = inforead.readline()

