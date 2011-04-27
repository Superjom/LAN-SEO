# -*- coding: utf-8-*-
import re

def filter_char(strr):
    #英文字符区  
    re_mo=re.compile('[\$|\%|~|,|\.|\^|&|\(|\)|\*|@|#|:|!]')
    #中文字符区
    re_s=re.compile('】') #去除中文标点
 
    s=re_mo.sub('1111 ',strr)
    s=re_s.sub('1111 ',s)
    return s
   
def r_special_char(strr):
    re_s=re.compile('□')
    
    return re_s.sub('dd',strr)

if __name__=='__main__':
    from pyquery import PyQuery as pq
    from chardet import *
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #html=pq(url='http://www.cau.edu.cn')
    f=open('wordBar')
    c=f.read()
    #html=pq(c)
    #s=html('content').text()
    s=c
    ss=s.decode('utf-8')
    sss=ss
    sss=sss.encode('gb2312','ignore')
    sss=sss.decode('gb2312')
    
    #s=html('body').text()
    #s='教育改革 ► 盘点2010: 跨越发展新起步 ► “创先争优”专题网 ► 2010新生入学'
    #s='英文字符： hello ,,..你好啊,2011哈啊会 ，^&*()我还是听喜欢,中，这个。。►的各客大赛计算□。#$%!。。~'
    #print detect(s)
   

   
    tt=filter_char(sss)
    
    s=r_special_char(r_special_char(tt))
    print s
