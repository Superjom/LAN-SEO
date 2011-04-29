#!/usr/bin/env python2.6
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from pyquery import PyQuery as pq
from urlparser import urlbar
from urlparser import sorter


#为了便于测试和性能的保证
#将文件每100个保存到一个文件中 分开储存

class Urlparser:
    'url的相关处理'
    def __init__(self,docph,urlbarph,stoph,sfph):
        self.urlbar=urlbar.urlbar(urlbarph) #urlbar实例
        self.docph=docph #docuemt文件地址
        self.stoph=stoph #按照to排序保存文件的地址
        self.sfph=sfph #按照from排序保存的文件地址
        self.votelist=[]

    def run(self):
        li=os.listdir(self.docph)
        for doc in li:
            print 'get a file:',doc
            f=open(self.docph+'/'+doc)
            c=f.read()
            f.close()
            if len(c)>100:
                root=pq(c)
                aa=root('a item')
                docid=0
                for a in range(len(aa)):
                    aindex=aa.eq(a).attr('href') #具体的url
                    docid=self.urlbar.find(aindex)
                    if docid:
                        self.__add(docid,doc)#添加记录到总list
        #开始对结果进行排序
        print 'start to sort by from'
        sorter.voteSortFr(self.votelist).run()
        self.__savelist(self.sfph)
        print '--ok--'
        print self.votelist
        print 'start to sort by to'
        sorter.voteSortTo(self.votelist).run() 
        self.__savelist(self.stoph)
        print '--ok--'




    def __add(self,f,t):
        '添加记录 f->t'
        self.votelist.append( [f,t] )

    def __glist(self):
        '将votelist转化为str'
        strr=''
        for vote in self.votelist:
            strr+=str(vote[0])+' '+str(vote[1])+'\n'
        return strr

    def __sortTo(self):
        '根据to进行排序'


    def __savelist(self,path):
        '将votelist保存到相应文件中'
        f=open(path,'w')
        f.write(self.__glist())
        f.close()

if __name__=='__main__':
    url=Urlparser('../store/document','../store/sortedurls.txt','../store/votetolist','../store/voteflist')
    url.run()


                

            
        

