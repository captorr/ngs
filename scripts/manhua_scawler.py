# -*- coding: UTF-8 -*-
"""
Author: Zhang Chengsheng, @2018.03.03
"""

import os,sys,time
import re
from bs4 import BeautifulSoup
import requests

file_out = 'D:\\zcs-genex\\180303\\t.jpg'




home_page = 'http://manhua.fzdm.com/058/'
rq = requests.get(url=home_page)
r = BeautifulSoup(rq.content,'lxml')
#print(str(r))

regu1 = '<li class="pure-u-1-2 pure-u-lg-1-4">(.*?)</a></li>'
regu2 = '"(.*?)"'
re1 = re.compile(regu1)
re2 = re.compile(regu2)
sites = re1.findall(str(r))



for i in sites:
    a = re2.findall(i)
    if len(a) == 2:
        url_1 = a[0]
        name = a[1]
        print(url_1,name)
        url_all = home_page + url_1
        rq1 = requests.get(url_all)
        r1 = BeautifulSoup(rq1.content,'lxml')
        s1 = re.compile('img.src="(.*?)"\\+mhurl').findall(str(r1))
        s2 = re.compile('var mhurl = "(.*?)"').findall(str(r1))
        page = re.compile('id="mhona">(.*?)</a><a href').findall(str(r1))[0]
        file_name = page + '.jpg'
        s = s1[0] + s2[0]

        print(s)
    break

    