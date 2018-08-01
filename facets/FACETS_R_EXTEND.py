"""
Author: Zhang Chengsheng, @2018.06.12
Usage: python3 script.py [1] inputdir_with_facets [2]outputdir
"""

import os, sys


def run(dir1):

    file1 = dir1 + '/R.t'
    file2 = dir1 + '/R.ted'

    f_o = open(file2, 'w')

    with open(file1, 'r') as f:
        x1 = 0
        y1 = 0
        file_old = ''
        for i in f.readlines():
            line = i.strip().split('\t')
            x2 = float(line[0])
            y2 = float(line[2])
            chr = line[5]
            file = line[4]
            if file != file_old:
                file_old = file
                x1 = 0
                y1 = 0

            left = x1 + y1
            right = x2 - y2
            if (right - left) > 1000:
                middle = (left + right) / 2
                r = ((right - left) / 2) - 2
                text_new = str(middle) + '\tadd\t' + str(r) + '\t2\t' + file + '\t' + chr + '\n'
                f_o.write(text_new)

            f_o.write(i)
            x1, y1 = x2, y2
            file_old = file

    f_o.close()

if __name__ == '__main__':
    dir1 = sys.argv[1]
    run(dir1)
