"""
Author: Zhang Chengsheng, @2018.06.12
Usage: python3 script.py [1] inputdir_with_facets [2]outputdir
"""

import os, sys

dict_chr = {'0': 0,
            '1': 249250621,
            '2': 243199373,
            '3': 198022430,
            '4': 191154276,
            '5': 180915260,
            '6': 171115067,
            '7': 159138663,
            '8': 146364022,
            '9': 141213431,
            '10': 135534747,
            '11': 135006516,
            '12': 133851895,
            '13': 115169878,
            '14': 107349540,
            '15': 102531392,
            '16': 90354753,
            '17': 81195210,
            '18': 78077248,
            '19': 59128983,
            '20': 63025520,
            '21': 48129895,
            '22': 51304566,
            '23': 155270560}


def dict_plus(num):
    out = 0
    for i in range(int(num)):
        out += dict_chr[str(i)]
    return out


def data_reshade(txt, num, filename):
    global file_out_o
    with open(txt, 'r') as f:
        count = 0
        for i in f.readlines():
            count += 1
            if count > 1:
                line = i.strip().split('\t')
                start = line[0]
                end = line[1]
                chr = line[2]
                tcn = line[12]
                if int(tcn) > 6:
                    tcn = '7'
                x = str((int(end) + int(start)) / 2 + int(dict_plus(chr)))
                width = str((int(end) - int(start)) / 2)
                if chr == '23':
                    chr = 'X'
                file_out_o.write(x + '\t' + str(num) + '\t' + width + '\t' + tcn + '\t' + filename + '\t' + chr + '\n')


def add(R_chr):
    chr_chr = R_chr
    with open(chr_chr, 'w') as f:
        count = 0
        for i in dict_chr:
            if i == '23':
                f.write('X')
            else:
                f.write(str(i))
            f.write('\t')
            f.write(str(count + dict_chr[i]/2))
            count += dict_chr[i]
            f.write('\t')
            f.write(str(count))
            f.write('\n')


def run(dir1, outputdir):
    global file_out_o

    file_list = [i for i in os.listdir(outputdir) if i.endswith('.txt')]
    out = outputdir + '/R.t'
    file_out_o = open(out, 'w')
    R_chr = outputdir + '/R.chr'
    count = 0
    for i in file_list:
        count += 1
        data_reshade(outputdir + '/' + i, str(count), i.split('.')[0])
    file_out_o.close()
    add(R_chr)

if __name__ == '__main__':
    dir1 = sys.argv[1]
    outputdir = sys.argv[2]
    run(dir1, outputdir)
