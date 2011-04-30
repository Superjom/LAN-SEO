# -*- coding:utf-8 -*-
import sys
import chardet
reload(sys)
sys.setdefaultencoding('utf-8')

class Pageranker:
    'pagerank计算'
    #需要生成特定的表
    def __init__(self,votetoph,votefrph):
        #初始化votelist列表
        f=open(voteph)
        c=f.readlines()
        f.close()
        self.voteTo=[]
        self.voteFr=[]
        self.outnum={} #!!!!!!!!将来需要用数组优化  此处为数组
        for l in c:
            self.voteTo.append(l.split())
        f=open(votefrph)
        c=f.readlines()
        f.close()
        for l in c:
            self.voteFr.append(l.split())
        #page值
        self.ranks=[]
        initrank=float(1)/len(self.voteTo)
        #初始设为1/s
        for i in range(len(self.voteTo)):
            self.ranks.append(initrank)
        #初始化每个voter的outN
        self.initN()

    def run(self,num): #无法判断误差  直接使用循环数        
        '计算pagerank主程序 循环一定次数'
        index=0
        while index<num:
            self.percal()

    def percal(self):
        '一次计算'  
        #从to入手 遍历每一个记录
        last=0
        for i,vote in enumerate(self.voteTo):
            last=vote[1]#记录本次处理过的记录 防止重复
            v=[]
            v.append(vote[0])
            j=i+1
            #遍历产生投票数列
            while self.voteTo[j][1]==last:
                v.append(self.voteTo[j][0])
                j+=1
            #开始计算rank
            sumvote=0
            for vote in v:
                #计算其他网页投票的rank
                sumvote+=self.rank[vote]/self.outnum(vote)
            self.rank[last]=self.rank[last]+sumvote
        #rank总和恢复1
        ranksum=0
        for rank in self.rank:
            ranksum+=rank
        for rank in self.rank:
            rank=rank/ranksum
    
    def initN(self):
        '计算投票的page外出链接的数目'
        #与voteFr有关
        #考虑到顺次遍历 将生成初始表
        self.outnum={}
        for i,vote in enumerate(self.voteTo):
            last=vote[0] #from 记录本次投票方 防止重复
            outlinknum=1
            j=i+1
            while self.voteFr[j][0]==last:
                outlinknum+=1
                j+=1
            self.outnum.setdefault(last,outlinknum)  #!!!!!!!!此处将来需要用数组进行优化

    def save(self,ph):
        strr=''
        for rank in self.rank:
            strr+=str(rank)+' '
        f=open(ph,'w')
        f.write(strr)
        f.close()




                















