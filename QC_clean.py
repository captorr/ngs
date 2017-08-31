#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python script.py [1].fq [2].fq [3]*outputdir

Zhang Chengsheng, @2017.06
"""


import os
import sys
import time


def name(input1):
    """file name normalize"""
    if input1.endswith('.fasta') or input1.endswith('.fastq') or input1.endswith('.fq'):
        if input1.endswith('.fasta'):
            filename_temp = input1.replace('.fasta','.clean.fasta')
        if input1.endswith('.fastq'):
            filename_temp = input1.replace('.fastq','.clean.fastq')
        if input1.endswith('.fq'):
            filename_temp = input1.replace('.fq','.clean.fq')
    else:
        print 'files name error'
        exit(1)
    return filename_temp

def percent_float(input3):
    input3 = float(input3)
    if input3 >= 1.0:
        input3 = '100%'
    elif input3 <= 0.0:
        input3 = '0'
    else:
        input3 = '%.2f%%' % (input3 * 100)
        input3 = str(input3)
    return input3

def countN(file1,file2,*target_dir):
    if target_dir != ():
        try:
            if os.path.exists(str(target_dir[0])):
                pass
            else:
                os.makedirs(str(target_dir[0]))
        except:
            print 'outputdir error'
            exit(1)

    file1 = file1
    file1_name = file1.split('/')[-1].split('.')[0]
    file2 = file2
    file2_name = file2.split('/')[-1].split('.')[0]
    #file_dir = '/'.join(file1.split('/')[:-1])
    file_name = '_'.join(file1.split('_')[:-1])
    log_n = file1 + '.QC.log'
    file_x_n = name(file1)
    file_y_n = name(file2)
    count = 0
    missed, missed_bases_x, missed_bases_y = 0, 0, 0
    good = 0
    low = 0
    total = 0
    numAx, numGx, numCx, numTx, numNx, numLengthx = 0, 0, 0, 0, 0, 0
    numAy, numGy, numCy, numTy, numNy, numLengthy = 0, 0, 0, 0, 0, 0
    line1x, line1y = '', ''
    line2x, line2y = '', ''
    line3x, line3y = '', ''
    line4x, line4y = '', ''
    q1 = True
    q20_x = 0
    q20_y = 0
    q30_x = 0
    q30_y = 0
    q_x = 0
    q_y = 0

    file_x = open(file_x_n, 'w')
    file_y = open(file_y_n, 'w')

    with open(file1, 'r') as f1:
        with open(file2, 'r') as f2:
            while 1:
                count += 1
                x = f1.readline()
                y = f2.readline()
                if x == '' or y == '':
                    break
                if count % 4 == 1:
                    line1x, line1y = x, y
                if count % 4 == 2:
                    line2x, line2y = x, y
                    total += 1 #total reads
                    if float(x.count('N')) / float(len(x[:-1])) > 0.1 or float(y.count('N')) / float(len(y[:-1])) > 0.1:
                        q1 = False #switch
                        missed += 1  # N>10% reads count
                        missed_bases_x += len(x[:-1])
                        missed_bases_y += len(y[:-1])
                    else:
                        pass

                if count % 4 == 3:
                    line3x, line3y = x, y
                if count % 4 == 0:
                    line4x, line4y = x, y
                    if len(line4x) != len(line2x) or len(line4y) != len(line2y):
                        q1 = False
                        low += 1

                    if q1 == True:

                        q20x = 0
                        q20y = 0
                        q_x_t = 0
                        q_y_t = 0
                        q20_xt = 0
                        q30_xt = 0
                        q20_yt = 0
                        q30_yt = 0

                        for i in line4x[:-1]:
                            q_x_t += (10 ** (-((int(ord(i))-33) / 10)))/10  # error rate function
                            if int(ord(i)) < 53:
                                q20x += 1
                                q20_xt += 1
                                q30_xt += 1
                            elif int(ord(i)) < 63:
                                q30_xt += 1
                            else:
                                pass

                        for i in line4y[:-1]:
                            q_y_t += (10 ** (-((int(ord(i))-33) / 10))) /10  #error rate function
                            if int(ord(i)) < 53:
                                q20y += 1
                                q20_yt += 1
                                q30_yt += 1
                            elif int(ord(i)) < 63:
                                q30_yt += 1
                            else:
                                pass


                        #q20x = [m for m in x[:-1] if (int(ord(m)) - 33) < 20]
                        #q20y = [n for n in y[:-1] if (int(ord(n)) - 33) < 20]

                        #q20_x += len(q20x)
                        #q20_y += len(q20y)
                        #q30x = [m for m in x[:-1] if (int(ord(m)) - 33) < 30]
                        #q30y = [n for n in y[:-1] if (int(ord(n)) - 33) < 30]
                        #q30_x += len(q30x)
                        #q30_y += len(q30y)
                        #q_x += sum([(10 ** (-((int(ord(m))) / 10))) for m in x[:-1]])
                        #q_y += sum([(10 ** (-((int(ord(m))) / 10))) for m in y[:-1]])


                        if float(float(q20x)) / float(len(x[:-1])) > 0.5 or float(float(q20y)) / float(len(y[:-1])) > 0.5:
                            q1 = False
                            low += 1
                            missed_bases_x += len(line2x[:-1])
                            missed_bases_y += len(line2y[:-1])
                        else:
                            q20_x += q20_xt
                            q30_x += q30_xt
                            q20_y += q20_yt
                            q30_y += q30_yt
                            q_x += q_x_t
                            q_y += q_y_t
                    if q1 == True:
                        good += 1

                        numAx += line2x.count('A')
                        numGx += line2x.count('G')
                        numCx += line2x.count('C')
                        numTx += line2x.count('T')
                        numNx += line2x.count('N')
                        numLengthx += len(line2x[:-1])

                        numAy += line2y.count('A')
                        numGy += line2y.count('G')
                        numCy += line2y.count('C')
                        numTy += line2y.count('T')
                        numNy += line2y.count('N')
                        numLengthy += len(line2y[:-1])

                        file_x.write(line1x + line2x + line3x + line4x)
                        file_y.write(line1y + line2y + line3y + line4y)

                    line1x, line1y = '', ''
                    line2x, line2y = '', ''
                    line3x, line3y = '', ''
                    line4x, line4y = '', ''
                    q1 = True
    log = open(log_n, 'w')
    try:
        log.write('Sample name:\t')
        log.write(file_name)
        log.write('\nRaw reads:\t')
        log.write(str(total * 2) + '\t100%')
        log.write('\nN>10% reads:\t')
        num1 = percent_float((float(missed) / float(total)))
        log.write(str(missed * 2) + '\t' + num1)
        log.write('\nLow quality reads:\t')
        num2 = percent_float((float(low) / float(total)))
        log.write(str(low * 2) + '\t' + num2)
        log.write('\nClean reads:\t')
        num3 = percent_float((float(good) / float(total)))
        log.write(str(good * 2) + '\t' + num3)

        log.write('\nRaw bases:\t')
        log.write(str(total * 2 * 150) + '\t')
        log.write(str('%.2f' % (total * 2 * 150.0 / 1000.0 / 1000.0)))
        log.write('\nClean bases:\t')
        log.write(str(good * 2 * 150) + '\t')
        log.write(str('%.2f' % (good * 2 * 150.0 / 1000.0 / 1000.0)))
        log.write('\nReal Raw bases:\t')
        log.write(str(str(missed_bases_x + numLengthx + missed_bases_y + numLengthy)) + '\t')
        log.write(str('%.2f' % ((missed_bases_x + numLengthx + missed_bases_y + numLengthy) / 1000.0 / 1000.0)))
        log.write('\nReal Clean bases:\t')
        log.write(str(numLengthx + numLengthy) + '\t')
        log.write(str('%.2f' % ((numLengthx + numLengthy)/(1000.0*1000.0))))
        log.write('\nError rate:\t')
        num3 = float((q_x + q_y))/float((numLengthx + numLengthy))
        num3 = '%.6f%%' % (num3 * 100)
        log.write(str(num3) + '\t')
        log.write('\nQ20:\t')
        num2 = percent_float(((numLengthy + numLengthx - q20_x - q20_y) / float((numLengthx + numLengthy))))
        log.write(str(numLengthy + numLengthx - q20_x - q20_y) + '\t' + num2)
        log.write('\nQ30:\t')
        num2 = percent_float(((numLengthy + numLengthx - q30_x - q30_y) / float((numLengthx + numLengthy))))
        log.write(str(numLengthy + numLengthx - q30_x - q30_y) + '\t' + num2)
        log.write('\nGC content\t')
        num9 = percent_float(float((numGx + numCx + numGy + numCy) / float(numLengthx + numLengthy)))
        log.write(num9 + '\t')


        log.write('\n\nfile1 name:\t')
        log.write(file1_name)
        log.write('\nRaw bases(MB):\t')
        log.write(str('%.2f' % ((missed_bases_x + numLengthx)/(1000.0*1000.0))) + '\t')
        log.write('\nClean bases(MB):\t')
        log.write(str('%.2f' % (numLengthx/(1000.0*1000.0))) + '\t100%')
        log.write('\nError rate:\t')
        num3 = float(q_x)/float(numLengthx)
        num3 = '%.6f%%' % (num3 * 100)
        log.write(str(num3) + '\t')
        log.write('\nQ20:\t')
        num2 = percent_float(((numLengthx - q20_x) / float(numLengthx)))
        log.write(str(numLengthx - q20_x) + '\t' + num2)
        log.write('\nQ30:\t')
        num2 = percent_float(((numLengthx - q30_x) / float(numLengthx)))
        log.write(str(numLengthx - q30_x) + '\t' + num2)
        log.write('\nCount of bases A:\t')
        num4 = percent_float(float((numAx) / float(numLengthx)))
        log.write(str(numAx) + '\t' + num4)
        log.write('\nCount of bases G:\t')
        num5 = percent_float(float((numGx) / float(numLengthx)))
        log.write(str(numGx) + '\t' + num5)
        log.write('\nCount of bases C:\t')
        num6 = percent_float(float((numCx) / float(numLengthx)))
        log.write(str(numCx) + '\t' + num6)
        log.write('\nCount of bases T:\t')
        num7 = percent_float(float((numTx) / float(numLengthx)))
        log.write(str(numTx) + '\t' + num7)
        log.write('\nCount of bases N:\t')
        num8 = percent_float(float((numNx) / float(numLengthx)))
        log.write(str(numNx) + '\t' + num8)
        log.write('\nGC content:\t')
        num9 = percent_float(float((numGx + numCx) / float(numLengthx)))
        log.write(num9 + '\t')


        log.write('\n\nfile2 name:\t')
        log.write(file2_name)
        log.write('\nRaw bases(MB):\t')
        log.write(str('%.2f' % ((missed_bases_y + numLengthy) / (1000.0 * 1000.0))) + '\t')
        log.write('\nClean bases(MB):\t')
        log.write(str('%.2f' % (numLengthy / (1000.0 * 1000.0))) + '\t100%')
        log.write('\nError rate:\t')
        num3 = float(q_y) / float(numLengthy)
        num3 = '%.6f%%' % (num3 * 100)
        log.write(str(num3) + '\t')
        log.write('\nQ20:\t')
        num2 = percent_float(((numLengthy - q20_y) / float(numLengthy)))
        log.write(str(numLengthy - q20_y) + '\t' + num2)
        log.write('\nQ30:\t')
        num2 = percent_float(((numLengthy - q30_y) / float(numLengthy)))
        log.write(str(numLengthy - q30_y) + '\t' + num2)
        log.write('\nCount of bases A:\t')
        num4 = percent_float((float(numAy) / float(numLengthy)))
        log.write(str(numAy) + '\t' + num4)
        log.write('\nCount of bases G:\t')
        num5 = percent_float((float(numGy) / float(numLengthy)))
        log.write(str(numGy) + '\t' + num5)
        log.write('\nCount of bases C:\t')
        num6 = percent_float((float(numCy) / float(numLengthy)))
        log.write(str(numCy) + '\t' + num6)
        log.write('\nCount of bases T:\t')
        num7 = percent_float((float(numTy) / float(numLengthy)))
        log.write(str(numTy) + '\t' + num7)
        log.write('\nCount of bases N:\t')
        num8 = percent_float((float(numNy) / float(numLengthy)))
        log.write(str(numNy) + '\t' + num8)
        log.write('\nGC content:\t')
        num9 = percent_float(float((numGy + numCy) / float(numLengthy)))
        log.write(num9 + '\t')

    except Exception as e:
        print 'error'
        print e

    log.close()
    file_x.close()
    file_y.close()
    if len(target_dir) == 0:
        print log_n
    elif len(target_dir) == 1:
        target_dir = str(target_dir[0])
        if os.path.exists(target_dir):
            pass
        else:
            os.makedirs(target_dir)
        os.system('mv ' + file_x_n + ' ' + target_dir)
        os.system('mv ' + file_y_n + ' ' + target_dir)
        print target_dir
    elif len(target_dir) == 2:
        target_dir1 = str(target_dir[0])
        if not os.path.exists(target_dir1):
            os.makedirs(target_dir1)
        os.system('mv ' + file_x_n + ' ' + target_dir1)
        os.system('mv ' + file_y_n + ' ' + target_dir1)
        target_dir2 = str(target_dir[1])
        if not os.path.exists(target_dir2):
            os.makedirs(target_dir2)
        os.system('mv ' + log_n + ' ' + target_dir2)
        print target_dir1
        print target_dir2

try:
    if len(sys.argv) == 4:
        countN(sys.argv[1],sys.argv[2],sys.argv[3])
    elif len(sys.argv) == 5:
        countN(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    else:
        countN(sys.argv[1],sys.argv[2])
except:
    print 'parameter error'


