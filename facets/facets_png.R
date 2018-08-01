###########################################
##
##  Author: Zhang Chengsheng, 2018.06.14
##  args: [1]input_dir
##  tested in R v3.3.3
##
###########################################


args<-commandArgs(T)
library(ggplot2)
library(grid)

dir1=args[1]
setwd(dir1)

file1='R.ted'
data1=read.table(file1,header=F,sep='\t')

file2='R.chr'
data2=read.table(file2,sep='\t')
axis_x=data2[,2][2:length(data2[,1])]
names(axis_x)=paste('chr ',data2[,1][2:length(data2[,1])],sep='')
axis_x_minor=data2[,3]

col1=c('#003388','#003388','#EEEEEE','#EEEEEE','#DD5500','#DD5500','#660000','#660000')
p1=ggplot()+geom_tile(aes(x=data1[,1],y=as.factor(data1[,5]),fill=as.factor(data1[,4]),width=2*data1[,3],height=0.95))+scale_fill_manual(values=col1)
p2=p1+labs(x='',y='',fill='Total copy\nnumber')+scale_x_continuous(breaks=axis_x,label=names(axis_x),minor_breaks=axis_x_minor)
p3=p2+theme(axis.ticks=element_blank(),axis.text.y=element_text(margin=margin(r=-45,'pt')),axis.text.x=element_text(angle=45,size=rel(1.2),vjust=0.8,hjust=0.8),panel.ontop=T,panel.background=element_rect(fill=NA),panel.grid.major=element_blank(),panel.grid.minor=element_line(size=1.1,color='white'))

file3='R.ploidy'
data3=read.table(file3,sep='\t')

midpoint=(max(data3[,2])+min(data3[,2]))/2
pL=ggplot()+geom_tile(aes(x=1,y=as.factor(data3[,1]),fill=data3[,2],width=2,height=0.95))+labs(x='',y='',fill='Ploidy')+theme(axis.ticks=element_blank(),axis.text.y=element_blank())+scale_fill_gradient2(low='blue4',mid='green3',high='yellow',midpoint=midpoint)+scale_x_continuous(breaks=1,label='Ploidy')
pL1=pL+theme(axis.text.x=element_text(angle=45,size=rel(1.2),vjust=0.8,hjust=0.8),panel.background=element_rect(fill=NA),panel.grid=element_blank())

ple=ggplot()+geom_tile(aes(x=rep(0:7,times=length(data3[,1])),y=as.factor(rep(data3[,1],each=8)),fill=as.factor(rep(0:7,times=length(data3[,1]))),col=rep(data3[,2],times=8),height=1,width=1))+scale_color_gradient2(low='blue4',mid='green3',high='yellow',midpoint=midpoint)+scale_fill_manual(values=col1)
ple1=ple+theme(panel.ontop=T,panel.background=element_rect(fill='white'),axis.text=element_blank(),axis.ticks=element_blank())+labs(x='',y='',fill='Total copy\nnumber',color='Ploidy')
ple2=ple1+theme(legend.position=c(0.5,0.55),legend.key.size=unit(12,'pt'),legend.key.width=unit(20,'pt'),legend.key.height=unit(10,'pt'))


##grid.newpage()  
png('CNV.png',width=4000,height=1000,res=250)
pushViewport(viewport(layout = grid.layout(1,20)))
print(p3+guides(fill=FALSE)+theme(axis.text.x=element_text(size=rel(1.2)),axis.text.y=element_text(size=rel(1.3)),plot.margin=margin(l=10,r=0,t=10,b=10,'pt')),vp=viewport(layout.pos.row=1,layout.pos.col=1:19))
print(pL1+guides(fill=FALSE)+theme(axis.text.x=element_text(size=rel(1.2)),plot.margin=margin(l=-10,r=30,t=10,b=7,'pt')),vp=viewport(layout.pos.row=1,layout.pos.col=19:19))
print(ple2+theme(plot.margin=margin(l=10,r=40,t=10,b=7,'pt')),vp=viewport(layout.pos.row=1,layout.pos.col=20:20))
dev.off()

