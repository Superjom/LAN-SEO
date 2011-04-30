#!/usr/bin/env python2.6
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from ICTCLAS50.Ictclas import Ictclas

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
        docID=hit[1]
        score=self.score(hit) #此次记录得分

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
            self.insert(first,docID)
            return False
        else:
            self[mid][1]+=score
            return True
    
    def score(self,hit):
        '计算加分'
        sco={
            0:10,   #title
            1:3,    #b
            2:5,    #h1
            3:4,    #h2
            4:3,    #h3
            5:1,    #a
            6:1     #content
        }
        score=hit[2]
        return sco[int(score)]



class Query:
    '查询库'
    def __init__(self,wbph,hitph):
        'init'
        self.ict=Ictclas('ICTCLAS50/') 

    def initHashHit(self,hitph):
        #初始化hits列表
        f=open(hitph)
        lines=f.readlines()
        f.close()
        self.hits=[]
        for l in lines:
            self.hits.append(l.split())
        #开始进行索引化
        #hits 根据每个 wordID进行索引
        length=len(self.hits)
        hashashed='-1'
        last=self.hits[0][0]#初始化 第一个wordID
        for i,hit in enumerate(self.hits):
            if hashashed==hit[0]:
                continue
            print 'wordID ...',hit[0]
            last=int(hit[0]) #下面开始进行遍历
            

        



    
    def wordsplit(self,sentence):
        '将查询语句分词'
        return self.ict.split(sentence)

if __name__=='__main__':
    query=Query('hello','ere')
    print query.wordsplit('你好中国')

        
        

