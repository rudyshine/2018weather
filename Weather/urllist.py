# encoding=utf-8
import codecs
import requests
import json
import pymongo
import time
import pandas as pd


inforead = codecs.open("urllist_ID.txt", 'r', 'utf-8')
idNumber = inforead.readline()
while idNumber != "":
    idNumber = idNumber.rstrip('\r\n')
    year = "2016"
    month = 1
    url = "http://d1.weather.com.cn/calendar_new/" + year + "/" + str(idNumber) + "_" + str(year) + str(month) + ".html?_=1513081038706"
    print(url)
    file = codecs.open("urllist.txt", "w")
    file.write(url)
    file.close()
    idNumber = inforead.readline()
        # request(year, month,idNumber)
        # time.sleep(3)
print('zz')