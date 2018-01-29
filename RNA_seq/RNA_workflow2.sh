#############################################
##                                         ##
##  Author: ZhangChengsheng, @2018.01.18   ##
##                                         ##
#############################################


clean_fq_11=$1
clean_fq_22=$2
file_name1=$3
threads=$4
QE_result_dir=$5
density_result_dir=$6
log_site=$7
RNA_region_result=$8
HISAT2_bam_file=$9
block=${10}  #500000
species=${11}  #human
total_log=${12}

software_python=/public/source/cszhang/software/python27/bin/python
software_pypy=/public/source/cszhang/bin/pypy
python_GC_error=/public/source/share/zcs_temp/QC/GC_error.py
python_density=/public/source/share/zcs_temp/RNAseq/reads_density.py
python_region=/public/source/share/zcs_temp/region/RNA_region_stat.py

echo $file_name1 sh2 start at: `date` >> $total_log
echo work start at: `date` >> $log_site
if ! [ -d "$QE_result_dir" ];then
    mkdir "$QE_result_dir"
fi
cd $QE_result_dir
echo GC_error stat start at: `date` >> $log_site
$software_pypy $python_GC_error $clean_fq_11 $clean_fq_22 $threads $QE_result_dir
echo GC_error exit code: $? >> $log_site
echo "GC_error command: $software_pypy $python_GC_error $clean_fq_11 $clean_fq_22 $threads $QE_result_dir" >> $log_site

if ! [ -d "$density_result_dir" ];then
    mkdir "$density_result_dir"
fi
if ! [ -d "$density_result_dir/$file_name1" ];then
    mkdir "$density_result_dir/$file_name1"
fi
cd "$density_result_dir/$file_name1"
echo density stat start at: `date` >> $log_site
$software_python $python_density $HISAT2_bam_file $density_result_dir/$file_name1 $block $threads none none $species
echo density exit code: $? >> $log_site
echo "density command: $software_python $python_density $HISAT2_bam_file $density_result_dir/$file_name1 $block $threads none none $species" >> $log_site


if ! [ -d "$RNA_region_result" ];then
    mkdir "$RNA_region_result"
fi
if ! [ -d "$RNA_region_result/$file_name1" ];then
    mkdir "$RNA_region_result/$file_name1"
fi
cd "$RNA_region_result/$file_name1"
echo region stat start at: `date` >> $log_site
$software_python $python_region $HISAT2_bam_file $RNA_region_result/$file_name1 none none $file_name1 $species
echo region exit code: $? >> $log_site
echo "region comand: $software_python $python_region $HISAT2_bam_file $RNA_region_result/$file_name1 none none $file_name1 $species" >> $log_site

echo work finished at: `date` >> $log_site
echo $file_name1 sh2 finished at: `date` >> "$total_log"



