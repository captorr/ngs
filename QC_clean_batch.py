#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python script.py [1]dir_path

need QC_clean.py

Zhang Chengsheng, @2017.06
"""


import os
import sys
import getopt

def makedir(dir_path):
    #if not os.path.exists(dir_path):
    if os.path.exists(dir_path):
        pass
    else:
        os.makedirs(dir_path)

def QC_clean(dir_path1,outputdir1,outputdir2):
    if not os.path.exists(dir_path1):
        help1()
        exit(1)

    global sh, qsub, run1

    file_name = [dir_path1 + '/' + i for i in os.listdir(dir_path1) if i.endswith('.fq') or i.endswith('.fastq')]
    PBS_header = '#PBS -l nodes=1:ppn=1\n#PBS -q long\n'
    couple = []
    if len(file_name) % 2 == 0:
        file_name = sorted(file_name)
        for i in range(len(file_name) / 2):
            couple.append([file_name[2 * i], file_name[2 * i + 1]])
    else:
        print 'error: have a single one .fq/.fastq file.'
        exit()

    for i in couple:
        print i

    QC_clean_command_path = '/'.join(dir_path1.split('/')[:-1]) + '/QCclean_command'
    #QC_clean_command_path = '\\'.join(dir_path1.split('\\')[:-1]) + '\\QCclean_command'
    if os.path.exists(QC_clean_command_path):
        pass
    else:
        os.makedirs(QC_clean_command_path)

    for i in couple:
        fq_name1 = '_'.join(i[0].split('/')[-1].split('.')[0].split('_')[:-1])
        fq_name2 = '_'.join(i[1].split('/')[-1].split('.')[0].split('_')[:-1])
        if fq_name1 == fq_name2:
            #HISAT2_outputdir = HISAT2_resault_dir + '/' + HISAT2_name1
            #makedir(HISAT2_outputdir)
            QCclean_command_file = open(QC_clean_command_path + '/' + fq_name1 + '.QC.sh', 'w')

            QCclean_command_file.write(PBS_header)
            QCclean_command_file.write('cd ' + dir_path1 + '\n')
            if outputdir1 == '':
                if outputdir2 == '':
                    QCclean_command_file.write('pypy QC_clean.py ' + i[0] + ' ' + i[1] + ' \n')
                else:
                    QCclean_command_file.write('pypy QC_clean.py ' + i[0] + ' ' + i[1] + str(dir_path1) + ' ' + outputdir2 +' \n')
            else:
                if outputdir2 == '':
                    QCclean_command_file.write('pypy QC_clean.py ' + i[0] + ' ' + i[1] + ' ' + outputdir1 +' \n')
                else:
                    QCclean_command_file.write('pypy QC_clean.py ' + i[0] + ' ' + i[1] + ' ' + outputdir1 + ' ' + outputdir2 +' \n')
            QCclean_command_file.close()
        else:
            print 'error: have miss matching'

    if sh == True:
        start_file = open(QC_clean_command_path + '/sh.start', 'w')
        start_file.write('cd ' + QC_clean_command_path)
        start_file.write('\nfor file in ' + QC_clean_command_path + '/*.sh\n')
        start_file.write('do\n')
        start_file.write('sh $file $\n')
        start_file.write('done')
    else:
        start_file = open(QC_clean_command_path + '/qsub.start', 'w')
        start_file.write('cd ' + QC_clean_command_path)
        start_file.write('\nfor file in ' + QC_clean_command_path + '/*.sh\n')
        start_file.write('do\n')
        start_file.write('qsub $file \n')
        start_file.write('done')
    if qsub == True:
        start_file = open(QC_clean_command_path + '/qsub.start', 'w')
        start_file.write('cd ' + QC_clean_command_path)
        start_file.write('\nfor file in ' + QC_clean_command_path + '/*.sh\n')
        start_file.write('do\n')
        start_file.write('qsub $file \n')
        start_file.write('done')

    print QC_clean_command_path

    if run1 == True:
        if sh == True:
            os.system('sh ' + QC_clean_command_path + '/sh.start')
            print 'shell script running'
        else:
            os.system('sh ' + QC_clean_command_path + '/qsub.start')
            print 'qsub running'




def help1():
    print 'python script.py [1]file_dir'
    print '-h --help:  help infomations'
    print '-o dirpath --output dirpath:  output_dir  default:none'
    print '-q --qsub:  make qsub.start  default:qsub'
    print '-s --sh:  make sh.start  default:qsub'
    print '-r --run:  run automatically  default:manually'
    print '-l dirpath --log dirpath:  log outputdir default: raw_data_dir'

outputdir = ''
outputdir2 = ''
qsub = True
sh = False
run1 = False
try:
    opt, value = getopt.getopt(sys.argv[2:], 'ho:l:qsr', ['help', 'output=', 'log=', 'sh', 'qsub', 'run'])
    for name, value in opt:
        if name in ('-o', '--output'):
            outputdir = value
        if name in ('-h', '--help'):
            help1()
            exit(1)
        if name in ('-q', '--qsub'):
            qsub = True
        if name in ('-s', '--sh'):
            sh = True
        if name in ('-r', '--run'):
            run1 = True
        if name in ('-l', '--log'):
            outputdir2 = value
except :
    help1()
    exit(1)
QC_clean(sys.argv[1], outputdir, outputdir2)





