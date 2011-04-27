# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os

#初始条件:
# urllist文件格式：     每行类似于:    s01  http://www.cau.edu.cn
# 传入html文件的目录    urllist的文件
class DocTransId:
    '传入排序好的urlist文件 自动将html源码文件名称转为docid'
    def __init__(self,urlistpath,transpath):
        self.transpath=transpath #转换docid的文件目录
        f=open(urlistpath)
        lines=f.readlines()
        f.close()
        self.idlist=[]
        for ll in lines:
            l=ll.split()
            print l[0]
            self.idlist.append(l[0])
    
    def trans(self):
        for i,docname in enumerate(self.idlist):
            print 'path:',self.transpath+'/'+docname,self.transpath+'/'+str(i) 
            os.rename(self.transpath+'/'+docname,self.transpath+'/'+str(i))

if __name__=='__main__':
    doc=DocTransId('try1.txt','try')
    doc.trans()

