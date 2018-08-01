## USAGE

FACETS

1. 准备一个包含所有N\T样本的bam文件全路径列表，假定是list.txt，格式是一行两个bam先N后T空格分割。

2. python3 qsub.py输入list.txt生成shell脚本提交任务。得到*.facets文件。

3. *.facets放到一个文件夹下，假定是result_dir。

4. windows环境双击运行start.cmd(需要python3环境变量)，按提示输入result_dir，outputdir。

5. 完成，生成CNV.png。 