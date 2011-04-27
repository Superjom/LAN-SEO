# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''
文档说明：
    pagerank的求值


'''
class PageRanker:
    def __init__(self,voteph):
	#初始化投票库
	self.votelist=[] #投票族
	f=open(voteph)
	lines=f.readlines()
	#开始解析
	for l in lines:
	    vote=[] #局部投票族
	    vote.append(l.split())#?????????可以直接压入片段吗?
	    self.votelist.append(vote)
    
    def calcualte(self):
	'计算一次'
	#最终结果对每个页面的PageRank值进行刷新

    def run(self):
	'循环计算 需要达到一定精度后才能停止'
