#!/usr/bin/env python2.6
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from SortFind import SortFind

class InitRankTotal(SortFind):
    '计算每个doc中标签得分总和 以便计算相对rank'
    def __init__(self,dochitph,tRankph):
        self.tRankph=tRankph #将要保存或初始化的rankTotal列表文件
        self.hits=[]
        self.tranks=[]
        #初始化hits
        f=open(dochitph)
        lines=f.readlines()
        f.close()
        for l in lines:
            self.hits.append(l.split())

    def gvalue(self,data):
        try:
            c=data[0]
        except:
            print 'something wrong',data,type(data)
        return int(data[0])

    def transTotalRank(self):
        '产生totalranks'
        length=len(self.hits) #hits长度
        #通过坐标点和宽度 逐步向后扫描
        lastpos=0
        lastwidth=0
        index=0 #遍历过程中 标志现在处理的hit

        while lastpos+lastwidth<length:
            startpos=lastpos+lastwidth
            lastwidth=0
            print 'now',self.hits[startpos][1]
            #需要保留lastpos及lastwidth值 同时对中间所有点进行扫描
            j=startpos
            startdot=self.hits[startpos][1] #新记录片段的开始点
            score=self.score(self.hits[j])
            self.tranks.append([startdot,score]) #加入docID记录

            while j<length and self.hits[j][1]==startdot:
                #开始处理
                score=self.score(self.hits[j])
                self.tranks[index][1]+=score #计算score总和 修改docID记录
                #索引值开始变化
                j+=1
                lastwidth+=1
            lastpos=startpos
            index+=1 

    def initTotalRank(self):
        '从文件初始化totalRank列表'
        print 'init totalRanks'
        f=open(self.tRankph)
        lines=f.readlines()
        f.close()
        for l in lines:
            self.tranks.append(l.split())
        SortFind.__init__(self,self.tranks)

    def show(self):
        for i in self.tranks:
            print i
    
    def save(self):
        print 'start to save'
        f=open(self.tRankph,'w')
        strr=''
        for tscore in self.tranks:
            strr+=str(tscore[0])+' '+str(tscore[1])+'\n'
        f.write(strr)
        f.close()

    def score(self,hit):
        '返回相应标签得分'
        sco={
            0:60,   #title
            1:30,    #b
            2:50,    #h1
            3:40,    #h2
            4:30,    #h3
            5:0,    #a
            6:3     #content
        }
        score=hit[2]
        return int(sco[int(score)])

if __name__=='__main__':
    trank=InitRankTotal('../../store/sorteddochits','../../store/tranks')
    trank.transTotalRank()
    trank.save()




        

