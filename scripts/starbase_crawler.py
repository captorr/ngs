"""
Author: Zhang Chengsheng, @2018.02.28
Description: A python3 script for starBase v2.0 db ceRNA network target miRNA search download and parse.
Website: http://starbase.sysu.edu.cn/index.php
Usage: python script.py [1]input_file
=======================================================
Output: 
[1] Input.out: All URL of input gene.
[2] Input.out.gene: Input gene target miRNA. #dumplicated
[3] Input.out.ceRNA: ceRNA of input gene target miRNA. #dumplicated
[4] Input.out.common: Common miRNA of input gene and it's ceRNA.
[5] Input.out.log: Script's log.
=======================================================
exapmle for input_file:
AKT1
AKT2
BCL9
BRD4
CCDC6
...
gene_symbol
...
=======================================================
"""

import requests
import re
import os,sys,time

def starbase_crawler(gene_name):
    headers = {
        b'User-Agent': b'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        b'Content-Type': b'multipart/form-data; boundary=----WebKitFormBoundaryG9oArr8stF6MbBiI',
        b'Cookie': b'_ga=GA1.3.1059924842.1519442549; Hm_lvt_eaa982b8ba4413b61f1766e6acfcb50b=1519442549; _gid=GA1.3.475277538.1519714977; _gat=1; Hm_lpvt_eaa982b8ba4413b61f1766e6acfcb50b=1519780905',
        b'Referer': b'http://starbase.sysu.edu.cn/mrnaCeRNA.php'}
    url_2 = 'http://starbase.sysu.edu.cn/browseMrnaCeRNA.php'  # http://starbase.sysu.edu.cn/browseMrnaCeRNA.php

    Files1 = {'clade': (None, 'mammal'),
              'genome': (None, 'Human'),
              'database': (None, 'hg19'),
              'sigCancerNum': (None, '-1'),
              'commonMirNum': (None, '5'),
              'pValue': (None, '0.05'),
              'FDR': (None, '1.0'),
              'geneSymbol': (None, str(gene_name)),
              'geneTable': (None, ''),
              '': (None, 'ensemblAllGene')}

    Data1 = 'shows=Shows%3A&displayNum=171&page=1&genome=Human&database=hg19&table=ceRNANetworksAll&term=&sigCancerNum=-1&commonMirNum=5&geneSymbol=AKT2&mirReadNum=0&FDR=1.0&pValue=0.05&nextPage=&backPage=&order=DESC'
    rq = requests.post(url_2, files=Files1)
    #print(rq.content)
    time.sleep(0.5)
    res_list = []
    reg = 'ceRNANetworkInfo.php(.*?)=ceRNANetworksAll'
    r1 = re.compile(reg)
    for i in r1.findall(str(rq.content)):
        res = 'http://starbase.sysu.edu.cn/ceRNANetworkInfo.php' + i + '=ceRNANetworksAll'
        res_list.append(res)
        #print(res)
    return res_list

def main_work(input,output):
    file1 = open(input,'r')
    gene_list = []
    gene_web_result = []
    for gene in file1.readlines():
        gene_list.append(gene.strip())
    file1.close()
    miss, hit = 0, 0
    for gene in gene_list:
        if gene:
            print(gene)
            res = starbase_crawler(gene)
            if res != []:
                #print(res)
                hit += 1
                for i in res:
                    if i not in gene_web_result:
                        gene_web_result.append(i)
            else:
                print('empty')
                miss += 1
    file2 = open(output,'w')
    for i in gene_web_result:
        file2.write(i)
        file2.write('\n')
    file2.close()
    print('%dhit, %dmiss' % (hit, miss))

def miRNAs_parse(input):
    genelist = []
    output = input
    file1 = open(input,'r')
    for i in file1.readlines():
        genelist.append(i.strip())
    file1.close()
    file_common = open(output + '.common','w')
    file_gene = open(output + '.gene','w')
    file_mi = open(output + '.ceRNA','w')
    file_log = open(output + '.log','w')

    regu1 = '<tr><td>common miRNAs(.*?)</td></tr>'
    r1 = re.compile(regu1)
    regu2 = '<B>(.*?)</B>'
    r2 = re.compile(regu2)
    total = len(genelist)
    count = 0.0
    for site in genelist:
        count += 1
        percentage = count/total
        url = site
        gene = re.compile('name=(.*?)&').findall(url)
        miRNA = re.compile('cernaName=(.*?)&').findall(url)
        if gene != [] and miRNA != []:
            gene = gene[0]
            miRNA = miRNA[0]
            rq = requests.post(url)
            time.sleep(0.2)
            #common
            res = r1.findall(str(rq.content))
            if res != []:
                miRNAs = r2.findall(res[0])
                #print(miRNAs)
                common = len(miRNAs)
                file_common.write(gene + '+' + miRNA + '\t' + ' '.join(miRNAs) + '\n')
            else:
                common = 0
                file_common.write(gene + '+' + miRNA + '\tNone\n')
            #gene
            regu_gene = '<tr class="dataRow odd"><td><b>' + str(gene) + '</b>(.*?)</td></tr>'
            r3 = re.compile(regu_gene)
            res_gene = r3.findall(str(rq.content))
            if res_gene != []:
                miRNAS_gene = r2.findall(res_gene[0])
                #print(miRNAS_gene)
                gene_len = len(miRNAS_gene)
                file_gene.write(gene + '\t' + ' '.join(miRNAS_gene) + '\n')
            else:
                gene_len = 0
                file_gene.write(gene + '\t\n')
            #miRNA
            regu_mi = '<tr><td><b>' + str(miRNA) + '</b>(.*?)</td></tr>'
            r4 = re.compile(regu_mi)
            res_mi = r4.findall(str(rq.content))
            if res_mi != []:
                miRNAs_mi = r2.findall(res_mi[0])
                #print(miRNAs_mi)
                mi_len = len(miRNAs_mi)
                file_mi.write(miRNA + '\t' + ' '.join(miRNAs_mi) + '\n')
            else:
                mi_len = 0
                file_mi.write(miRNA + '\t\n')

            log = '%s+%s:  %s:%d, %s:%d, common:%d' %(gene, miRNA, gene, gene_len, miRNA, mi_len, common) + ' ' + time.asctime() + ' ' + '%.2f' % (100*percentage) + '%'
            file_log.write(log + '\n')
            print(log)
        else:
            print('input:' + url + ' error!')
            file_log.write('input:' + url + ' error!')


#file1 = 'D:\\zcs-genex\\180227\\644.txt'
#file2 = 'D:\\zcs-genex\\180227\\644.txt.out'

file1 = sys.argv[1]
file2 = file1 + '.out'
main_work(file1,file2)
miRNAs_parse(file2)




