################################################
##                                            ##
##  Author: Zhang Chengsheng, @2018.03.28     ##
##                                            ##
################################################


fq_1=$1
fq_2=$2
threads=$3  #8
outputdir=$4
log_site=$5


software_STAR=/public/source/share/zcs_temp/software/STAR
genome_dir=/public/source/cszhang/test/180313/ensembl_genome/STAR
hg38=/public/source/cszhang/test/180313/ensembl_genome/STAR/Homo_sapiens.GRCh38.fa
hg38_GATK=/public/source/cszhang/test/180313/ensembl_genome/Homo_sapiens.GRCh38.fa
software_picard=/public/source/share/zcs_temp/picard.jar
software_annovar_1=/public/source/cszhang/software/annovar/convert2annovar.pl
software_annovar_2=/public/source/cszhang/software/annovar/table_annovar.pl
software_annovar_db=/public/source/cszhang/software/annovar/humandb/

if ! [ -d "$outputdir" ];then
    mkdir "$outputdir"
fi
cd $outputdir

outputdir_pass1=${outputdir}/STAR-pass1
if ! [ -d "$outputdir_pass1" ];then
    mkdir "$outputdir_pass1"
fi
cd $outputdir_pass1
echo $fq_1 STAR-1 pass start at: `date` >> $log_site
$software_STAR --genomeDir $genome_dir --readFilesIn $fq_1 $fq_2 --runThreadN $threads #13G 10min
echo $fq_1 STAR-1 exit code: $? >> $log_site

genome_dir_new=${outputdir}/genome_pass2
if ! [ -d "$genome_dir_new" ];then
    mkdir "$genome_dir_new"
fi
cd $genome_dir_new
echo $fq_1 STAR-1 index start at: `date` >> $log_site
$software_STAR --runMode genomeGenerate --genomeDir $genome_dir_new --genomeFastaFiles $hg38 --sjdbFileChrStartEnd ${outputdir_pass1}/SJ.out.tab --sjdbOverhang 75 --runThreadN $threads #13G 40min
echo $fq_1 STAR-1 index exit code: $? >> $log_site

outputdir_pass2=${outputdir}/STAR-pass2
if ! [ -d "$outputdir_pass2" ];then
    mkdir "$outputdir_pass2"
fi
cd $outputdir_pass2
echo $fq_1 STAR-2 pass start at: `date` >> $log_site
$software_STAR --genomeDir $genome_dir_new --readFilesIn $fq_1 $fq_2 --runThreadN $threads #13G 40min
echo $fq_1 STAR-2 exit code: $? >> $log_site


outputdir_picard=${outputdir}/picard
if ! [ -d "$outputdir_picard" ];then
    mkdir "$outputdir_picard"
fi
cd $outputdir_picard
echo $fq_1 picard AddOrReplaceReadGroups Start at: `date` >> $log_site
java -jar $software_picard AddOrReplaceReadGroups I=${outputdir_pass2}/Aligned.out.sam O=${outputdir_picard}/rg_added_sorted.bam SO=coordinate RGID=id RGLB=library RGPL=platform RGPU=machine RGSM=sample #13G 24min
echo $fq_1 picard AddOrReplaceReadGroups exit code: $? >> $log_site
echo $fq_1 picard MarkDuplicates Start at: `date` >> $log_site
java -jar $software_picard MarkDuplicates I=${outputdir_picard}/rg_added_sorted.bam O=${outputdir_picard}/dedupped.bam  CREATE_INDEX=true VALIDATION_STRINGENCY=SILENT M=output.metrics #13G 24min
echo $fq_1 picard MarkDuplicates exit code: $? >> $log_site

outputdir_GATK=${outputdir}/GATK4
if ! [ -d "$outputdir_GATK" ];then
    mkdir "$outputdir_GATK"
fi
cd $outputdir_GATK
echo $fq_1 GATK4 SplitNCigarReads Start at: `date` >> $log_site
GATK4 SplitNCigarReads -R $hg38_GATK -I ${outputdir_picard}/dedupped.bam -O ${outputdir_GATK}/split.bam #90min
echo $fq_1 GATK4 HaplotypeCaller exit code: $? >> $log_site
echo $fq_1 GATK4 HaplotypeCaller Start at: `date` >> $log_site
GATK4 HaplotypeCaller -R $hg38_GATK -I ${outputdir_GATK}/split.bam --dont-use-soft-clipped-bases true -stand-call-conf 20.0 -O ${outputdir_GATK}/output.vcf #224min
echo $fq_1 GATK4 HaplotypeCaller exit code: $? >> $log_site

outputdir_annovar=${outputdir}/Annovar
if ! [ -d "$outputdir_annovar" ];then
    mkdir "$outputdir_annovar"
fi
cd $outputdir_annovar
perl $software_annovar_1 -format vcf4 ${outputdir_GATK}/output.vcf > ${outputdir_annovar}/vcf.avinput
echo $fq_1 annovar Start at: `date` >> $log_site
perl $software_annovar_2 ${outputdir_annovar}/vcf.avinput $software_annovar_db -buildver hg38 -out annovar -protocol refGene,knownGene,ensGene -operation g,g,g #5 min
echo $fq_1 annovar exit code: $? >> $log_site
