#############################################
##                                         ##
##  Author: ZhangChengsheng, @2018.01.18   ##
##                                         ##
#############################################


clean_fq_11=$1
clean_fq_22=$2
file_name1=$3
HISAT2_result_dir=$4
threads=$5
stringtie_dir=$6
log_site=$7
total_log=$8


software_HISAT2=/public/source/cszhang/software/hisat2-2.1.0/hisat2
HISAT2_genome=/public/source/share/lai_test/homo/grch38_snp_tran/genome_snp_tran
genome_gtf=/public/source/share/zcs_temp/homo/Homo_sapiens.GRCh38.89.chr.gtf
software_samtools=/public/source/software/samtools/samtools
software_stringtie=/public/source/software/bin/bin/stringtie
software_python=/public/source/cszhang/software/python27/bin/python
python_sort=/public/source/share/zcs_temp/RNAseq/genetab_sort.py


if ! [ -d "$HISAT2_result_dir" ];then
    mkdir "$HISAT2_result_dir"
fi

echo $file_name1 sh1 start at: `date` >> $total_log
echo work start at: `date` >> $log_site
HISAT2_outputfile=${HISAT2_result_dir}/${file_name1}.sam
cd $HISAT2_result_dir
echo HISAT2 start at:    `date` >> $log_site
$software_HISAT2 -p $threads --dta --new-summary --summary-file ${HISAT2_outputfile}.summary --novel-splicesite-outfile ${HISAT2_outputfile}.novelsplicesit -x $HISAT2_genome -1 $clean_fq_11 $clean_fq_22 -S $HISAT2_outputfile > ${HISAT2_outputfile}.log 2>&1
echo HISAT2 exit code: $? >> $log_site
echo "HISAT2 command: $software_HISAT2 -p $threads --dta --new-summary --summary-file ${HISAT2_outputfile}.summary --novel-splicesite-outfile ${HISAT2_outputfile}.novelsplicesit -x $HISAT2_genome -1 $clean_fq_11 $clean_fq_22 -S $HISAT2_outputfile > ${HISAT2_outputfile}.log 2>&1" >> $log_site

echo samtools start at:    `date` >> $log_site
$software_samtools sort -@ $threads -O sam -o ${HISAT2_outputfile}.sorted $HISAT2_outputfile
samtools_1=$?
$software_samtools view -b -S ${HISAT2_outputfile}.sorted > ${file_name1}.sorted.bam
samtools_2=$?
$software_samtools index ${file_name1}.sorted.bam
samtools_3=$?
echo samtools exit code: 'sort:' $samtools_1 'view:' $samtools_2 'index:' $samtools_3 >> $log_site

#-e

if ! [ -d "$stringtie_dir" ];then
    mkdir "$stringtie_dir"
fi

cd $stringtie_dir
echo stringtie start at:    `date` >> $log_site
$software_stringtie ${HISAT2_result_dir}/${file_name1}.sorted.bam -b $stringtie_dir -e -A ${stringtie_dir}/${file_name1}.e.genetab -G $genome_gtf -C ${stringtie_dir}/${file_name1}.cov_refs_e.gtf -p $threads -o ${stringtie_dir}/${file_name1}.stringtie.out_e.gtf
stringtie_e=$?
$software_stringtie ${HISAT2_result_dir}/${file_name1}.sorted.bam -b $stringtie_dir -A ${stringtie_dir}/${file_name1}.genetab -G $genome_gtf -C ${stringtie_dir}/${file_name1}.cov_refs.gtf -p $threads -o ${stringtie_dir}/${file_name1}.stringtie.out.gtf
stringtie_m=$?
echo stringtie exit code: 'e:' $stringtie_e 'm:' $stringtie_m >> $log_site
echo "stringtie command: $software_stringtie ${HISAT2_result_dir}/${file_name1}.sorted.bam -b $stringtie_dir -e -A ${stringtie_dir}/${file_name1}.genetab -G $genome_gtf -C ${stringtie_dir}/${file_name1}.cov_refs.gtf -p $threads -o ${stringtie_dir}/${file_name1}.stringtie.out.gtf" >> $log_site
$software_python $python_sort ${stringtie_dir}/${file_name1}.genetab

echo work finished at: `date` >> $log_site
echo $file_name1 sh1 finished at: `date` >> $total_log
