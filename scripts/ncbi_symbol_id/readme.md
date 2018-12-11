### README

原本是根据基因列表查询基因曾用名的小教本

突然翻出来改了改，能修正列表中错误的基因名，输出正确基因名了。

---
python3 idt_porbe.py genelist.txt

搜索NCBI数据库中的基因曾用命，生成新的txt，内容为：

| gene symbol | input gene name | name used to be |

* 搜不到返回空值

* 现在可能不好使了

---

python3 idt_probe_new.py genelist.txt

在NCBI数据库中检查输入的基因名的最新symbol ID，生成txt：

|origin | real|
|------|---|
|输入的基因名 | 最新基因名|

* 搜不到也是返回空值

* 可能也不好使了

* 速度贼慢，居然还用urllib包

