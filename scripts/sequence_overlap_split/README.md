## README

[sequence_overlap_split.py](https://github.com/captorr/ngs/blob/master/scripts/sequence_overlap_split/sequence_overlap_split.py)

将长序列切割为指定长度、指定overlap大小的短片段。



* -i 输入文件，txt格式，所有内容视为一条序列。

* -o [int] overlap区域大小

* -l [int] 切割后片段长度

* -s [left/right] 指定起始方向，左端或右端

* -t 输出互补序列

* -w 输出 “-互补-正常-互补-正常-” 交替的序列，第一个序列互补与否取决于-t参数

* -r 输出序列打印到屏幕上