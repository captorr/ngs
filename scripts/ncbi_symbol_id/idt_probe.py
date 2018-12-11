"""
Author: Zhang Chengsheng, @2018.01.29

Input: gene name list (symbol or any id format)
Output: 'gene name /t search name /t Also known as id list /n' 

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


def ncbi_Crawler(gene_name):
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

#print(str(soup))


def re_match(strings):
    """balabala"""
    regular = '\<span class="highlight" style="background-color:"\>.+?\<td class="col-omim"\>'
    regular_c = re.compile(regular)
    b = re.findall(regular_c, strings)
    res_list = []
    for i in b:
        if 'Homo sapiens' in i:
            res_list.append(i)
    if not res_list:
        return 'no result'

    re_sub = '<.*?>'
    re_sub_c = re.compile(re_sub)

    res_line = []
    if res_list:
        for i in res_list:
            res_line1 = []
            for j in i.split('</td><td>'):
                # print(j)
                j = j.replace('<span class="gene-id">', '\t')
                test = re.sub(re_sub_c, '', j)
                res_line1.append(test)
                # print(test)
                # print(j)
            res_line.append(res_line1)

    return res_line
    # ['WASHC2A\tID: 387680', 'WASH complex subunit 2A [Homo sapiens (human)]', 'Chromosome 10, NC_000010.11 (50067888..50133509)', 'FAM21A, FAM21B, bA56A21.1, bA98I6.1']

def text_writing(gene_name,res_of_re_match):
    """input: result of re_match()"""
    if len(res_of_re_match) == 0:
        res_line = str(gene_name) + '\n'
        return res_line
    elif len(res_of_re_match) == 1:
        res = res_of_re_match[0]
        gene_name1 = res[0].split('\t')[0]
        res_line = str(gene_name).strip() + '\t' + str(gene_name1) + '\t' + str(res[-1]) + '\n'
        return res_line
    elif len(res_of_re_match) > 1:
        res_line = ''
        for i in res_of_re_match:
            res = i
            gene_name1 = res[0].split('\t')[0]
            res_line += '[multi]' + str(gene_name) + '\t' + str(gene_name1) + '\t' + str(res[-1]) + '\n'
        return res_line
    else:
        return gene_name + '\ttext_writing error\n'

def main(input):
    """"""
    output_file = input + '.out'
    output_file_o = open(output_file,'w')
    input_o = open(input,'r')
    gene_list = input_o.readlines()
    input_o.close()
    count = 0
    for i in gene_list:
        count += 1
        print(count,' genes start at: ',time.asctime())
        re_gene = ncbi_Crawler(str(i).strip('\n'))
        if re_gene != 'none':
            res = re_match(str(re_gene))
            if res != 'no result':
                res_line = text_writing(i,res)
                #print(res_line)
                output_file_o.write(res_line)
            else:
                output_file_o.write(i)
                output_file_o.write('\t')
                output_file_o.write('no result')
                output_file_o.write('\n')
        else:
            output_file_o.write(i)
            output_file_o.write('\t')
            output_file_o.write('network error')
            output_file_o.write('\n')

    output_file_o.close()

#probe_test = "D:\\zcs-genex\\180129\\IDT_probe\\probe_text.txt"
probe_test = sys.argv[1]
main(probe_test)



