#!/usr/bin/env python2.6
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from ICTCLAS50.Ictclas import Ictclas
from indexer.wordbar import Wordbar as wordbar
from query.initHashWid import InitHashWid
from query.initRankTotal import InitRankTotal
#浮点数计算
from decimal import *

class Hitlist(list):
    '查询中产生的查询结果列表'
    #计算每个docID的得分情况
    #初始的得分规则：
    #  命中1个词： + 20
    #  title+10 h1+5    h2+4    h3+3    b+3     content+1   a+1
    #基础算法：
    #   查询docID是否已经存在 如果不存在 则插入记录（排序）
    #   在查询过程中 将得分情况加入

    def find(self,hit):
        #传入标准hit  [wordID,docID,rank,pos]
        #返回记录格式 [docID,rank]
        docID=int(hit[1])
        score=int(self.score(hit)) #此次记录得分
        #print 'pre score',type(score)
        l=len(self)
        first=0
        end=l-1
        mid=0
        if l==0:
            self.insert(0,[docID,score] )
            return False
        while first<end:
            mid=(first+end)/2
            
            if docID>self[mid][0]:
                first=mid+1
            elif docID<self[mid][0]:
                end=mid-1
            else:
                break
        if first==end:
            if self[first][0]>docID:
                self.insert(first,[docID,score])
                return False
            elif self[first][0]<docID:
                self.insert(first+1,[docID,score])
                return False
            else:
                self[end][1]+=score
                return True
        elif first>end:
            self.insert(first,[docID,score])
            return False
        else:
            self[mid][1]+=score
            return True
    
    def score(self,hit):
        '计算加分'
        sco={
            0:50,   #title
            1:30,    #b
            2:50,    #h1
            3:40,    #h2
            4:30,    #h3
            5:3,    #a
            6:3     #content
        }
        score=hit[2]
        return int(sco[int(score)])



class Query:
    '查询库'
    def __init__(self,wbph,hitph):
        'init'
        self.ict=Ictclas('ICTCLAS50/') 
        self.hitph=hitph
        self.hitdoclist=Hitlist() #得分统计列表
        self.wordbar=wordbar('../store/wordbar') #词库 以便得到wordID
        #hithash相关
        self.hithasher=InitHashWid('../store/sortedwidhits','../store/hithash')
        self.hithasher.initHashWid()#初始化hithash
        #init rank total 单个doc的score总和
        self.ranktotal=InitRankTotal('../store/sorteddochits','../store/tranks')
        self.ranktotal.initTotalRank()

        self.hits=[]
        self.inithits()#初始化hits
        self.hithash=self.hithasher.hithash
        self.length=len(self.hits) #hits长度
        print 'length of hits is',self.length

    def inithits(self):
        f=open(self.hitph)
        lines=f.readlines()
        f.close()
        for l in lines:
            self.hits.append(l.split())

    def query(self,strr):
        '单个查询'
        words=self.wordsplit(strr) #分词后的查询结果
        print '分词结果为',words
        for word in words.split():
            #对每个word进行处理
            print '--start to query word--',word
            wordid=self.wordbar.find(word) #需要查询的wordID
            print '查得的wordID为',wordid
            if wordid:
                hithashpos=self.hithasher.find([wordid,0]) #hithasher返回的为目标数据在hithash中的位置
                if hithashpos:
                    starthitpos=int(self.hithash[hithashpos][1])
                    print '查得的hitpos为',starthitpos
                    #得到wordID在hits表中的片段地址 starthitpos  endhitpos
                    print '开始地址',starthitpos
                    if starthitpos+1<self.length:
                        endhitpos=int(self.hithash[hithashpos+1][1])-1
                    else:
                        endhitpos=starthitpos
                else:
                    continue
            else:
                continue
            #开始扫描片段 进行加分计算
            index=starthitpos
            print '结束地址',endhitpos
            while index<=endhitpos:
                #开始加分处理
                #print self.hits[index][0]
                self.hitdoclist.find(self.hits[index])
                index+=1

        print 'the former doclist---------------------------'
        for i in self.hitdoclist:
            print i

        #将score转化为相对score
        print '开始转为相对score'
        for i,score in enumerate(self.hitdoclist):
            #调整精度
            getcontext().prec = 8
            docid=score[0]
            rankpos=self.ranktotal.find([docid,0])#返回记录的位置
            ranktotal=self.ranktotal.tranks[rankpos][1]
            print 'rank',score[1],type(score[1])
            print 'the total rank',int(ranktotal)
            self.hitdoclist[i][1]=float(Decimal(score[1])/Decimal(int(ranktotal)))
        print 'start to print the hitdoclist'
        for i in self.hitdoclist:
            print i

        
    def wordsplit(self,sentence):
        '将查询语句分词'
        return self.ict.split(sentence)

if __name__=='__main__':
    query=Query('hello','../store/sortedwidhits')
    '''word=raw_input('query>>')
    while word != 'q':
        query.query(word)'''
    query.query('开放的中国农业大学欢迎您')

    #query.query('hello')
    

        
        

