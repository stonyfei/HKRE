#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Stony'

import urllib3
from bs4 import BeautifulSoup
http = urllib3.PoolManager()
url = http.request('GET', 'hk.centadata.com/ccichart/estate_info.aspx?id=000010')


'''
print(url.data)
'''
import re
import codecs


soup = BeautifulSoup(url.data)
estatename = soup.find(id=re.compile("EstateName")).get_text(strip=True)
address = soup.find_all(id=re.compile("EstateAddress"))
age = soup.find_all(id=re.compile("BuildingAge"))
registdate = soup.find_all(id=re.compile("RegistDate"))
transactionprice = soup.find_all(id=re.compile("TransactionPrice"))
conarea = soup.find_all(id=re.compile("ConArea"))
realarea = soup.find_all(id=re.compile("RealArea"))
conunitprice = soup.find_all(id=re.compile("ConUnitPrice"))

num = len (age)

alldata = [[0] * 11 for i in range(num)]

for i in range(num):
    alldata[i][0] = estatename

k = 0
for tag in address:
    t= tag.contents[0]
    s = t.string
    ss = s.split(' ')
    for p in range (0,4):
        alldata[k][p+1] = ss[p]
    k = k + 1

k = 0
for tag in age:
    t= tag.contents[0]
    s = t.string
    alldata[k][5] = s
    k = k + 1

k = 0
for tag in registdate:
    t= tag.contents[0]
    s = t.string
    twoo = '20'
    s = s[:6] + twoo + s[6:]
    alldata[k][6] = s
    k = k + 1

k = 0
for tag in transactionprice:
    t= tag.contents[0]
    s = t.string
    s = s.replace('HK$','')
    s = s.replace('萬','')
    alldata[k][7] = s
    k = k + 1

k = 0
for tag in conarea:
    t= tag.contents[0]
    s = t.string
    s = s.replace('呎','')
    alldata[k][8] = s
    k = k + 1

k = 0
for tag in realarea:
    t= tag.contents[0]
    s = t.string
    s = s.replace('呎','')
    alldata[k][9] = s
    k = k + 1

k = 0
for tag in conunitprice:
    t= tag.contents[0]
    s = t.string
    s = s.replace('HK$','')
    alldata[k][10] = s
    k = k + 1

print(alldata)

import csv

headers = ['Estate','Phase','Block','Floor','Flat','Age','Date','Price','Construction Area','Real Area', 'Unit Price']
csvfile = codecs.open( 'HKRE.csv', 'wb+', encoding='utf-8')
csvfile.stream.write(codecs.BOM_UTF8)
csvwriter = csv.writer(csvfile,dialect='excel')
csvwriter.writerow(headers)
alldata = reversed(alldata)
csvwriter.writerows(alldata)
