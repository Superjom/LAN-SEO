# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Urltest:
    def __init__(self):
        self.rightlist=('cn','com','php','asp','jsp','html','htm')

    def test(self,url):
        length=len(url)
        if url.find('///')>-1:
            return False
        if url.find('mailto:')>-1:
            return False

        for i in range(len(url)):
            index=length-i-1
            if url[index]=='.':
                break
            if url[index]=='/':
                return True 
        end=url[index+1:]
        #print end
        for li in self.rightlist:
            if li==end:
                return True
        return False
    
    def absUrl(self,homeurl,url):
        '对相对地址的处理 如果其首部包含类似../的地址 转为绝对地址'
        #计算homeurl的层次 url的层次
        #print homeurl
        #print url
        if homeurl[-1]!='/':
            homeurl+='/'
        level=[]
        length=len(homeurl)
        level2=0
        if homeurl.find('water///')>-1:
            return False
        for i in range(length):
            l=length-i#倒序
            if homeurl[l-1]=='/':
                level.append(l)
        for i in range(5):
            print url[level2*3 : (level2+1)*3]
            if url[level2*3 : (level2+1)*3]=='../':
                level2+=1
            else:
                break
        if level2>=len(level):
            #url不合法 出现 cau.edu.cn/   ../index.php
            return False
        baseurl=homeurl[0:level[level2]]
        #print baseurl
        apdurl=url[3*level2:]
        #print apdurl
        newurl=baseurl+apdurl
        newurl.replace('./','')
        return newurl

    def __backFind(self,home,s):
        '返回倒序查找的第一个s的位置'
        thome=home[::-1] #反向字符串
        i=thome.find(s)
        return len(home)-i-1

    def absDirUrl(self,url):
        '对绝对地址进行处理'
        #print 'now pas',url
        while url.find('/./')>-1:
            url=url.replace('/./','/')

        '''while url.find('../')>-1:
            ti=url.find('../')
            td=self.__backFind(url[:ti-1],'/')
            url=url[:td]+url[ti+2:]'''
        #print 'end url:',url
        return url

            

            

if __name__=='__main__':
    urlt=Urltest()
    for i in ['www.au.dd.cn','ww.c.cn/hsz','www.ca.ed.cn/ii.doc']:
        print i
        print urlt.test(i)
    print urlt.absUrl('www.cau.edu.cn/hsz/cau/redcross','../../index.php')
    print '绝对地址的情况'
    print urlt.absDirUrl('http://www.cau.edu.cn/hsz/../index.php')
    inl=raw_input('input a url:')
    while (inl!='0'):
        print urlt.absDirUrl(inl)
        inl=raw_input('input a url:')


                






            
