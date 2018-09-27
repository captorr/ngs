"""
python3 scripts
Author: Zhang Chengsheng, @2018.09.21
"""

import os, sys, time
import requests
from bs4 import BeautifulSoup as BS
import re
from random import choice


def web_(site1):
    site = 'http://www.letpub.com.cn'
    a = requests.get(site1)
    return a.content.decode('utf8')


def context_parsing(text,home=False):
    mark = '</tr><tr style="background:#EFEFEF;">'
    text_lines = text.split('\n')
    line = [i for i in text_lines if i.startswith(mark)]
    mark1 = '</tr><tr style="background:#EFEFEF;"><td style="border:1px #DDD solid; border-collapse:collapse; text-align:left; padding:8px 8px 8px 8px; color:#3b5998; font-weight:bold;'
    res_10 = line[0].split(mark1)
    res_10 = [i for i in res_10 if i]
    res = []
    for i in res_10:
        r = re.findall("\">(.*?)</td>",i)
        r.remove('题目')
        r.remove('学科分类')
        res.append(r)
    if home:
        pages = re.findall("共(.*?)页", text)
        return res, int(pages[0])
    return res  #, int(pages)


def get_ip():
    """获取代理IP"""
    url = "http://www.xicidaili.com/nn/4"
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
                "Accept-Encoding":"gzip, deflate, sdch",
                "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
                "Referer":"http://www.xicidaili.com",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
                }
    r = requests.get(url,headers=headers)
    soup = BS(r.text, 'html.parser')
    data = soup.table.find_all("td")
    ip_compile= re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')
    port_compile = re.compile(r'<td>(\d+)</td>')
    ip = re.findall(ip_compile,str(data))
    port = re.findall(port_compile,str(data))
    return [":".join(i) for i in zip(ip,port)],time.time()


def url_get(dict1,pages='1'):
    site1 = "http://www.letpub.com.cn/index.php?page=grant&name=&person=&no=&company=&startTime=2018&endTime=2018&money1=&money2=&subcategory=&addcomment_s1=%s&addcomment_s2=%s&addcomment_s3=%s&currentpage=%s#fundlisttable" % (dict1[0],dict1[1],dict1[2],pages)
    return site1


def res_get(url,home=True,pages=1):
    global ip_list
    try:
        refresh_iplist()
        ip = choice(ip_list)
        #ip='222.174.8.187:35101'
        proxies = {"http": ip, }
        hz_r = requests.get(url_get(string_dict2[url],pages=str(pages)),proxies=proxies)
    except Exception as e:
        print(e)
        if home:
            return 404,0
        else:
            return 404

    try:
        text = hz_r.content.decode('utf8')
        if home:
            r, pn = context_parsing(text, home=home)
            res = ['\t'.join(i) for i in r]
            res = '\n'.join(res)
            return res,pn
        else:
            r = context_parsing(text, home=home)
            res = ['\t'.join(i) for i in r]
            res = '\n'.join(res)
            return res
    except Exception as e:

        try:
            print('[error1]',e,text)
        except:
            if home:
                return 404, 0
            else:
                return 404
        if '地址今日访问额度已经用完' in text:
            if home:
                return 888,0
            else:
                return 888
        else:
            if home:
                return 404, 0
            else:
                return 404


def refresh_iplist():
    global ip_list,time1
    time2 = time.time()
    if time2 - time1 > 60:
        ip_list,time1 = get_ip()


def continue2work(i,home,pages=1,count=1):
    count += 1
    if count > 50:
        if home:
            return 666,666
        else:
            return 666
    try:
        if home:
            res,pn = res_get(i, home=home, pages=pages)
        else:
            res = res_get(i, home=home, pages=pages)
        if res == 404:
            if home:
                res,pn = continue2work(i, home=home, pages=pages, count=count)
                return res,pn
            else:
                res = continue2work(i, home=home, pages=pages, count=count)
                return res
        else:
            if home:
                return res,pn
            else:
                return res
    except:
        if home:
            res, pn = continue2work(i, home=home, pages=pages, count=count)
            return res, pn
        else:
            res = continue2work(i, home=home, pages=pages, count=count)
            return res


class Config_pickle:
    def __init__(self):
        self.config = 'config_path'  # config file abspath

    def _get_list(self):
        o = open(self.config,'r')
        list1 = []
        for i in o.readlines():
            list1.append(i.strip())
        o.close()
        return list1

    def _add(self,i):
        o = open(self.config,'a+')
        o.write(i)
        o.write('\n')
        o.close()


def main():
    global ip_list,time1
    file_out = 'file_out'  # result file abspath
    ip_list,time1 = get_ip()
    #ip_list, time1 = [],0
    A = Config_pickle()

    for i in string_dict2:

        finished = A._get_list()
        print(i, ': start!')

        if i + '\t' + 'home' in finished:
            print(i,': pass!')
            continue

        res, pn = res_get(i, home=True)

        if res == 404:
            res,pn = continue2work(i, home=True, pages=1)
        if res == 666:
            print(i, ": can't link")
            continue
        if res == 888:
            print('sldfjas;ldfj!')
            exit(1)
        o = open(file_out, 'a+',encoding='utf8')
        o.write(str(res))
        o.write('\n')
        o.close()
        print(i, ': successful!')
        for pages in range(pn-1 if pn - 1 < 50 else 50):
            if i+'\t'+str(pages+2) in finished:
                continue
            res = res_get(i, home=False, pages=pages + 2)
            if res == 404:
                res = continue2work(i, home=False, pages=pages + 2)
            if res == 666:
                print(i, ": pages %s failed" % str(pages + 2))
                continue
            if res == 888:
                print('sldfjas;ldfj!')
                exit(1)
            o = open(file_out, 'a+',encoding='utf8')
            o.write(str(res))
            o.write('\n')
            o.close()
            print(i, ': pages:%s finished!' % str(pages + 2))
            A._add(i+'\t'+str(pages+2))
        else:
            A._add(i+'\t'+str(pn)+'\t'+'home')
            A._add(i + '\t' + 'home')
            print(i,'all finished!')


if __name__ == '__main__':
    string_dict1 = {
        '生理学与整合生物学': ['146', '195', '0'],
        '微生物学': ['146', '151', '0'],
        '植物学': ['146', '162', '0'],
        '生物物理、生物化学与分子生物学': ['146', '171', '0'],
        '免疫学': ['146', '181', '0'],
        '遗传学与生物信息学': ['146', '208', '0'],
        '细胞生物学': ['146', '218', '0'],
        '发育生物学与生殖生物学': ['146', '232', '0'],
        '动物学': ['146', '261', '0'],
        '生物力学与组织工程学': ['146', '279', '0'],
    }
    string_dict2 = {
        '呼吸系统': ['662', '663', '0'],
        '循环系统': ['662', '683', '0'],
        '消化系统': ['662', '708', '0'],
        '血液系统': ['662', '733', '0'],
        '生殖系统/围生医学/新生儿': ['662', '752', '0'],
        '泌尿系统': ['662', '783', '0'],
        '内分泌系统/代谢和营养支持': ['662', '803', '0'],
        '眼科学': ['662', '833', '0'],
        '耳鼻咽喉头颈科学': ['662', '846', '0'],
        '神经系统和精神疾病': ['662', '855', '0'],
        '影像医学与生物医学工程': ['662', '886', '0'],
        '皮肤及其附属器': ['662', '914', '0'],
        '运动系统': ['662', '938', '0'],
        '急重症医学/创伤/烧伤/整形': ['662', '953', '0'],
        '肿瘤学,消化系统肿瘤': ['662', '966', '973'],
        '肿瘤学,肿瘤发生': ['662', '966', '967'],
        '肿瘤学,肿瘤遗传与表观遗传': ['662', '966', '968'],
        '肿瘤学,肿瘤复发与转移': ['662', '966', '969'],
        '肿瘤学,肿瘤综合治疗': ['662', '966', '970'],
        '肿瘤学,呼吸系统肿瘤': ['662', '966', '971'],
        #'肿瘤学,血液淋巴肿瘤': ['662', '966', '972'],
        '肿瘤学,泌尿系统肿瘤': ['662', '966', '974'],
        '肿瘤学,女性生殖系统肿瘤': ['662', '966', '975'],
        '肿瘤学,乳腺肿瘤': ['662', '966', '976'],
        '肿瘤学,骨与软组织肿瘤': ['662', '966', '977'],
        '肿瘤学,肿瘤学': ['662', '966', '978'],
        '肿瘤学,肿瘤病因': ['662', '966', '979'],
        '肿瘤学,肿瘤免疫': ['662', '966', '980'],
        '肿瘤学,肿瘤干细胞': ['662', '966', '981'],
        '肿瘤学,肿瘤物理治疗': ['662', '966', '982'],
        '肿瘤学,神经系统肿瘤': ['662', '966', '983'],
        '肿瘤学,肿瘤研究体系新技术': ['662', '966', '984'],
        '肿瘤学,头颈部及颌面肿瘤': ['662', '966', '985'],
        '肿瘤学,肿瘤康复': ['662', '966', '986'],
        '肿瘤学,肿瘤生物治疗': ['662', '966', '987'],
        '肿瘤学,内分泌系统肿瘤': ['662', '966', '988'],
        '肿瘤学,肿瘤化学药物治疗': ['662', '966', '989'],
        '肿瘤学,肿瘤诊断': ['662', '966', '990'],
        '肿瘤学,男性生殖系统肿瘤': ['662', '966', '991'],
        '肿瘤学,皮肤、体表及其他部位肿瘤': ['662', '966', '992'],
        '肿瘤学,肿瘤预防': ['662', '966', '993'],
        '预防医学': ['662', '994', '0'],
        '医学免疫学': ['662', '1008', '0'],
        '药理学': ['662', '1026', '0'],
        '老年医学': ['662', '1085', '0'],
        '检验医学': ['662', '1087', '0'],
        '康复医学': ['662', '1096', '0'],
        '药物学': ['662', '1103', '0'],
        '放射医学': ['662', '1135', '0'],
    }
    main()



