# -*- coding:utf-8 -*-
import sys

import urlparser.sorter as urlsorter
from urlparser import  docTransId
import Parser

reload(sys)
sys.setdefaultencoding('utf-8')

#全局的运行程序
#除了爬虫以外
class Main:
    def __init__(self):
#-------------------------------常量定义----------------------------------------------------
        self.docdir='store/'  #数据目录基址
#-------------------------------url及html转化阶段-------------------------------------------
        #开始处理url 将doc转化为 docID
        #   将 store 目录中的 config.txt记录 url进行排序 将结果记录到 sortedurls.txt

        self.sorturl()

        #开始 将html源文件名称进行转化
        #   根据 sortedurls.txt 中的记录 将html中的html源文件更名为docId

        self.trans_doc_id()


#-------------------------------html处理阶段-----------------------------------------------
        #开始进行解析
        self.parse()

    def sorturl(self):
        'url排序 并且将结果储存'
        urlsort=urlsorter.urlsorter(self.docdir+'config.txt',self.docdir+'sortedurls.txt')
        urlsort.run()
        urlsort.savelist()
    
    def trans_doc_id(self):
        '将html源码文件改名称为docdir'
        doctid=docTransId.DocTransId(self.docdir+'sortedurls.txt',self.docdir+'html')
        doctid.trans()

    def parse(self):
        '解析 分词及 xml处理'
        pa=Parser.parser(self.docdir+'html',self.docdir+'document',self.docdir+'wordsplit',self.docdir+'wordbar')
        #处理为xml 文件文件
        pa.transDoc()
        #处理为xml分词文件
        pa.splitWord()
        #处理为词库
        pa.transWbar()

if __name__=='__main__':
    main=Main()
    print 'hello'





