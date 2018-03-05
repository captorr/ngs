"""
Author: Zhang Chengsheng, @2018.03.05
Usage: python script.py [1]file_in

example for file_in:
#file_in = 'D:\\zcs-genex\\180305\\result.txt'
need R script: 'D:\\zcs-genex\\SCRIPTS\\david_go_kegg_180305.R'
"""

import os,sys



def david_trans_to_png(file_in):
    file_in_o = open(file_in, 'r')
    context = file_in_o.readlines()
    file_in_o.close()
    file_out_go = file_in + '.go_enrichment'
    file_out_kegg = file_in + '.kegg_enrichment'
    file_out_go_o = open(file_out_go, 'w')
    file_out_kegg_o = open(file_out_kegg, 'w')
    # 'GOTERM_BP_DIRECT',GOTERM_CC_DIRECT','GOTERM_MF_DIRECT','KEGG_PATHWAY'
    # 'Biological_Process','Cellular_Component','Molecular_Function','KEGG' ,'KEGG_PATHWAY':'KEGG_PATHWAY'
    trans_dict = {'GOTERM_BP_DIRECT': 'Biological_Process', 'GOTERM_CC_DIRECT': 'Cellular_Component',
                  'GOTERM_MF_DIRECT': 'Molecular_Function'}
    for i in range(len(context)):
        if i == 0:
            title = context[i].split('\t')
            title.insert(2, 'Term_name')
            text = '\t'.join(title)
            file_out_go_o.write(text)
            file_out_kegg_o.write(text)
        else:
            line = context[i].split('\t')
            if line[0] in trans_dict:
                # GO
                line[0] = trans_dict[line[0]]
                if '~' in line[1]:
                    term = line[1].split('~')
                    line[1] = term[0]
                    line.insert(2, term[1])
                else:
                    line.insert(2, '')
                    print('line:', i, 'error_1 !')
                text = '\t'.join(line)  # GO
                file_out_go_o.write(text)
            else:
                # KEGG
                if line[0] == 'KEGG_PATHWAY':
                    if ':' in line[1]:
                        term = line[1].split(':')
                        line[1] = term[0]
                        line.insert(2, term[1])
                    else:
                        line.insert(2, '')
                        print('line:', i, 'error_3 !')
                    text = '\t'.join(line)
                    file_out_kegg_o.write(text)
                else:
                    print('line:', i, 'error_2 !')

    file_out_go_o.close()
    file_out_kegg_o.close()
    return file_out_go, file_out_kegg

def david_png(go,kegg):
    Rscript = 'D:\\zcs-genex\\SCRIPTS\\david_go_kegg_180305.R'
    cmd = 'rscript ' + Rscript + ' ' + go + ' ' + kegg
    os.system(cmd)

file_in = sys.argv[1]
go, kegg = david_trans_to_png(file_in)
david_png(go,kegg)
