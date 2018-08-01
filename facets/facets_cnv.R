###########################################
##
##  Author: Zhang Chengsheng, 2018.06.12
##  args:[1]facets_file [2]sample_name [3]outputdir
##  tested in R v3.3.3
##
###########################################


args<-commandArgs(T)
## [1]facets_file [2]sample_name [3]outputdir
setwd(args[3])
file1=args[1]
sample_name=args[2]

library(facets)
set.seed(114)
xx=preProcSample(file=file1)
oo=procSample(xx,cval=150)
fit=emcncf(oo)
##fit2=emcncf2(oo)
png(paste(sample_name,'.png',sep=''),width=3000,height=2400,res=300)
plotSample(x=oo,emfit=fit)
dev.off()
##plotSample(x=oo,emfit=fit2)

table1=data.frame(start=fit$start,end=fit$end,fit$cncf,purity=fit$purity,ploidy=fit$ploidy)

write.table(table1,file=paste(sample_name,'.txt',sep=''),sep='\t',quote=F,row.names=F)

