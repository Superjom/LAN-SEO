#coding=gbk


'''
Created on 2011-3-12

@author: chunwei
'''

from pyquery import PyQuery as pq
import xml.dom.minidom as dom
from sgmllib import SGMLParser  

class htmlctrl():
    '''
    ��html����ز���
    '''
    def __init__(self,html):
        '''
        init
        '''
        self.html=html
        self.d=pq(html)
    
    def gA(self):
        a=self.d('a')
        aa={}
        for i in range(len(a)):
            aindex=a.eq(i)
            aa.setdefault(aindex.text(),aindex.attr('href'))
        return aa
    
    def gUrl(self):
        '�ܵ����е�url ����iframe�����src'
        a=self.d('a')
        aa=[]
        for i in range(len(a)):
            aindex=a.eq(i)
            href=aindex.attr('href')
            aa.append(href)
        frame=self.d('frame')
        for i in range(len(frame)):
            aindex=frame.eq(i)
            aa.append(aindex.attr('src'))
        return aa
        
    def gNode(self,node):
        '�õ����ձ��һά���� Ԫ�ص��ڵ�'
        b=self.d(node)
        bb=[]
        for i in range(len(b)):
            bb.append(b.eq(i).text())
        return bb
    
        

if __name__=='__main__':
    html=pq(url='http://www.cau.edu.cn')
    htmlc=htmlctrl(html.html())
    print htmlc.gUrl()
    
    
   
    
    
    
    
    
    
    
        
