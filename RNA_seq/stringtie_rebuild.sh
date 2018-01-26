#############################################
##                                         ##
##  Author: ZhangChengsheng, @2018.01.25   ##
##                                         ##
#############################################


task_ctrl=$1
log_site=$2
file_name1=$3
stringtie_dir=$4
HISAT2_result_dir=$5
total_log=$6

software_stringtie=/public/source/software/bin/bin/stringtie


echo StringTie -m start at: `date` >> $log_site
$software_stringtie ${HISAT2_result_dir}/${file_name1}.sorted.bam -b $stringtie_dir -e -A ${stringtie_dir}/${file_name1}.m.genetab -G ${task_ctrl}/allsample_merge.gtf -C ${stringtie_dir}/${file_name1}.cov_refs_m.gtf -p $threads -o ${stringtie_dir}/${file_name1}.stringtie.out_m.gtf
echo StringTie -m exit code: $? >> $log_site
echo "$software_stringtie ${HISAT2_result_dir}/${file_name1}.sorted.bam -b $stringtie_dir -e -A ${stringtie_dir}/${file_name1}.m.genetab -G ${task_ctrl}/allsample_merge.gtf -C ${stringtie_dir}/${file_name1}.cov_refs_m.gtf -p $threads -o ${stringtie_dir}/${file_name1}.stringtie.out_m.gtf" >> $log_site
echo StringTie -m done at: `date` >> $log_site

