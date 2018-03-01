"""
Author: Zhang Chengsheng, @2018.03.01
Description: search and filter miRNA in form of 'x/x-3p or x/x-5p'
Usage: python2&3 script.py [1]input file
Input: starbase_crawler.py output file .out.gene undumplicated
Output: filter result
==========================================
input example:
gene_symbol '\t' miRNA1 miRNA2 miRNA3 ....
gene_symbo2 '\t' miRNA1 miRNA2 miRNA3 ....
gene_symbo2 '\t' miRNA1 miRNA2 miRNA3 ....
....
"""

import os,sys

#file1 = 'D:\\zcs-genex\\180301\\644.gene.filter.txt'
file1 = sys.argv[1]
file1_o = open(file1,'r')
file2_o = open(file1 + '.out1','w')

for i in file1_o.readlines():
    line = i.strip()
    gene = line.split('\t')[0]
    miRNA = line.split('\t')[-1]
    miRNAs = miRNA.split(' ')
    mi_list = []
    for mi in miRNAs:
        if '-3p' in mi or '-5p' in mi:
            single = mi.split('/')
            for i in single:
                if '-3p' in i:
                    p3 = i.strip('-3p')
                    if len([hit for hit in single if p3 in hit]) > 1:
                        mi_list.append(mi)
                        break
                if '-5p' in i:
                    p5 = i.strip('-5p')
                    if len([hit for hit in single if p5 in hit]) > 1:
                        mi_list.append(mi)
                        break

    file2_o.write(gene)
    file2_o.write('\t')
    if mi_list != []:
        file2_o.write(' '.join(mi_list))
    file2_o.write('\n')

file1_o.close()
file2_o.close()