"""
python2&3 script
Author: Zhang Chengsheng, @2019.04.24
"""

import os,sys
import multiprocessing
import shutil


def file_copy(ori,new,replace):
    if os.path.exists(new) and not replace:
        return
    sys.stdout.write("copy {} ...\n".format(ori))
    shutil.copy(ori,new)


def dir_copy(ori_dir,new_dir,process,replace):
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    p = multiprocessing.Pool(processes=process)
    count = 0
    for paths in os.walk(ori_dir):
        path = paths[0]
        new_path = path.replace(ori_dir, new_dir)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        files = [i for i in os.listdir(path)]
        for file in files:
            new_file = os.path.join(new_path, file)
            p.apply_async(file_copy,args=(os.path.join(path, file), new_file, replace))
            count += 1
    p.close()
    p.join()


def options(argv):
    from argparse import ArgumentParser as AP
    usages = "python {} -i [origin_directory] -o [target_directory] -p [process]".format(argv[0])
    description = "copy files iteratively from one directory to another directory."
    p = AP(usage=usages,description=description)
    p.add_argument("-i", dest="dir_in", metavar="dir_in", help="origin_directory")
    p.add_argument("-o", dest="dir_out", metavar="dir_out", help="target_directory")
    p.add_argument("-p", dest="process", metavar="[int]", help="process, default: 1", type=int, default=1)
    p.add_argument("-r", dest="replace", metavar="[bool]", help="replace target file if it exist, default:false", type=bool, default=False)
    if len(argv) == 1:
        p.print_help()
        exit(1)
    return p.parse_args(argv[1:])


def main():
    args = options(sys.argv)
    dir_copy(args.dir_in,args.dir_out,args.process,args.replace)


if __name__ == '__main__':
    main()