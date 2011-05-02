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
from query.sorter import sorter

class Hitlist(list):
    def __init__(self):
        self.firvote=3 #首次命中加分的比率
        self.status=[]
        self.initStatus=[0,0,0,0,0,0,0,0] #初始化的状态

    '查询中产生的查询结果列表'
    #计算每个docID的得分情况
    #初始的得分规则：
    #  命中1个词： + 20
    #  title+10 h1+5    h2+4    h3+3    b+3     content+1   a+1
    #基础算法：
    #   查询docID是否已经存在 如果不存在 则插入记录（排序）
    #   在查询过程中 将得分情况加入

    #   为了充分保证关键字的全面性 对于每个关键子的第一一次hit
    #   进行双倍的加分
#   #   为此 将会在doclist中加入 一个标志符号   
#       更新排序算法  开始使用新的排序算法
#       使用各个标签分别全智的比率 最后控制各个标签的比率     动态控制各个标签在其中的比重
#       同时需要考虑 关键在的整合度     在每个标签中匹配关键字 对于首次出现的关键字  进行更大倍率的加分
#       !!!!!!!!!!!!!!!!!!!!!!!需要保证 status and self的记录一一对应

    def addStatus(self,hit):
        '添加一个标志为'
        initst=self.initStatus
        #更改标志位
        initst[int(hit[2])]=1
        self.status.append(initst)

    def find(self,hit):
        #传入标准hit  [wordID,docID,rank,pos]
        #返回记录格式 [docID,rank]
        #对于首次命中将会添加slef.firvote的倍率
        #为此添加了一个标志位
        #需要修改结构 同时需要注意关键字的首次配批
        #结构为：   [docID,title,b,h1,h2,h3,a,content]
        #添加标志位 [title,b,h1,h2,h3,a,content,total]

        docID=int(hit[1])
        scoIndex=int(hit[2])+1 #不同标签在self中的位置
        score=int(self.score(hit)) #此次记录得分
        #print 'the score is',hit,score
        l=len(self)
        first=0
        end=l-1
        mid=0

        if l==0:
            #添加记录
            self.insert(0,[docID,0,0,0,0,0,0,0] )
            #修改 首次加分
            self[-1][ scoIndex ]=self.firvote*score
            self.addStatus(hit)
            return False
        #产生位置索引
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

                #添加记录
                self.insert(first,[docID,0,0,0,0,0,0,0] )
                #修改 首次加分
                self[-1][scoIndex ]=self.firvote*score
                self.addStatus(hit)
                return False

            elif self[first][0]<docID:

                #添加记录
                self.insert(first+1,[docID,0,0,0,0,0,0,0] )
                #修改 首次加分
                self[-1][scoIndex]=self.firvote*score
                self.addStatus(hit)
                return False

            else:

                if self.status[end][ int(hit[2])]==0:
                    #记录已经存在
                    self[end][scoIndex]+=self.firvote*score
                else:
                    self[end][scoIndex]+=score
                return True

        elif first>end:

            #添加记录
            self.insert(first,[docID,0,0,0,0,0,0,0] )
            #修改 首次加分
            self[-1][ scoIndex ]=self.firvote*score
            self.addStatus(hit)
            return False

        else:

            if self.status[mid][ int(hit[2])]==0:
                self[mid][scoIndex ]+=self.firvote*score
            else:
                self[mid][scoIndex]+=score
            return True
    
    def score(self,hit):
        '计算加分'
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
    
    def InitStatus(self):
        '对其中每个doc的记录回原'
        for i,vote in enumerate(self):
            for j in range(7):
                self.status[i][j]=0

class Query:
    '查询库'
    def __init__(self,pageph,hitph):
        'init'
        self.ict=Ictclas('ICTCLAS50/') 
        self.hitph=hitph
        self.pageph=pageph
        self.hitdoclist=Hitlist() #得分统计列表
        self.wordbar=wordbar('../store/wordbar') #词库 以便得到wordID
        #hithash相关
        self.hithasher=InitHashWid('../store/sortedwidhits','../store/hithash')
        self.hithasher.initHashWid()#初始化hithash
        #init rank total 单个doc的score总和
        self.ranktotal=InitRankTotal('../store/sorteddochits','../store/tranks')
        self.ranktotal.initTotalRank()

        self.hits=[]
        #初始化pagerank
        self.pageranker=[]
        self.initPageranker()
        self.inithits()#初始化hits
        self.hithash=self.hithasher.hithash
        self.length=len(self.hits) #hits长度
        #print 'length of hits is',self.length
        #排序
        self.sorter=sorter()

    def initPageranker(self):
        print 'init pageranker'
        f=open(self.pageph)
        lines=f.readlines()
        f.close()
        for l in lines:
            self.pageranker.append(float(l))
        

    def inithits(self):
        f=open(self.hitph)
        lines=f.readlines()
        f.close()
        for l in lines:
            self.hits.append(l.split())

    def query(self,strr):
        '单个查询'
        words=self.wordsplit(strr) #分词后的查询结果
        #print '分词结果为',words
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
                self.hitdoclist.find(self.hits[index])
                index+=1

        #对结尾进行还原
        print '对结尾进行还原'
        self.hitdoclist.InitStatus()

        print 'the former doclist---------------------------'
        for i in self.hitdoclist:
            print i

        #将score转化为相对score
        #print '开始转为相对score'

        for i,score in enumerate(self.hitdoclist):

            #调整精度
            getcontext().prec = 6
            docid=score[0]
            rankpos=self.ranktotal.find([docid,0])#返回记录的位置
            perrank=0 #对于每个记录最终的page值综合

            for j,total in enumerate(self.ranktotal.tranks[rankpos]):
                #开始对每个总值进行扫描 将最终结果保存到 self.hitdoclist[i][-1]中

                if j>0:

                    ranktotal=self.ranktotal.tranks[rankpos][j]
                    
                    if int(ranktotal)==0:
                        self.hitdoclist[i][j]=0
                    else:
                        self.hitdoclist[i][j]=float(score[j])/float(ranktotal)

            #开始将每个标签的rank添加到总rank中
            #title:9 h1:3 h2:2 h3:2 b:1 a:0.5 content:0.5
            #开始加入pageranker
            print 'now calculate the pageranker with the result'
            print 'the docid is',self.hitdoclist[i][0]

            #self.hitdoclist[i][-1]= self.pageranker[ int(self.hitdoclist[i][0])]*(  self.hitdoclist[i][1]*0.5 + self.hitdoclist[i][2]*0.056+ self.hitdoclist[i][3]*0.167 +self.hitdoclist[i][4]*0.11 + self.hitdoclist[i][5]*0.11  +self.hitdoclist[i][6]*0.027 +self.hitdoclist[i][7]*0.027 )
            self.hitdoclist[i][-1]=self.hitdoclist[i][1]
            for k,summ in enumerate(self.hitdoclist[i]):
                if k>0:
                    self.hitdoclist[i][-1]+=summ

        print 'start to print the former hitdoclist'
        for i in self.hitdoclist:
            print i
        self.sorter.run(self.hitdoclist)
        print 'the result'
        self.sorter.showlist()
        #return self.getResList() #返回结果字符串 给服务器

    def wordsplit(self,sentence):
        '将查询语句分词'
        return self.ict.split(sentence)

    def getResList(self):
        strr=''
        for i in self.hitdoclist:
            strr+=str(i[0])+' '
        return strr

if __name__=='__main__':
    query=Query('../store/pageranker','../store/sortedwidhits')
    '''word=raw_input('query>>')
    while word != 'q':
        query.query(word)'''
    query.query('开放的中国农业大学欢迎您')

