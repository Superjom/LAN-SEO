# -*- coding:utf-8 -*-
import sys
import chardet
reload(sys)
sys.setdefaultencoding('utf-8')
import urlsorter as url
if __name__=='__main__':
    url.InitUrlList() 
    f=open('config.txt')
    lines=f.readlines()
    f.close()
    for l in lines:
        tem=l.split()
        url.AddUrl(tem[0],tem[1])
    url.ShowList()
    url.QuickSort()
    url.ShowList()
    print url.GetUrlStr()

    url.DsyUrlList()



    

