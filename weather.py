#!/usr/bin/python
from twilio.rest import Client
import bs4,requests,pprint
import re


def textMyself(message): # 通过 twilio 库实现短信发送功能
    accountSID = 'ACa4xxxxxxec33ca369axxx189xxx'
    authTorken = '3xx1xxb1705xxxfb7f5b727xxxx'
    myTwilioNumber = '+1256xxxxxx3'
    myCellPhone = '+8618xxxxxxx075'
    twiloCli = Client(accountSID, authTorken)
    message = twiloCli.messages.create(body=message, from_=myTwilioNumber,
                                       to=myCellPhone)

def getHTMLText(url): # 抓取天气官网天气数据
    try:
        res = requests.get(url,timeout=30)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res.text
    except:
        return 'error'

def getWeatherList(html): # 分析天气数据，提取需要的数据
    # 通过 bs4 类获取标签 <ul class="t clearfix"> </ul> 内的天气信息 
    weatherSoup = bs4.BeautifulSoup(html,'html.parser')
    elems = weatherSoup.find('ul',attrs={'class':'t clearfix'})

    # 初始化变量
    dateList= []
    weaList=[]
    temList = []
    winList =[]
    wList = []

    # 从 elems 中二次提取数据
    date = elems.select('h1') # 日期
    wea = elems.select('.wea') # 天气
    tem = elems.select('.tem') # 温度
    win = elems.select('.win') # 风力

    # 剔除多余的标签，保留所需要的字符
    for i in date:
        dateList.append(i.text)
    for i in wea:
        weaList.append(i.text)
    for i in tem:
        temList.append(i.text.replace('\n',''))
    for i in win:
        winList.append(i.text.replace('\n',''))

    # 将提取出的数据保存在列表中
    for i in range(len(dateList)):
        d1 = dateList[i]
        w1 = weaList[i]
        t1 = temList[i]
        wi1 = winList[i]
        wList.append([d1,w1,t1,wi1])

    return wList

def printWeatherInfo(wList): # 格式化输出数据

    tplt = '\n日期: {:9}\n天气: {:9}\n温度: {:9}\n风力: {:10}' # 定义模板格式
    sessionTxt = '' # 初始化字符串，将格式化后的数据保留在其中
    for i in wList:
        print(tplt.format(i[0],i[1],i[2],i[3]))
        sessionTxt = sessionTxt + '\n' + tplt.format(i[0],i[1],i[2],i[3]) + '\n'
    return sessionTxt


def main():
    url = 'http://www.weather.com.cn/weather/101190202.shtml' #江阴天气
    html = getHTMLText(url)
    weaInfoList = getWeatherList(html)
    text = printWeatherInfo(weaInfoList)
    textMyself(text)

if __name__ == '__main__':
    main()
