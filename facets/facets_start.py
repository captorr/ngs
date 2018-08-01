"""
Author: Zhang Chengsheng, @2018.06.14
Usage: python3 script.py
"""

import os, sys, time
import FACETS_R
import FACETS_PLOIDY
import facets_cnv
import FACETS_R_EXTEND

input_dir = input('Please type folder path of .facets files: ')
output_dir = input('Please type output folder path:')
facets_cnv.run(input_dir, output_dir)
FACETS_R.run(input_dir, output_dir)
FACETS_PLOIDY.run(input_dir, output_dir)
FACETS_R_EXTEND.run(output_dir)

R_S = os.path.dirname(os.path.realpath(sys.argv[0])) + '/facets_png.R'
cmd = 'rscript ' + R_S + ' ' + output_dir
os.system(cmd)
sys.stdout.write('\n')
for i in range(5):
    sys.stdout.write(str(5-i)+'\r')
    time.sleep(1)
