# -*- coding:utf-8 -*-
import sys
import chardet
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from indexer import wordbar
from indexer import sorter


#为了便于测试和性能的保证
#将文件每100个保存到一个文件中 分开储存
#需要 在docID排序的基础上 再根据wordID进行排序
#在docID排序时，并不需要重新进行排序（只要保证docID已经排序便可)
#排序顺序必须为： docID > wordID

class Indexer:
    '索引器'
    #hits的结构  hitlist=[wordid,docid,score,pos]
    def __init__(self,docph,wbpath,topath):
        self.docph=docph    #分词xml所在文件夹
        self.topath=topath  #需要保存到的地址
        self.wbpath=wbpath  #词库地址
        self.hitlist=[]     
        self.each=100       #每一百个储存到一个文件中
        self.num=0          #直接处理的文件数目
        #权值 根据 id 从0开始排起  最终通过pagerank进行处理

        #开始初始化 词库
        self.wb=wordbar.Wordbar(self.wbpath)
        
    def run(self):
        '方法运行'
        findWI=self.findWordId
        li=os.listdir(self.docph)   #取得分词xml地址
        length=len(li)
        for doc in range(length):
            print doc
            #对每个文件进行处理
            #print self.docph+doc
            try:
                f=open(self.docph+'/'+str(doc))
                c=f.read()
                f.close()
            except:
                print 'no file',doc
                continue
            tags=c.split('@chunwei@')
            #print 'the tags is'
            #print tags
            abspos=0           #对于每个标签的增值
            for scoid,tag in enumerate(tags):
                #开始分别对每个标签进行处理
                words=tag.split() #取得每个词汇
                for pos,word in enumerate(words):
                    wid=findWI(word)
                    if wid: #保证只有词库中的词才能够被收录
                        self.hitlist.append([wid,doc,scoid,abspos+pos])

    def sortDoc(self):
        '对hit 根据docID进行排序'
        print 'sortDoc'
        #sort=sorter.hitDocSort(self.hitlist)
        #sort.run()

    def sortWid(self):
        '对hit 根据wordID进行排序'
        print 'wortWid'
        sort=sorter.hitWidSort(self.hitlist) #初始化
        sort.run()
        print 'succeed sorted wid'


    def __saveCHits(self):
        self.savehits(self.topath)

    def savehits(self,path):
        '保存hits'
        strr=''
        print 'length of hislist',len(self.hitlist)
        #print self.hitlist
        for i in self.hitlist:
            strr+=str(i[0])+' '+str(i[1])+' '+str(i[2])+' '+str(i[3])+'\n'
        f=open(path,'w')
        f.write(strr)
        f.close()

    def findWordId(self,word):
        '返回词汇的hash值'
        return self.wb.find(word)

if __name__=='__main__':
    index=Indexer('../store/wordsplit','../store/wordbar','../store/hits')
    index.run()

    #根据docID进行排序
    index.sortDoc()
    index.savehits('../store/sorteddochits')

    #根据wordID进行排序
    index.sortWid()
    index.savehits('../store/sortedwidhits')
    #index.savehits()
