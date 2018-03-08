# coding : UTF-8

import requests
import csv
import random
import time
import socket
import http.client
import urllib.request
from bs4 import BeautifulSoup

def get_content(url , data = None):
    header={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'zh-CN,zh;q=0.8','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'}
    timeout = random.choice(range(80,180))

    try:
        rep = requests.get(url,headers = header,timeout = timeout)
        rep.encoding ='utf-8'
        time.sleep(random.choice(range(8,15)))
    except socket.error as e:
        print('4:', e)
        time.sleep(random.choice(range(20,60)))
    except http.client.BadStatusLine as e:
        print('5:', e)
        time.sleep(random.choice(range(30,80)))
    except http.client.IncompleteRead as e:
        print('6:', e)
        time.sleep(random.choice(range(5,15)))
    return rep.text

def get_data(html_text):
    final = []
    bs = BeautifulSoup(html_text,"html.parser")# 创建BeautifulSoup对象
    body = bs.body# 获取body部分
    data = body.find('div', {'id':'7d'})# 找到id为7d的div
    ul = data.find('ul')# 获取ul部分
    li = ul.find_all('li')# 获取所有的li
    for day in li:# 对每个li标签中的内容进行遍历
        temp = []
        date = day.find('h1').string# 找到日期
        # print(date)
        temp.append(date)# 添加到temp中
        inf = day.find_all('p')# 找到li中的所有p标签
        temp.append(inf[0].string,)# 第一个p标签中的内容（天气状况）加到temp中
        # if inf[1].find('span')is None:
        #     temperature_highest =None# 天气预报可能没有当天的最高气温（到了傍晚，就是这样），需要加个判断语句,来输出最低气温
        # else:
        temperature_highest = day.find('span').string# 找到最高温
        temperature_highest = temperature_highest.replace('℃','')# 到了晚上网站会变，最高温度后面也有个℃
        print('11111111111111',temperature_highest)
        temperature_lowest = day.find('i').string# 找到最低温
        print(temperature_lowest)

        temperature_lowest = temperature_lowest.replace('℃','')# 最低温度后面有个℃，去掉这个符号
        temp.append(temperature_highest)# 将最高温添加到temp中
        temp.append(temperature_lowest)#将最低温添加到temp中
        final.append(temp)#将temp加到final中
    return final

def write_data(data, name):
    file_name = name
    with open(file_name,'a', errors='ignore', newline='')as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)

if __name__ == '__main__':
    url ='http://www.weather.com.cn/weather/101190401.shtml'
    html = get_content(url)
    result = get_data(html)
    print(result)
    write_data(result,'weather.csv')