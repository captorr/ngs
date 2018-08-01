"""
Author: Zhang Chengsheng, @2018.06.12
Usage: python3 scripts.py [1]facets_dir
"""

import os, sys


def run(dir1, outputdir):

    file_list = [i for i in os.listdir(outputdir) if i.endswith('.txt')]

    out = outputdir + '/R.ploidy'
    out_o = open(out, 'w')

    for i in sorted(file_list):
        with open(outputdir + '/' + i, 'r') as f:
            count = 0
            for line in f.readlines():
                count += 1
                if count > 1:
                    ploidy = str(line.strip().split('\t')[-1])
                    out_o.write(i.split('.')[0])
                    out_o.write('\t')
                    out_o.write(ploidy)
                    out_o.write('\n')
                    break
    out_o.close()

if __name__ == '__main__':
    dir1 = sys.argv[1]
    outputdir = sys.argv[2]
    run(dir1, outputdir)
