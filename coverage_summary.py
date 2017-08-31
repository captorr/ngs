#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" 
python script.py [1]bed_path [2]sam_path [3]outputdir [4]log_dir [5]panel_name 
stat coverage on bed_file
###  need bamtools  ###

Zhang Chengsheng, @2017.07
"""


import os
import sys

class coverage_summary:
    def __init__(self,path1,path2,outputdir,outputdir_log,panel):
        self.bed_path = path1 # bed_panel
        self.bed_name = self.bed_path.split('/')[-1]
        self.sam_path = path2 # sam file
        self.sam_name = self.sam_path.split('/')[-1]
        self.dir_path = '/'.join(self.sam_path.split('/')[0:-1])
        self.dir_path_1 = ''
        self.idxstats_file = ''
        self.all_bed = ''
        self.bed200 = ''
        self.bed300 = ''
        self.bedcov_target = ''
        self.bedcov_flanking = ''
        self.bedcov_flanking300 = ''
        self.bedcov_total = ''
        self.flagstat = ''
        self.summary_file = ''
        self.outputdir = outputdir
        self.outputdir_log = outputdir_log
        self.panel = panel

    def samtools_idxstats(self):
        name = self.bed_name + '.idxstats'
        self.dir_path_1 = self.dir_path + '/' + self.sam_name.replace('.sam','') + '_' + self.panel +  '_summary'
        self.idxstats_file = self.dir_path_1 + '/' + name
        if os.path.exists(self.dir_path_1):
            pass
        else:
            os.makedirs(self.dir_path_1)
        script1 = open(self.dir_path_1 + '/' + 'idx_step1.sh','w')
        script1.write('#PBS -l nodes=1:ppn=1'+'\n')
        script1.write('cd $PBS_O_WORKDIR'+'\n')
        script1.write('samtools idxstats ' + self.sam_path + ' > ' + self.idxstats_file)
        script1.close()
        print 'run samtools idxstats'
        os.system('sh ' + self.dir_path_1 + '/' + 'idx_step1.sh')

    def file_making(self):
        test_file = self.bed_path
        if os.path.isfile(test_file):
            self.bed200 = self.dir_path_1 + '/' + self.bed_name + '.+200.bed'
            self.bed300 = self.dir_path_1 + '/' + self.bed_name + '.+300.bed'
            file = open(self.bed200, 'w')
            file1 = open(self.bed300, 'w')
            temp1 = 0
            count4 = 0
            chr = ''
            with open(test_file, 'r') as bed_in:
                for i in bed_in.readlines():
                    count4 += 1
                    if count4 == 1:
                        temp = i.split('\t')
                        temp[1] = str(int(temp[1]) - 200)
                        temp[2] = str(int(temp[2]) + 200)
                        temp1 = temp[2]
                        chr = temp[0]
                        temp = '\t'.join(temp)
                        file.write(temp)
                    else:
                        temp = i.split('\t')
                        temp[1] = str(int(temp[1]) - 200)
                        temp[2] = str(int(temp[2]) + 200)
                        if temp[0] == chr and int(temp[1]) < int(temp1):
                            temp[1] = str(int(temp1) + 1)
                        if int(temp[2]) <= int(temp[1]):
                            temp[2] = str(int(temp[1]) + 1)
                        chr = temp[0]
                        temp1 = temp[2]
                        temp = '\t'.join(temp)
                        file.write(temp)
            temp1 = 0
            count4 = 0
            chr = ''
            with open(test_file, 'r') as bed_in:
                for i in bed_in.readlines():
                    count4 += 1
                    if count4 == 1:
                        temp = i.split('\t')
                        temp[1] = str(int(temp[1]) - 300)
                        temp[2] = str(int(temp[2]) + 300)
                        temp1 = temp[2]
                        chr = temp[0]
                        temp = '\t'.join(temp)
                        file1.write(temp)
                    else:
                        temp = i.split('\t')
                        temp[1] = str(int(temp[1]) - 300)
                        temp[2] = str(int(temp[2]) + 300)
                        if temp[0] == chr and temp[1] < temp1:
                            temp[1] = str(int(temp1) + 1)
                        if int(temp[2]) <= int(temp[1]):
                            temp[2] = str(int(temp[1]) + 1)
                        chr = temp[0]
                        temp1 = temp[2]
                        temp = '\t'.join(temp)
                        file1.write(temp)
            file1.close()
            file.close()
        else:
            print 'input error'

        self.all_bed = self.idxstats_file + '.bed'
        if os.path.getsize(self.idxstats_file) > 0 :
            file = open(self.all_bed, 'w')
            with open(self.idxstats_file) as input1:
                x = input1.readlines()
                for i in range(len(x) - 1):
                    temp = x[i]
                    temp = temp.split('\t')
                    temp.insert(1, '1')
                    temp = '\t'.join(temp)
                    file.write(temp)
            file.close()
        else:
            print 'idxstats file size error, check samtools idxstats'

    def samtools_bedcov(self):
        self.bedcov_target = self.dir_path_1 + '/' + 'bedcov_target.log'
        self.bedcov_flanking = self.dir_path_1 + '/' + 'bedcov_flanking.log'
        self.bedcov_flanking300 = self.dir_path_1 + '/' + 'bedcov_flanking300.log'
        self.bedcov_total = self.dir_path_1 + '/' + 'bedcov_total.log'
        print 'run samtools bedcov target'
        os.system('samtools bedcov ' + self.bed_path + ' ' + self.sam_path + ' > ' + self.bedcov_target)
        print 'run samtools bedcov flanking'
        os.system('samtools bedcov ' + self.bed200 + ' ' + self.sam_path + ' > ' + self.bedcov_flanking)
        print 'run samtools bedcov flanking300'
        os.system('samtools bedcov ' + self.bed300 + ' ' + self.sam_path + ' > ' + self.bedcov_flanking300)
        print 'run samtools bedcov bam'
        os.system('samtools bedcov ' + self.all_bed + ' ' + self.sam_path + ' > ' + self.bedcov_total)

    def samtools_flagstat(self):
        self.flagstat = self.dir_path_1 + '/' + 'sam_flagstat.log'
        print 'run samtools flagstat'
        os.system('samtools flagstat ' + self.sam_path + ' > ' + self.flagstat)

    def percent_float(self,input3):
        input3 = float(input3)
        if input3 >= 1.0:
            input3 = '100%'
        elif input3 <= 0.0:
            input3 = '0.00%'
        else:
            input3 = '%.2f%%' % (input3 * 100)
            input3 = str(input3)
        return input3

    def coverage_count(self):
        global l1,l2
        global c1,c2,c3,len_t,len_f
        global x0, x1, x5, x10, x20, x50, x100, x200, x300, x500, x750, x1000
        global z0, z5, z10, z20, z50, z100, z200, z500, z300, z750, z1000
        global lx0, lx1, lx5, lx10, lx20, lx50, lx100, lx200, lx300, lx500, lx750, lx1000
        global ly0, ly5, ly10, ly20, ly50, ly100, ly200, ly300, ly500, ly750, ly1000
        a = self.bedcov_target
        b = self.bedcov_flanking
        c = self.bedcov_flanking300
        if os.path.isfile(a) and os.path.isfile(b):
            with open(a, 'r') as file1:
                l1 = len(file1.readlines())
            with open(b, 'r') as file2:
                l2= len(file2.readlines())
        else:
            print 'bam input error'
        if l1 == l2:
            file1 = open(a, 'r')
            file2 = open(b, 'r')
            file3 = open(c, 'r')
            c1, c2, c3 = 0, 0, 0
            len_t, len_f = 0, 0
            x0, x1, x5, x10, x20, x50, x100, x200, x300, x500, x750, x1000 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            lx0, lx1, lx5, lx10, lx20, lx50, lx100, lx200, lx300, lx500, lx750, lx1000 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            y0, y1, y5, y10, y20, y50, y100, y200, y300, y500, y750 ,y1000 = 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0
            ly0, ly1, ly5, ly10, ly20, ly50, ly100, ly200, ly300, ly500, ly750, ly1000 = 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0
            for i in range(l1):
                temp1 = file1.readline()
                temp2 = file2.readline()
                temp3 = file3.readline()
                n1 = int(temp1.split('\t')[-1])
                n2 = int(temp2.split('\t')[-1])
                n3 = int(temp3.split('\t')[-1])
                length_t = int(temp1.split('\t')[2]) - int(temp1.split('\t')[1])
                length_f = int(temp2.split('\t')[2]) - int(temp2.split('\t')[1])
                len_t += length_t  # target region length
                len_f += length_f  # t+f region length
                c1 += n1  # target bases
                c2 += n2  # t+f bases
                c3 += n3
                x1 += 1  # counts
                if n1 / length_t > 0:
                    x0 += 1
                    lx0 += length_t
                    if n1 / length_t >= 5:
                        x5 += 1
                        lx5 += length_t
                        if n1 / length_t >= 10:
                            x10 += 1
                            lx10 += length_t
                            if n1 / length_t >= 20:
                                x20 += 1
                                lx20 += length_t
                                if n1 / length_t >= 50:
                                    x50 += 1
                                    lx50 += length_t
                                    if n1 / length_t >= 100:
                                        x100 += 1
                                        lx100 += length_t
                                        if n1 / length_t >= 200:
                                            x200 += 1
                                            lx200 += length_t
                                            if n1 / length_t >= 300:
                                                x300 += 1
                                                lx300 += length_t
                                                if n1 / length_t >= 500:
                                                    x500 += 1
                                                    lx500 += length_t
                                                    if n1 / length_t >= 750:
                                                        x750 += 1
                                                        lx750 += length_t
                                                        if n1 / length_t >= 1000:
                                                            x1000 += 1
                                                            lx1000 += length_t
                y1 += 1
                if length_f - length_t != 0 :
                    if (n2 - n1) / (length_f - length_t) > 0:
                        y0 += 1
                        ly0 += (length_f - length_t)
                        if (n2 - n1) / (length_f - length_t) >= 5:
                            y5 += 1
                            ly5 += (length_f - length_t)
                            if (n2 - n1) / (length_f - length_t) >= 10:
                                y10 += 1
                                ly10 += (length_f - length_t)
                                if (n2 - n1) / (length_f - length_t) >= 20:
                                    y20 += 1
                                    ly20 += (length_f - length_t)
                                    if (n2 - n1) / (length_f - length_t) >= 50:
                                        y50 += 1
                                        ly50 += (length_f - length_t)
                                        if (n2 - n1) / (length_f - length_t) >= 100:
                                            y100 += 1
                                            ly100 += (length_f - length_t)
                                            if (n2 - n1) / (length_f - length_t) >= 200:
                                                y200 += 1
                                                ly200 += (length_f - length_t)
                                                if (n2 - n1) / (length_f - length_t) >= 300:
                                                    y300 += 1
                                                    ly300 += (length_f - length_t)
                                                    if (n2 - n1) / (length_f - length_t) >= 500:
                                                        y500 += 1
                                                        ly500 += (length_f - length_t)
                                                        if (n2 - n1) / (length_f - length_t) >= 750:
                                                            y750 += 1
                                                            ly750 += (length_f - length_t)
                                                            if (n2 - n1) / (length_f - length_t) >= 1000:
                                                                y1000 += 1
                                                                ly1000 += (length_f - length_t)
                else:
                    pass


            x1 = float(x1)
            len_flanking = len_f - len_t # flanking region length
            #z5, z10, z20, z50, z100, z200 = y5 - x5, y10 - x10, y20 - x20, y50 - x50, y100 - x100, y200 - x200
            x0 = x0 / x1
            x5 = x5 / x1
            x10 = x10 / x1
            x20 = x20 / x1
            x50 = x50 / x1
            x100 = x100 / x1
            x200 = x200 / x1
            x300 = x300 / x1
            x500 = x500 / x1
            x750 = x750 / x1
            x1000 = x1000 / x1
            z0, z5, z10, z20, z50, z100, z200, z300, z500, z750, z1000 = y0/x1, y5/x1, y10/x1, y20/x1, y50/x1, y100/x1, y200/x1, y300/x1, y500/x1, y750/x1, y1000/x1
            len_t1 = float(len_t)
            len_f1 = float((len_f-len_t))
            lx0, lx5, lx10, lx20, lx50, lx100, lx200, lx300, lx500, lx750, lx1000 = lx0/len_t1, lx5/len_t1, lx10/len_t1, lx20/len_t1, lx50/len_t1, lx100/len_t1, lx200/len_t1, lx300/len_t1, lx500/len_t1, lx750/len_t1, lx1000/len_t1
            ly0, ly5, ly10, ly20, ly50, ly100, ly200, ly300, ly500, ly750, ly1000 = ly0/len_f1, ly5/len_f1, ly10/len_f1, ly20/len_f1, ly50/len_f1, ly100/len_f1, ly200/len_f1, ly300/len_f1, ly500/len_f1, ly750/len_f1, ly1000/len_f1
            file1.close()
            file2.close()

        else:
            print 'length different error in two files'
        return c1,c2,c3,len_t,len_f,x0,x1, x5, x10, x20, x50, x100, x200,x300,x500,x750,x1000,z0,z5, z10, z20, z50, z100, z200,z300,z500,z750,z1000,lx0, lx5, lx10, lx20, lx50, lx100, lx200, lx300,lx500, lx750, lx1000,ly0, ly5, ly10, ly20, ly50, ly100, ly200, ly300,ly500, ly750, ly1000

    def summary(self):
        bases_t,bases_t_f,bases_t_f_300,leng_t,leng_t_f,x0,x1,x5,x10,x20,x50,x100,x200,x300,x500,x750,x1000,z0,z5,z10,z20,z50,z100,z200,z300,z500,z750,z1000,lx0, lx5, lx10, lx20, lx50, lx100, lx200, lx300,lx500, lx750, lx1000,ly0, ly5, ly10, ly20, ly50, ly100, ly200, ly300,ly500, ly750, ly1000 = self.coverage_count()
        bases_f = bases_t_f - bases_t
        leng_f = leng_t_f - leng_t

        file3 = open(self.bedcov_total, 'r')
        l3 = len(file3.readlines())
        file3.close()
        file3 = open(self.bedcov_total, 'r')
        bases_Total = 0
        for i in range(l3):
            temp3 = file3.readline()
            n3 = int(temp3.split('\t')[-1])
            bases_Total += n3
        file3.close()

        file4 = open(self.idxstats_file,'r')
        reads_mapped_idx = 0
        reads_missed_idx = 0
        for i in file4.readlines():
            n4 = int(i.split('\t')[2])
            n5 = int(i.split('\t')[3])
            reads_mapped_idx += n4
            reads_missed_idx += n5
        file4.close()

        file5 = open(self.flagstat,'r')
        data5 = file5.readlines()
        reads_total = data5[0].split(' ')[0]
        reads_mapped = data5[4].split(' ')[0]
        reads_paired = data5[5].split(' ')[0]
        reads_properly = data5[8].split(' ')[0]
        reads_different_chr = data5[11].split(' ')[0]
        reads_different_chrQ = data5[12].split(' ')[0]
        file5.close()

        self.summary_file = self.dir_path_1 + '_coverage.txt'
        file6 = open(self.summary_file, 'w')
        file6.write('Total reads\t' + reads_total + '(100%)')
        num1 = float(reads_mapped) / float(reads_total)
        num1 = self.percent_float(num1)
        file6.write('\nReads mapped to genome\t' + reads_mapped + '(' + num1 + ')')
        num2 = float(reads_properly) / float(reads_total)
        num2 = self.percent_float(num2)
        file6.write('\nReads properly mapped\t' + reads_properly + '(' + num2 + ')')
        num3 = float(reads_paired) / float(reads_total)
        num3 = self.percent_float(num3)
        file6.write('\nPaired mapped\t' + reads_paired + '(' + num3 + ')')
        num4 = float(reads_different_chr) / float(reads_total)
        num4 = self.percent_float(num4)
        file6.write('\nWith mate mapped to a different chr\t' + reads_different_chr + '(' + num4 + ')')
        num5 = float(reads_different_chrQ) / float(reads_total)
        num5 = self.percent_float(num5)
        file6.write('\nWith mate mapped to a different chr (mapQ>=5)\t' + reads_different_chrQ + '(' + num5 + ')')
        file6.write('\nBases mapped to genome(Mb)\t' + str('%.2f' % (bases_Total / 1048576.0)))
        file6.write('\nAverage read length\t' + str('%.2f' % (float(bases_Total) / float(reads_mapped))))
        file6.write('\nInitial bases on target\t' + str(leng_t))
        file6.write('\nInitial bases near target\t' + str(leng_f))
        file6.write('\nInitial bases on or near target\t' + str(leng_t_f))
        file6.write('\nBases mapped on target(Mb)\t' + str('%.2f' % (bases_t / 1048576.0)))
        file6.write('\nBases mapped near target(Mb)\t' + str('%.2f' % (bases_f / 1048576.0)))
        file6.write('\nBases mapped on or near target(Mb)\t' + str('%.2f' % (bases_t_f / 1048576.0)))
        num6 = float(bases_t) / float(bases_Total)
        num6 = self.percent_float(num6)
        file6.write('\nFraction of effective bases on target\t' + num6)
        num7 = float(bases_t_f) / float(bases_Total)
        num7 = self.percent_float(num7)
        file6.write('\nFraction of effective bases on or near target\t' + num7)
        num8 = float(bases_t_f_300) / float(bases_Total)
        num8 = self.percent_float(num8)
        file6.write('\nFraction of effective bases on or near target (300bp)\t' + num8)
        file6.write('\nMean depth on target\t' + str('%.2f' % (float(bases_t) / float(leng_t))))
        file6.write('\nMean depth near target\t' + str('%.2f' % (float(bases_f) / float(leng_f))))
        file6.write('\nMean depth on or near target\t' + str('%.2f' % (float(bases_t_f) / float(leng_t_f))))

        x0 = self.percent_float(x0)
        file6.write('\nTarget region coverage by count\t' + x0)
        x5 = self.percent_float(x5)
        file6.write('\nFraction of target covered with at least 5X\t' + x5)
        x10 = self.percent_float(x10)
        file6.write('\nFraction of target covered with at least 10X\t' + x10)
        x20 = self.percent_float(x20)
        file6.write('\nFraction of target covered with at least 20X\t' + x20)
        x50 = self.percent_float(x50)
        file6.write('\nFraction of target covered with at least 50X\t' + x50)
        x100 = self.percent_float(x100)
        file6.write('\nFraction of target covered with at least 100X\t' + x100)
        x200 = self.percent_float(x200)
        file6.write('\nFraction of target covered with at least 200X\t' + x200)
        x300 = self.percent_float(x300)
        file6.write('\nFraction of target covered with at least 300X\t' + x300)
        x500 = self.percent_float(x500)
        file6.write('\nFraction of target covered with at least 500X\t' + x500)
        x750 = self.percent_float(x750)
        file6.write('\nFraction of target covered with at least 750X\t' + x750)
        x1000 = self.percent_float(x1000)
        file6.write('\nFraction of target covered with at least 1000X\t' + x1000)

        z0 = self.percent_float(z0)
        file6.write('\nFlanking region coverage by count\t' + z0)
        z5 = self.percent_float(z5)
        file6.write('\nFraction of flanking region covered with at least 5X\t' + z5)
        z10 = self.percent_float(z10)
        file6.write('\nFraction of flanking region covered with at least 10X\t' + z10)
        z20 = self.percent_float(z20)
        file6.write('\nFraction of flanking region covered with at least 20X\t' + z20)
        z50 = self.percent_float(z50)
        file6.write('\nFraction of flanking region covered with at least 50X\t' + z50)
        z100 = self.percent_float(z100)
        file6.write('\nFraction of flanking region covered with at least 100X\t' + z100)
        z200 = self.percent_float(z200)
        file6.write('\nFraction of flanking region covered with at least 200X\t' + z200)
        z300 = self.percent_float(z300)
        file6.write('\nFraction of flanking region covered with at least 300X\t' + z300)
        z500 = self.percent_float(z500)
        file6.write('\nFraction of flanking region covered with at least 500X\t' + z500)
        z750 = self.percent_float(z750)
        file6.write('\nFraction of flanking region covered with at least 750X\t' + z750)
        z1000 = self.percent_float(z1000)
        file6.write('\nFraction of flanking region covered with at least 1000X\t' + z1000)

        lx0 = self.percent_float(lx0)
        file6.write('\nTarget region coverage by length\t' + lx0)
        lx5 = self.percent_float(lx5)
        file6.write('\nTarget region coverage by length with at least 5X\t' + lx5)
        lx10 = self.percent_float(lx10)
        file6.write('\nTarget region coverage by length with at least 10X\t' + lx10)
        lx20 = self.percent_float(lx20)
        file6.write('\nTarget region coverage by length with at least 20X\t' + lx20)
        lx50 = self.percent_float(lx50)
        file6.write('\nTarget region coverage by length with at least 50X\t' + lx50)
        lx100 = self.percent_float(lx100)
        file6.write('\nTarget region coverage by length with at least 100X\t' + lx100)
        lx200 = self.percent_float(lx200)
        file6.write('\nTarget region coverage by length with at least 200X\t' + lx200)
        lx300 = self.percent_float(lx300)
        file6.write('\nTarget region coverage by length with at least 300X\t' + lx300)
        lx500 = self.percent_float(lx500)
        file6.write('\nTarget region coverage by length with at least 500X\t' + lx500)
        lx750 = self.percent_float(lx750)
        file6.write('\nTarget region coverage by length with at least 750X\t' + lx750)
        lx1000 = self.percent_float(lx1000)
        file6.write('\nTarget region coverage by length with at least 1000X\t' + lx1000)

        ly0 = self.percent_float(ly0)
        file6.write('\nFlanking region coverage by length\t' + ly0)
        ly5 = self.percent_float(ly5)
        file6.write('\nFlanking region coverage by length at lease 5X\t' + ly5)
        ly10 = self.percent_float(ly10)
        file6.write('\nFlanking region coverage by length at lease 10X\t' + ly10)
        ly20 = self.percent_float(ly20)
        file6.write('\nFlanking region coverage by length at lease 20X\t' + ly20)
        ly50 = self.percent_float(ly50)
        file6.write('\nFlanking region coverage by length at lease 50X\t' + ly50)
        ly100 = self.percent_float(ly100)
        file6.write('\nFlanking region coverage by length at lease 100X\t' + ly100)
        ly200 = self.percent_float(ly200)
        file6.write('\nFlanking region coverage by length at lease 200X\t' + ly200)
        ly300 = self.percent_float(ly300)
        file6.write('\nFlanking region coverage by length at lease 300X\t' + ly300)
        ly500 = self.percent_float(ly500)
        file6.write('\nFlanking region coverage by length at lease 500X\t' + ly500)
        ly750 = self.percent_float(ly750)
        file6.write('\nFlanking region coverage by length at lease 750X\t' + ly750)
        ly1000 = self.percent_float(ly1000)
        file6.write('\nFlanking region coverage by length at lease 1000X\t' + ly1000)
        file6.close()

    def moving(self):
        target_dir = self.sam_path
        if self.outputdir == 'outputdir':
            new_dir = '/'.join(target_dir.split('/')[0:-1]) + '/coverage_summary_' + self.panel
            if os.path.exists(new_dir):
                pass
            else:
                os.makedirs(new_dir)
        else:
            try:
                new_dir = self.outputdir
                if not os.path.exists(new_dir):
                    os.makedirs(new_dir)
            except:
                print 'warning: Incorrect outputdir or permission error! Shift to default outputdir:'
                new_dir = '/'.join(target_dir.split('/')[0:-1]) + '/coverage_summary_' + self.panel
                if os.path.exists(new_dir):
                    pass
                else:
                    os.makedirs(new_dir)
        print new_dir

        command2 = 'mv ' + self.dir_path_1 + ' ' + new_dir
        command1 = 'mv ' + self.summary_file + ' ' + new_dir
        os.system(command2)
        if self.outputdir_log == 'log':
            os.system(command1)
        else:
            try:
                log_dir = self.outputdir_log
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                    pass
                print log_dir
                command3 = 'mv ' + self.summary_file + ' ' + log_dir
                os.system(command3)
            except:
                log_dir = new_dir
                print 'warning: Incorrect outputdir_log or permission error! Shift to default outputdir:'
                print log_dir
                os.system(command1)





if __name__ ==  '__main__':
    func = coverage_summary(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    func.samtools_idxstats()
    func.file_making()
    func.samtools_bedcov()
    func.samtools_flagstat()
    func.coverage_count()
    func.summary()
    func.moving()























