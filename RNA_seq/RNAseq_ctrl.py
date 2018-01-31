"""
Author: Zhang Chengsheng, @2018.01.23
-------------------------------------
children shell script:
/public/source/share/zcs_temp/RNA_workflow/RNA_workflow.sh    #line77
/public/source/share/zcs_temp/RNA_workflow/RNA_workflow2.sh    #line81
/public/source/share/zcs_temp/RNA_workflow/stringTie_merge.sh    #line201
/public/source/share/zcs_temp/RNA_workflow/stringtie_rebuild.sh    #line92
"""

import sys,os,getopt,time

def config_making(target_dir,clean1,clean2,file_name,HISAT2,stringtie,QE,density,region,threads,log,species,nodes,block):
    target_dir = target_dir
    conf_file = target_dir + '/' + file_name + '.config'
    file1 = open(conf_file,'w')
    b_info = '#original file:' + conf_file + '\n'
    t_info = '#made at:' + time.asctime() + '\n'
    u_info = '#user:' + str(os.popen('whoami').read().strip()) + '\n'
    file1.write("#RNA-seq workflow parameter configure\n")
    file1.write(b_info)
    file1.write(t_info)
    file1.write(u_info)
    file1.write("clean_fastq_1:" + clean1 + "\n")
    file1.write("clean_fastq_2:" + clean2 + "\n")
    file1.write("file_name:" + file_name + "\n")
    file1.write("HISAT2_result_dir:" + HISAT2 + "\n")
    file1.write("StringTie_result_dir:" + stringtie + "\n")
    file1.write("QE_result_dir:" + QE + "\n")
    file1.write("Density_result_dir:" + density + "\n")
    file1.write("Region_result_dir:" + region + "\n")
    file1.write("threads:" + threads + "\n")
    file1.write("log_file:" + log + "\n")
    file1.write("species:" + species + "\n")
    file1.write("nodes:" + nodes + "\n")
    file1.write("block:" + block + "\n")
    file1.close()
    return conf_file


def shell_making(sh1,sh2,config,task_ctrl,total_log,ST_m2='none'):
    outputdir = task_ctrl + '/shell'
    file1 = open(sh1,'w')
    file2 = open(sh2,'w')
    file_config = open(config,'r')
    config_dict = {}
    for i in file_config.readlines():
        if not i.startswith('#') and ':' in i:
            try:
                line = i.strip('\n').split(':')
                config_dict[line[0]] = line[1]
            except:
                continue
    file_config.close()
    try:
        fq1 = str(config_dict["clean_fastq_1"])
        fq2 = str(config_dict["clean_fastq_2"])
        file_name = str(config_dict["file_name"])
        HISAT2 = str(config_dict["HISAT2_result_dir"])
        Stringtie = str(config_dict["StringTie_result_dir"])
        QE = str(config_dict["QE_result_dir"])
        density = str(config_dict["Density_result_dir"])
        region = str(config_dict["Region_result_dir"])
        threads = str(config_dict["threads"])
        log = str(config_dict["log_file"])
        species = str(config_dict["species"])
        nodes = str(config_dict["nodes"])
        block = str(config_dict["block"])
    except Exception as e:
        print e
        print "error in RNAseq_ctrl shell_making: illegal config !"
        config_file()
        exit(1)

    PBS_header = '#PBS -l nodes=1:ppn=' + threads + '\n#PBS -q ' + nodes + '\ncd ' + outputdir + '\n'
    file1.write(PBS_header)
    sh1_cmd = "sh /public/source/share/zcs_temp/RNA_workflow/RNA_workflow.sh " + fq1 + " " + fq2 + " " + file_name + " " + HISAT2 + " " + threads + " " + Stringtie + " " + log + " " + total_log + "\n"
    file1.write(sh1_cmd)
    file1.close()
    file2.write(PBS_header)
    sh2_cmd = "sh /public/source/share/zcs_temp/RNA_workflow/RNA_workflow2.sh " + fq1 + " " + fq2 + " " + file_name + " " + threads + " " + QE + " " + density + " " + log + " " + region + " " + HISAT2 + "/" + file_name + ".sorted.bam" + " " + block + " " + species + "\n"
    file2.write(sh2_cmd)
    file2.close()

    #----------------------------------stringtie_merge-------------------------------------#

    #----------------------------------stringtie_merge_single-------------------------------------#
    PBS_header_ST2 = '#PBS -l nodes=1:ppn=' + threads + '\n#PBS -q ' + nodes + '\ncd ' + outputdir + '\n'
    if ST_m2 != "none":
        file4_o = open(ST_m2,'w')
        file4_o.write(PBS_header_ST2)
        sh4_cmd = "sh /public/source/share/zcs_temp/RNA_workflow/stringtie_rebuild.sh " + task_ctrl + " " + log + " " + file_name + " " + Stringtie + " " + HISAT2 + " " + threads + "\n"
        file4_o.write(sh4_cmd)
        file4_o.close()









def main(input_dir,outputdir,threads, species, nodes, block,total_log,merge):
    #global threads, species, nodes, block
    file_name = [input_dir + '/' + i for i in os.listdir(input_dir) if i.endswith('.clean.fq') or i.endswith('.clean.fastq')]
    couple = []
    if len(file_name) % 2 == 0:
        file_name = sorted(file_name)
        for i in range(len(file_name) / 2):
            couple.append([file_name[2 * i], file_name[2 * i + 1]])
    else:
        print 'error: have a single one .fq/.fastq file.'
        exit()

    if outputdir == 'none':
        task_ctrl = '/'.join(input_dir.split('/')[:-1]) + '/task_ctrl'
        outputdir = '/'.join(input_dir.split('/')[:-1])
        if not os.path.exists(task_ctrl):
            os.makedirs(task_ctrl)
    else:
        if not os.path.exists(outputdir):
            try:
                os.makedirs(outputdir)
                print 'outputdir path: ', outputdir
            except Exception as e:
                print e
                print "error: can't make outputdir!"
                exit(1)
        task_ctrl = outputdir + '/task_ctrl'
        if not os.path.exists(task_ctrl):
            try:
                os.makedirs(task_ctrl)
            except Exception as e:
                print e
                print "error: can't make task_ctrl dir!"
                exit(1)

    if total_log == 'none':
        total_log = task_ctrl + '/TOTAL.log'
    else:
        try:
            if not os.path.exists(total_log):
                t = open(total_log,'w')
                t.close()
        except Exception as e:
            print e
            print "error: can't make log file!"
            exit(1)

    command_list = []
    command_list2 = []
    file_num = 0
    for i in couple:
        file_num += 1
        fq_name1 = '_'.join(i[0].split('/')[-1].split('.')[0].split('_')[:-1])
        fq_name2 = '_'.join(i[1].split('/')[-1].split('.')[0].split('_')[:-1])
        fq_name = '_'.join(i[0].split('/')[-1].split('.')[0].split('_')[1:3])
        if fq_name1 == fq_name2:
            log = task_ctrl + '/' + fq_name + '.log'
            conf_file = config_making(task_ctrl,i[0],i[1],fq_name,outputdir+'/HISAT2_result',outputdir+'/StringTie_result',outputdir+'/QE_result',outputdir+'/density_result',outputdir+'/region_result',threads,log,species,nodes,block)
            if not os.path.exists(task_ctrl + '/shell'):
                try:
                    os.makedirs(task_ctrl + '/shell')
                    sh1 = task_ctrl + '/shell/' + fq_name + '.1.sh'
                    sh2 = task_ctrl + '/shell/' + fq_name + '.2.sh'
                    #ST_m = task_ctrl + '/shell/' + fq_name + '.3.sh'
                    if merge:
                        ST_m2 = task_ctrl + '/shell/' + fq_name + '.4.sh'
                    else:
                        ST_m2 = 'none'
                except:
                    print "error: can't makedir of 'task_ctrl/shell' !"
                    exit(1)
            else:
                sh1 = task_ctrl + '/shell/' + fq_name + '.1.sh'
                sh2 = task_ctrl + '/shell/' + fq_name + '.2.sh'
                if merge:
                    ST_m2 = task_ctrl + '/shell/' + fq_name + '.4.sh'
                else:
                    ST_m2 = 'none'
            shell_making(sh1,sh2,conf_file,task_ctrl,total_log,ST_m2)
            q_sh = task_ctrl + '/' + fq_name + '.q'
            q_sh_o = open(q_sh,'w')
            q_sh_o.write("work1=$(qsub -d " + task_ctrl + "/shell " + sh1 + ")\n")
            command_list.append("work" + str(file_num) + "=$(qsub -d " + task_ctrl + "/shell " + sh1 + ")\n")
            q_sh_o.write("qsub -d " + task_ctrl + "/shell -W depend=afterok:$work1 " + sh2 + "\n")
            command_list.append("qsub -d " + task_ctrl + "/shell -W depend=afterok:$work" + str(file_num) + " " + sh2 + "\n")
            q_sh_o.close()
            command_list2.append("qsub -d " + task_ctrl + "/shell -W depend=afterok:$jobid_replaced " + ST_m2 + "\n")
        else:
            print 'error: have miss matching'
            print i[0]
            print i[1]
            exit(1)
    if merge:
        ST_m = task_ctrl + '/shell/' + 'stringtie_merge.3.sh'
        PBS_header_ST = str('#PBS -l nodes=1:ppn=1\n#PBS -q ' + nodes + '\ncd ' + task_ctrl + '/shell\n')
        file3_o = open(ST_m, 'w')
        file3_o.write(PBS_header_ST)
        sh3_cmd = "sh /public/source/share/zcs_temp/RNA_workflow/stringTie_merge.sh " + task_ctrl + " " + total_log + "\n"
        file3_o.write(str(sh3_cmd))
        file3_o.close()

        start_file = open(task_ctrl + '/q.start', 'w')
        start_file.write('cd ' + task_ctrl + '\n')
        for i in range(len(command_list)):
            start_file.write(command_list[i])

        start_file.write("merge=$(qsub -d " + task_ctrl + "/shell -W depend=afterok")
        for i in range(file_num):
            start_file.write(':$work' + str(i+1))
        start_file.write(" " + ST_m + ")\n")

        for i in range(len(command_list2)):
            start_file.write(str(command_list2[i]).replace('jobid_replaced','merge'))

    else:
        start_file = open(task_ctrl + '/q.start', 'w')
        start_file.write('cd ' + task_ctrl)
        start_file.write('\nfor file in ' + task_ctrl + '/*.q\n')
        start_file.write('do\n')
        start_file.write('sh $file\n')
        start_file.write('sleep 0.1\n')
        start_file.write('done')
        start_file.close()

    print task_ctrl



def help1():
    print '\n***************************************************'
    print 'Workflow of RNA-seq analysis. Input: clean fastq dir'
    print 'Author: Zhang Chengsheng'
    print '---------------------------------------------------'
    print 'Usage:  python script.py [1]input_dir [option]'
    print '-h --help:  show help infomations and config file details.'
    print '-p [int] --process [int]:  process required.  #default: 8'
    print '-o [dirpath] --output [dirpath]:  output_dir  #default:parent directory of input_dir.'
    print '-s [str] --species [str]: species.supported:[human].  #default: human.'
    print '-n [str] --nodes [str]: choose the nodes in [long,short].  #default: long.'
    print '-b [int] --block [int]: set the block of density analysis.  #default: 500000'
    print '-r --run:  run automatically  #default:manually' #underworked
    print '-l [filepath] --log [filepath]: set the path of TOTAL.log.  #default:parent directory of input_dir'
    print "-m --merge: merge all transcripts into one.  #default: doesn't merge"
    print '---------------------------------------------------'
    print '***************************************************\n'

def config_file():
    print '\n*******************config_file*********************'
    print '==================================================='
    print "config file only set for single task and must contain these 13 rows splitted by ':'(need not in order)  :"
    print 'clean_fastq_1,clean_fastq_2,file_name,HISAT2_result_dir,StringTie_result_dir,'
    print 'QE_result_dir,Density_result_dir,Region_result_dir,threads,log_file,species,nodes,block'
    print '---------------------example-----------------------'
    print 'clean_fastq_1:abs_path/foo_bar_1.clean.fq'
    print 'clean_fastq_2:abs_path/foo_bar_2.clean.fq'
    print 'file_name:file_id'
    print 'HISAT2_result_dir:abs_path/HISAT2_result'
    print 'StringTie_result_dir:abs_path/stringtie_result'
    print 'QE_result_dir:abs_path/QE_result'
    print 'Density_result_dir:abs_path/density_result'
    print 'Region_result_dir:abs_path/region_result'
    print 'threads:8'
    print 'log_file:abs_path/task_ctrl/file_id.log'
    print 'species:human'
    print 'nodes:long'
    print 'block:500000'
    print '==================================================='
    print '***************************************************\n'


def option(argv):
    global species,run1,nodes,block,threads,output,total_log,merge
    try:
        opt, value = getopt.getopt(argv, 'hp:o:s:n:b:rl:m', ['help', 'process=', 'output=', 'species=', 'nodes=', 'block=','run','log=','merge'])
        for name, value in opt:
            if name in ('-h', '--help'):
                help1()
                config_file()
                exit(1)
            if name in ('-o','--output'):
                output = value
            if name in ('-p', '--process'):
                threads = value
            if name in ('-s','-species'):
                species = value
            if name in ('-n', '--nodes'):
                nodes = value
            if name in ('-b', '--block'):
                block = value
            if name in ('-r', '--run'):
                run1 = True
            if name in ('-l','--log'):
                total_log = value
            if name in ('-m','--merge'):
                merge = True

    except:
        help1()
        print 'parameters error!'
        exit(1)

species = 'human'
run1 = False
nodes = 'long'
block = '500000'
output = 'none'
threads = '8'
total_log = 'none'
merge = False

if len(sys.argv) < 2:
    help1()
    exit(1)
if len(sys.argv) >= 2:
    if not os.path.exists(sys.argv[1]):
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            help1()
            config_file()
        else:
            help1()
            print 'input dir not exist!'
        exit(1)
option(sys.argv[2:])
main(sys.argv[1],output,threads, species, nodes, block, total_log, merge)
