# -*- coding:utf-8 -*-
import sys
import chardet
from urltest import Urltest
reload(sys)
sys.setdefaultencoding('utf-8')
#bug： urlvoter 中发现 很多url不标准 导致urlvoter中url缺失
#document中的url进行处理 统一转化为标准url
#此程序将会嵌入parser中 在生成document中使用
class UrlTrans:
    '传入url 转化为标准形式'
    def __init__(self,sortedUrlPh):
        '初始化urlid表 使用docID进行转化'
        #找到对应url
        self.urltest=Urltest()#链接的相关操作对象
        f=open(sortedUrlPh)
        c=f.readlines()
        f.close()
        self.urlID=[]
        for l in c:
            self.urlID.append(l.split()[1])

    def setTemHomeUrl(self,docID):
        '传入docID 取回url'
        #便于相对地址的转化
        self.temurl=self.urlID[int(docID)]

    def trans_d(self,url):
        #此处不对url检验
        item=url
        if item[0:4]=='\r\n':
            item=item[4:]
        if item[-1]=='/':
            item=item[:-1]
        if len(item)>=len('http://') and item[0:7]=='http://':
            return item
        if item[0:5]=='/java' or item[0:4]=='java':
            return False
        if item[0:3]=='../':
            item=self.urltest.absUrl(self.temurl,item)
        elif item[0] != '/':   
            item = '/' + item   
            item = self.temurl+ item   #使用局部home_url代替了homeurl
        elif item[:2]=='./':
            item=self.temurl+item[2:]
        return item

if __name__=='__main__':
    url=UrlTrans('../../store/sortedurls.txt')
    url.setTemHomeUrl(23)
    print url.trans_d('../hello.html')







