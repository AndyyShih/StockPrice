import requests
import json , csv
import pandas as pd
import os
import matplotlib.pyplot as plt

def convertDate(date): 
    str1 = str(date)
    yearstr = str1[:3] #取出民國年份
    realyear = str(int(yearstr) + 1911) #轉為西元年分份
    realdate = realyear + str1[4:6] + str1[7:9] #組合年月日
    return realdate

pd.options.mode.chained_assignment = None #取消顯示padas資料重設警告

SearchDate = input("請輸入搜尋年月:")
StockNumber = input("請輸入股票代碼:")
filename = str(StockNumber) + '-' + str(SearchDate) +'.csv'

if not os.path.isfile(filename): #如果檔案不存在，建立檔案
    url_head = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='
    url_date = str(SearchDate)
    url_mid = '01&stockNo='
    url_nuber = str(StockNumber)
    url_tail = '&_=1577941266315'
    url_twse = url_head + url_date + url_mid + url_nuber + url_tail
    res = requests.get(url_twse) #回傳為json資料
    jdata = json.loads(res.text) #json解析

    outputfile = open(filename , 'w' , newline='' , encoding='utf-8-sig') #開啟儲存檔案
    outputwriter = csv.writer(outputfile)
    outputwriter.writerow(jdata['fields'])

    for dataline in (jdata['data']): #寫入資料
        outputwriter.writerow(dataline)
    outputfile.close() #關閉檔案

pdstock = pd.read_csv(filename , encoding='utf-8-sig')
for i in range(len(pdstock['日期'])): #轉換日期格式
    pdstock['日期'][i] = convertDate(pdstock['日期'][i])
#繪製統計圖
pdstock.plot(kind= 'line' , figsize=(12,6) , x = '日期' , y = ['收盤價','最低價','最高價'])
plt.title(str(SearchDate) + "股價資料", fontproperties="SimSun", fontsize = 30)
plt.xlabel("日期", fontproperties="SimSun", fontsize = 30)
plt.ylabel("股價", fontproperties="SimSun", fontsize = 30)

plt.savefig('./' + str(SearchDate) + '股價資料.jpg') #儲存統計圖
plt.show()