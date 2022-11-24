library(ggplot2)
library(ggmap)
#library(sp)
#library(maptools)
#library(maps)
#library(ggpubr)

data <- read.delim('/Users/bingfengchen/Desktop/mps.txt', row.names = 1, sep = '\t', stringsAsFactors = FALSE, check.names = FALSE,na.strings="na")
#datas =read.table("suppressive map.txt",header = T, row.names = 1)
mp<-NULL #null map
mapworld<-borders("world",colour = NA,fill="gray80") #basic map
mp<-ggplot()+mapworld+ylim(-90,90)+theme(panel.background = element_rect(color = NA , fill = 'transparent'), legend.key = element_rect(fill = 'transparent'))
mp2<-mp+geom_point(aes(x=data$Longitude,y=data$Latitude,size=data$Abundance,color="black"),alpha=0.8)+scale_color_manual(values=c("#7EAECE","#1D4890","#ED9628","#9A2624","#F4B295","#157038"))+scale_size(range=c(1,10))
mp3<-mp2+theme(legend.position = "none")+xlab(NULL)+ylab(NULL)+theme(axis.ticks = element_blank(), axis.text.y = element_blank())+theme(axis.ticks = element_blank(), axis.text.x = element_blank())
mp3 
