#coding=utf-8
from pyquery import PyQuery as pq
import xml.dom.minidom as dom
from sgmllib import SGMLParser  
from html import htmlctrl
import re
import sys

#是否有必要将爬虫和收集器集合起来，进行处理
#爬虫下载后，同时进行解析
class collector():
    #用于从原料库中提取并加工出document 加入知识库
    #知识库中将包含用xml进行封装的各种信息
    def __init__(self,html):
        self.html=html
        self.d=pq(html)
        self.d('script').remove()
        self.d('style').remove()
        reload(sys)
        sys.setdefaultencoding('utf-8')
       
        
    def clear_other_node(self):
        #print self.clearNode(self.body)
        self.d('head').remove()
        self.d('h1').remove()
        self.d('h2').remove()
        self.d('h3').remove()
        self.d('b').remove()
        self.d('a').remove()
    
    def a_trav(self,a):
        '将url转化为绝对url'
        item=a
        homepage='http://www.cau.edu.cn/lxy/'
        length=len(homepage)
        if item == None:   
            return 
        if item[0:4] == '\r\n':   
            item = item[4:]   
        if item[-1] == '/':   
            item = item[:-1]   
        elif item[0:5] == '/java' or item[0:4] == 'java':   
            pass  
        else:      
            if item[0] != '/':   
                item = '/' + item   
            item = homepage + item   
            return item    
        return item
    
    def pure(self):
        '返回纯文本 便于分词及词库生成'
        content=''
        content+=self.d('title').text()
        content+=self.d('a').text()
        content+=self.d('b').text()
        content+=self.d('body').text()
        return content

        

    def xml(self):
        str='<html></html>'
        titleText=self.d('title').text()
        self.dd=dom.parseString(str)
        #print self.dd
        html=self.dd.firstChild
        #生成title
        htmlCtrl=htmlctrl(self.d.html())
        title=self.dd.createElement('title')
        html.appendChild(title)
        title.setAttribute('text',titleText)
        #生成b
        bb=htmlCtrl.gNode('b')
        b=self.dd.createElement('b')
        for i in bb:
            ii=self.dd.createElement('item')
            ii.setAttribute('text',i)
            b.appendChild(ii)
        html.appendChild(b)
        #生成h1
        bb=htmlCtrl.gNode('h1')
        b=self.dd.createElement('h1')
        for i in bb:
            ii=self.dd.createElement('item')
            ii.setAttribute('text',i)
            b.appendChild(ii)
        html.appendChild(b)
        #生成h2
        bb=htmlCtrl.gNode('h2')
        b=self.dd.createElement('h2')
        for i in bb:
            ii=self.dd.createElement('item')
            ii.setAttribute('text',i)
            b.appendChild(ii)
        html.appendChild(b)
        #生成h3
        bb=htmlCtrl.gNode('h3')
        b=self.dd.createElement('h3')
        for i in bb:
            ii=self.dd.createElement('item')
            ii.setAttribute('text',i)
            b.appendChild(ii)
        html.appendChild(b)
        #生成a
        aa=htmlCtrl.gA()
        a=self.dd.createElement('a')
        for i in aa:
            aindex=self.dd.createElement('item')
            aindex.setAttribute('name',i)
            aindex.setAttribute('href',self.a_trav(aa[i]))
            a.appendChild(aindex)
        html.appendChild(a)
        #加入content
        htmltext=self.d.html().decode('gbk','ignore').encode('utf-8')
        ht=pq(htmltext)
        #bug 说明
        #此处  需啊注意 其中有html的特殊字符   &# 等等
        #在分词的时候另外说明
        content=ht.text()
        cc=self.dd.createElement('content')
        ctext=self.dd.createTextNode(content)
        cc.appendChild(ctext)
        html.appendChild(cc)
        
        #print self.dd.toprettyxml()
        return self.dd
        

if __name__=='__main__':
    c=collector('a')
    f=open('1.xml','w')
    document=c.xml().toxml()
    f.write(document)
