#############################################
##                                         ##
##  Author: ZhangChengsheng, @2018.01.24   ##
##                                         ##
#############################################


task_ctrl=$1
log_site=$2


software_stringtie=/public/source/software/bin/bin/stringtie
genome_gtf=/public/source/share/zcs_temp/homo/Homo_sapiens.GRCh38.89.chr.gtf


for i in `ls "$task_ctrl"/*.config`;
do
#${stringtie_dir}/${file_name1}.stringtie.out.gtf
line=`grep "StringTie_result_dir" $i | cut -d ":" -f 2`/`grep "file_name" $i | cut -d ":" -f 2`.stringtie.out.gtf
config_line="$config_line $line"
done



echo StringTie --merge start at: `date` >> $log_site
$software_stringtie --merge -G $genome_gtf -o $task_ctrl/allsample_merge.gtf $config_line
echo StringTie --merge exit code: $? >> $log_site
echo "$software_stringtie --merge -G $genome_gtf -o $task_ctrl/allsample_merge.gtf $config_line" >> $log_site
echo StringTie --merge done at: `date` >> $log_site


