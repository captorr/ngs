# -*- coding: UTF-8 -*-
"""
Author: Zhang Chengsheng, @2018.03.03
"""

import os,sys,time
import re
from bs4 import BeautifulSoup
import requests

file_out_dir = 'E:\\manhua'

home_page = 'http://manhua.fzdm.com/058/'
rq = requests.get(url=home_page)
r = BeautifulSoup(rq.content,"html.parser") #python3.5 bs4
#r = BeautifulSoup(rq.content,"lxml") #python3.6 bs4
#print(str(r))

regu1 = '<li class="pure-u-1-2 pure-u-lg-1-4">(.*?)</a></li>'
regu2 = '"(.*?)"'
re1 = re.compile(regu1)
re2 = re.compile(regu2)
sites = re1.findall(str(r))

def get_pic(url):
    try:
        rq1 = requests.get(url)
    except:
        return 'E1'

    r1 = BeautifulSoup(rq1.content, "html.parser") #python3.5 bs4
    #r1 = BeautifulSoup(rq1.content, "lxml")  # python3.6 bs4
    if len(str(r1)) < 500:
        return 'E'
    s1 = re.compile('img.src="(.*?)"\\+mhurl').findall(str(r1))
    s2 = re.compile('var mhurl = "(.*?)"').findall(str(r1))
    page = re.compile('id="mhona">(.*?)</a><a href').findall(str(r1))[0]
    s = s1[0] + s2[0]
    # print(s)
    return s

for i in sites:
    a = re2.findall(i)
    if len(a) == 2:
        url_1 = a[0]
        name = a[1]
        print(url_1,name)
        pic_dir = file_out_dir + '\\' + str(name)
        if not os.path.exists(pic_dir):
            os.mkdir(pic_dir)
        url_all = home_page + url_1
        for page in range(30):
            url_c = url_all + 'index_' + str(page) + '.html'
            #print(url_c)
            if len(str(page)) == 1:
                page = '0' + str(page)
            file_name = str(page) + '.jpg'
            if not os.path.exists(pic_dir + '\\' + file_name):
                pic_url = get_pic(url_c)
                if pic_url == 'E':
                    break
                elif pic_url == 'E1':
                    print(str(page),'error')
                else:
                    file_name_o = open(pic_dir + '\\' + file_name, 'wb')
                    try:
                        rb = requests.get(pic_url)
                        time.sleep(0.2)
                        file_name_o.write(rb.content)
                        file_name_o.close()
                        size = os.path.getsize(pic_dir + '\\' + file_name)
                        print(str(page),'downloaded',size)
                        if not size:
                            os.remove(pic_dir + '\\' + file_name)
                            print(str(page),'removed')
                    except:
                        print(str(page),"can't downloading !!!!!")
            else:
                print(page,'pass')


