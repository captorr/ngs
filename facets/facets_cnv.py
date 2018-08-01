"""
Python3 script
Author: Zhang Chengsheng, @2018.06.12
Usage: python3 script.py [1] inputdir_with_facets [2]outputdir
"""

import os, sys


def run(inputdir, outputdir):

    Rscript = os.path.dirname(os.path.realpath(sys.argv[0])) + '/facets_cnv.R'

    if not os.path.isfile(Rscript):
        sys.stdout.write("error: can't find facets_cnv.R")

    file_list = [i for i in os.listdir(inputdir) if i.endswith('.facets')]

    for i in file_list:
        cmd = 'rscript ' + Rscript + ' ' + inputdir + '/' + i + ' ' + str(i.split('.')[0]) + ' ' + outputdir
        os.system(cmd)

if __name__ == '__main__':
    inputdir = sys.argv[1]
    outputdir = sys.argv[2]
    run(inputdir, outputdir)
