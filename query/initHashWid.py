#!/usr/bin/env python2.6
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from SortFind import SortFind

class InitHashWid(SortFind):
    '初始化hits的索引'
    #对hits进行处理 转化为hash结构的hits
    #对hits中wordID有查询功能
    def __init__(self,hitph,hashph):
        self.hitph=hitph
        self.hashph=hashph
        self.hithash=[] #hit的hash列表 [wordID,startpos]
        self.hits=[] #hits列表

    def gvalue(self,data):
        return int(data[0])
    
    def show(self):
        for i in self.wlist:
            print i

    def transHashWid(self):
        #初始化hits列表
        f=open(self.hitph)
        lines=f.readlines()
        f.close()
        for l in lines:
            self.hits.append(l.split())
        #开始进行索引化
        #hits 根据每个 wordID进行索引
        length=len(self.hits)
        lastpos=0
        lastwidth=0
        while lastpos+lastwidth<length:
            startpos=lastpos+lastwidth
            lastwidth=1
            self.hithash.append([self.hits[startpos][0],startpos]) #加入记录
            startdot=self.hits[startpos][0] #新记录的开始位置
            j=startpos+1
            while j<length and self.hits[j][0]==startdot:
                j+=1
                lastwidth+=1
            lastpos=startpos

    def initHashWid(self):
        '初始化hithash'
        f=open(self.hashph)
        lines=f.readlines()
        f.close()
        for l in lines:
            self.hithash.append(l.split())
        #print self.hithash
        SortFind.__init__(self,self.hithash)

    def save(self):
        print 'start to save'
        strr=''
        for i in self.hithash:
            strr+=str(i[0])+' '+str(i[1])+'\n'
        f=open(self.hashph,'w')
        f.write(strr)
        f.close()

if __name__=='__main__':
    hit=InitHashWid('../../store/sortedwidhits','../../store/hithash')
    hit.transHashWid()
    hit.save()
    #hit.initHashWid()
    #hit.show()
    print hit.find([34,0])

