from bs4 import BeautifulSoup
import requests

url='http://www.weather.com.cn/weather/101190401.shtml'

html = requests.get(url).content
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
result = soup.find_all("ul",class_="t clearfix")
print(result)

for day in result:  # 对每个li标签中的内容进行遍历
    temp = []
    date = day.find('h1').string  # 找到日期
    temp.append(date)  # 添加到temp中
    print(date)

