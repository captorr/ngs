"""
Author: Zhang Chengsheng, @2018.11.13
Usage: python scripts.py -i [file_in] -o [overlap] -l [length]

script for splitting sequence into parts with given length and overlap size.
"""

import os,sys
from argparse import ArgumentParser as AP


def options(argv):
    usages = "python3 {} -i file_in -l [length] -o [overlap]".format(argv[0])
    description = "script for splitting sequence into parts with given length and overlap size."
    p = AP(usage=usages,description=description)
    p.add_argument("-i", dest="file_in", metavar="file_in", help="Sequence file in format of txt")
    p.add_argument("-o", dest="overlap", metavar="[int]", help="overlap size.", type=int)
    p.add_argument("-l", dest="length", metavar="[int]", help="sequence length after splitted", type=int)
    p.add_argument("-s", dest="start", metavar="[left/right]", choices=["left", "right"],
                   help="Sequence split start from left or right. (default: left)", default="left")
    p.add_argument("-t", dest="transform", action="store_true",
                   help="Output sequence in transform. (default: False)",default=False)
    p.add_argument("-w", dest="inturn", action="store_true",
                   help="Output sequence in turn of transformed or not, the first sequence depend on option -t. (default: False)",default=False)
    p.add_argument("-r", dest="report", action="store_true",
                   help="print sequence split result on screen. (default: False)", default=False)

    if len(argv) == 1:
        p.print_help()
        exit(1)
    return p.parse_args(argv[1:])


def trans(seq, transform=True,reverse=False):
    dict1 = {"A":"T",
             "T":"A",
             "G":"C",
             "C":"G",
             "a":"t",
             "t":"a",
             "c":"g",
             "g":"c"}
    new_seq = ""
    if transform:
        for i in seq:
            new_seq += dict1[i] if i in dict1 else i
    else:
        new_seq = seq
    if reverse:
        new_seq = new_seq[::-1]

    return new_seq


def overlap_split(file_in, overlap, ave_length, start="left", transform=False, inturn=False, report=False):
    seq = ""
    transformm = transform
    with open(file_in, 'r') as f:
        for i in f.readlines():
            seq += i.strip()
    if report:
        sys.stdout.write(seq + '\n')
    o1 = open(file_in + '_withgap.txt', 'w')
    o2 = open(file_in + '_withoutgap.txt', 'w')
    o1.write(seq + '\n')
    o2.write(seq + '\n')
    for idx, i in enumerate(range(0, len(seq), ave_length - overlap)):
        if start == "right":
            right = len(seq) - i
            left = right-ave_length
        else:
            left = i
            right = left + ave_length
        if left < 0:
            left = 0
        seq_real = seq[left:right]
        if inturn:
                transformm = False if abs(idx % 2 - transform) else True
        seq_real = trans(seq_real, transform=transformm)
        if report:
            sys.stdout.write("-" * left + seq_real + '\n')
        o1.write("-" * left + seq_real + '\n')
        o2.write(seq_real + '\n')
        if start == "right" and left == 0:
            break
        if start == "left" and right > len(seq):
            break

    o1.close()
    o2.close()
    sys.stdout.write("\nfinished!\n")
    sys.stdout.write("output file in: \n{}\n{}\n".format(file_in + '_withgap.txt', file_in + '_withoutgap.txt'))


def main():
    args = options(sys.argv)
    overlap_split(args.file_in, args.overlap, args.length, args.start, args.transform, args.inturn, args.report)


if __name__ == '__main__':
    main()


