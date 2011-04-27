# -*- coding:utf-8 -*-
import sys
import chardet
reload(sys)
sys.setdefaultencoding('utf-8')

class Pageranker:
    'pagerank计算'
    def __init__(self,votetoph,votefrph):
        #初始化votelist列表
        f=open(voteph)
        c=f.readlines()
        f.close()
        self.voteTo=[]
        self.voteFr=[]
        for l in c:
            self.voteTo.append(l.split())
        f=open(votefrph)
        c=f.readlines()
        f.close()
        for l in c:
            self.voteFr.append(l.split())
        #page值
        self.ranks=[]






