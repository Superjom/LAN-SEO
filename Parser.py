#!/usr/bin/env python
#coding=utf-8
from pyquery import PyQuery as pq
from parser.wordlist import wordList as wordlist
import sys
import chardet
import re
from parser.collector import collector
from ICTCLAS50.Ictclas import Ictclas
import os
       
class parser:
    def __init__(self,htmlph,xmlph,wsplitph,wbpath):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.ict=Ictclas('ICTCLAS50/') 
        self.wordbar=wordlist()#wordBar
        self.spword='@chunwei@' #区分内容的关键字
        #设定相应路径
        self.htmlph=htmlph
        self.xmlph=xmlph
        self.wsplitph=wsplitph
        self.wbpath=wbpath

    def transDoc(self):
        '将html源码转化为document文件'
        htmlli=os.listdir(self.htmlph)#取得html路径
        num=0
        for hp in htmlli:
            print hp
            f=open(self.htmlph+'/'+hp)
            c=f.read()
            #自动判别编码 并进行转化
            res=chardet.detect(c)
            print res
            coding=res['encoding']
            #print 'the former coding',coding
            if coding!='utf-8':
                try:
                    c=c.decode(coding)
                except:
                    print 'something wrong'
            collec=collector(c)#开始解析
            f.close()
            f=open(self.xmlph+'/'+hp,'w')
            try:
                f.write(collec.xml(hp).toxml())#写入到新文件中
            except:
                print 'can not trans xml'
            f.close()
            num+=1


    def splitWord(self):
        '将document文件中的各项进行分词后 保存到新文件中'
        spword='@chunwei@'
        docli=os.listdir(self.xmlph+'/')
        num=0
        for dp in docli:
            print dp

            #if num>1:
            #    break
            #num+=1

            f=open(self.xmlph+'/'+dp)
            c=f.read()
            if len(c)<200:
                continue #对空文件忽略
            root=pq(c)#利用pyquery进行处理
            f.close()
            #开始对各栏目进行处理
            bb=''
            title=root('title').eq(0)
            bb+=self.ict.split( title.attr('text').encode('utf-8'))+' '
            bb+=spword
            #b的处理
            b=root('b item')
            length=len(b)
            for i in range(length):
                bb+=self.ict.split( b.eq(i).attr('text').encode('utf-8'))+' ' 
            bb+=spword
            #h1
            b=root('h1 item')
            length=len(b)
            for i in range(length):
                bb+=self.ict.split( b.eq(i).attr('text').encode('utf-8') )+' '    
            bb+=spword
            #h2
            b=root('h2 item')
            length=len(b)
            for i in range(length):
                bb+=self.ict.split( b.eq(i).attr('text').encode('utf-8') )+' '    
            bb+=spword
            #h3
            b=root('h3 item')
            length=len(b)
            for i in range(length):
                bb+=self.ict.split( b.eq(i).attr('text').encode('utf-8') ) +' '
            bb+=spword
            #a
            b=root('a item')
            length=len(b)
            for i in range(length):
                self.ict.split( b.eq(i).attr('name').encode('utf-8') )+' '
            bb+=spword
            #content
            content=root('content').eq(0)
            #print 'the content is '
            #print content.text()
            bb+=self.ict.split( content.text().encode('utf-8'))+' '
            #print 'the bb is'
            #print bb
            #save the result'''
            f=open(self.wsplitph+'/'+dp,'w+')
            f.write(bb)
            f.close()

    def __wordFind(self,strr):
        #print strr
        words=strr.split()
        flag=re.compile('\d')
        for i in words:
            if len(i)<=10:
                if i.find('=')>-1:
                    continue
                if i.find('.')>-1:
                    continue
                if flag.search(i):
                    continue
                self.wordbar.find(i)

    def transWbar(self):
        '将已经分词的wordxml 分词为 wordBar 并且进行储存'
        li=os.listdir(self.wsplitph)
        for xml in li:
            print xml
            #开始解析分词
            f=open(self.wsplitph+'/'+xml)
            c=f.read()
            f.close()   
            #开始将文本整合 最后对str进行分词
            for i in c.split(self.spword):
                self.__wordFind(i)
            #保存最后词库
        strr=''
        for i in self.wordbar:
            #以字符串的形式保存
            strr+=i+' '
        f=open(self.wbpath,'w')
        f.write(strr)
        f.close()

    def _debug(self):
        f=open(self.wbpath)
        c=f.read()
        for i in c.split():
            print i,hash(i)

if __name__=='__main__':
    p=parser('store/html','store/document','store/wordsplit','store/wordBar')
    #p.transDoc()
    #p.splitWord()
    #p.transWbar()
    p._debug()
