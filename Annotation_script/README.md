# {需要一个名字}的使用说明
---

## 软件说明

略。 输入*.fasta文件，输出结果。

## 环境依赖

* [python3]()

* [hisat2]()

* [samtools]()

## quick start

	cd /public/source/share/zcs
	python3 config.py -i config.txt -g hg38.gtf
	python3 config.py -i config.txt

## 使用说明

支持两种运行方式：

* 1、 config一体化运行

* 2、 分步输入参数运行


### config一体化运行

* 1、 更改配置文件(config.txt)内容。`##config of scripts`条目下所有选项必填，包括各个脚本的存放位置，依赖软件的调用路径，本次运行输入输出文件的路径，线程数，以及注释数据库路径。（`DB`首次创建后可重复使用）

* 2、首次运行需要先创建注释数据库（`DB`）。配置文件`DB`中填入生成路径，运行`python3 config.py -i config.txt -g gtf`，目前仅支持ENSEMBL标准格式gtf。

* 3、如已有注释数据库（`DB`），则可直接运行`python3 config.py -i config.txt`，软件可自动运行。


### 分步运行

软件计算分为6步

 - 1、长reads拆分(split_mapping.py)
 - 2、hisat2映射(hisat2)
 - 3、映射结果排序(samtools sort -n)
 - 4、映射结果组装(split_mapping2.py)
 - 5、组装结果注释(split_annotation.py)
 - 6、结合注释信息区分已知转录本、新转录本以及计算基因融合转录本。(annotation_cat.py)

每步脚本均有参数说明，可通过python script.py -h 查看

* 首次运行需要创建注释数据库（`DB`），运行`python3 split_annotation.py -d DB -g gtf`。

* `python3 split_mapping.py [parameter]`
	* -i [path] fasta
	* -o [path] split fasta
	* -l [int] splitted read length, default: 100
	* -v [int] splitted read overlap, default: 50
	* -m [int] min read length, default: 30

* hisat2映射

* `samtools sort -n `

* `python3 split_mapping2.py [parameter]`
	* -i [path] nsort.sam
	* -o [path] bed file
	* -l [int] splitted read length, default: 100
	* -v [int] splitted read overlap, default: 50
	* -p [int] process, default: 1 

* `python3 split_annotation.py [parameter]`
	* -i [path] bed file
	* -o [path] annotation file
	* -d [path] DB
	* -p [int] process, default: 1 
	* optional argument:
		* -g [path] gtf

* `python3 annotation_cat.py [parameter]`
	* -i [path] annotation file
	* -o [path] result file
	* -d [path] DB
	* -p [int] process, default: 1 