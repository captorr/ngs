"""
Author: Zhang Chengsheng, @2018.01.29

Input: gene name list (symbol or any id format)
Output: 'origin /t real/n'

input example:
HLA-A
TAS2R43
PRSS3
RBMXL1
DDX11
ZNF469
SLC35G5
GOLGA6L6
PRB2
"""


import os,sys,time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from urllib.request import quote
import re
from bs4 import BeautifulSoup


def ncbi_Crawler(gene_name):  #TODO: space split error
    url_1 = 'https://www.ncbi.nlm.nih.gov/gene/?term=' + gene_name  #?term='(' + gene_name + ')+AND+"Homo+sapiens"%5Bporgn%3A__txid9606%5D'
    try:
        headers = {b'Host': b'www.ncbi.nlm.nih.gov',
                   b'Cache - Control': b'max - age = 0',
                   b'Upgrade-Insecure-Requests': b'1',
                   b'User-Agent': b'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
                   b'Accept-Encoding': b'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   b'Accept-Language': b'zh-CN,zh;q=0.9',
                   }
        html = urlopen(url_1, headers)
        time.sleep(0.5)
    except Exception as e:
        soup = 'none'
        print(e)
    else:
        soup = BeautifulSoup(html, 'lxml')
    finally:
        return str(soup)


def new_parse(strings, orig_name):
    regular = '<div><a href=.+?<td class="gene-name-id">'
    regular_c = re.compile(regular)
    b = re.findall(regular_c, strings)
    for i in b:
        if 'Homo sapiens' in i and orig_name in i:
            temp = i.split('</')[0].split('>')[-1]
            print(temp)
            break
    else:
        temp = ''
    return orig_name,temp


def main(input):
    """"""
    output_file = input + '.out'
    output_file_o = open(output_file,'w')
    output_file_o.write('origin\treal\n')
    input_o = open(input,'r')
    gene_list = input_o.readlines()
    input_o.close()
    count = 0
    for i in gene_list:
        count += 1
        print(count,' genes start at: ',time.asctime())
        re_gene = ncbi_Crawler(str(i).strip('\n'))
        if re_gene != 'none':
            origin, new = new_parse(re_gene,str(i).strip('\n'))
            output_file_o.write('{}\t{}\n'.format(origin,new))

        else:
            output_file_o.write('{}\tnetwork error\n'.format(str(i).strip('\n')))
    output_file_o.close()


if __name__ == '__main__':
    probe_test = sys.argv[1]
    main(probe_test)
