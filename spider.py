# -*- coding: utf-8 -*-
#from sgmllib import SGMLParser  
import threading  
import time  
import urllib2  
import StringIO  
import gzip  
import string  
import os  
from parser.html import htmlctrl
from spider.urltest import Urltest
#from collector import collector
#rewrite SGMLParser for start_a  
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#           修改处
# 将spider and collecter 程序进行链接  去除原料库设置  直接转为 document 知识库
# 将url等直接写入知识库中
# 将取得url的方法改为 标准 pyquery方法
# 将 iframe的src也同时载入其中

#可能问题：
#       url规模过大 可能需要文件批量保存（在1万规模上） 研究url-list的文件保存和查找
#       废旧链接的去除

#提高url的质量：
#       1. 对cau的首页重复下载： 判断title，类似title只下载一次
#       2. 对包含#的url不予下载
#       3. 对iframe 及 frame的页面只能下载

#对广度有限爬虫的bug补充：
#   bug：
#       只能下载一级网页 如： cau.edu.cn/hongdou.html
#       在url中 如果出现如： cau.edu.cn/hsz/index.php 的情况
#       及多级url，将不能够继续下载子页面       
#   solve：
#       使用类似 list-find 的算法，动态加入参考home-url
#       在每个url在转化为绝对地址之后 判断其是否包含多级url 每一级url
#       不重复地保存到homeurl中

#对url绝对化的bug处理：
#   bug：
#       原来的url绝对化使用一个

##############################################

class Newlist(list):#这个类其实是一个添加了find方法的LIST。当num变量在LIST中，返回True,当不在LIST中，返回False并把num按二分法插入LIST中  
    def find(self, num):  
        #查找的时候，很小心的哦
        #查找时 默认查找带url而非ip  如果为ip开头  则自动将ip转为对应url
        #对不能解析的文件进行过滤：
        #如果末尾有.存在，且不为cn com org等  去除
        urltest=Urltest()
        if not urltest.test(num):
            return True 

        l = len(self)  
        first = 0  
        end = l - 1  
        mid = 0  
        if l == 0:  
            self.insert(0,num)  
            #print 'input ',num
            return False  
        while first < end:  
            mid = (first + end)/2  
            if num > self[mid]:  
                first = mid + 1  
            elif num < self[mid]:  
                end = mid - 1  
            else:  
                break  
        if first == end:  
            if self[first] > num:  
                self.insert(first, num) 
                #print 'input ',num 
                return False  
            elif self[first] < num:  
                self.insert(first + 1, num)  
                #print 'input ',num
                return False  
            else:  
                return True  
                
        elif first > end:  
            self.insert(first, num) 
            #print 'input ',num 
            return False  
        else:  
            return True  
#下面的reptile顾名思义是一个爬虫          
class reptile(threading.Thread):  
    #configfile: 是配置文件，存放网页的URL和下载下后的路径  
    #maxnum:     每个爬虫有个最大下载量，当下载了这么多网页后，爬虫dead  
    #需要解决一个问题：
    #校内许多的网站都是使用ip进行交互，需要解决url和ip的差异
    #工作方式：
    #   主程序给定一个队列，各个爬虫开始在此队列中进行查找，队列自动判断ip及域名的差异，采用ip和域名双判断
    
    #需要定义一个黑名单，对一些站点不要
    
    def __init__(self, Name, queue, list,result, Flcok, inittime = 0.00001, downloadway = './',configfile = 'D:\\bbs\\conf.txt', maxnum = 10000):  
        threading.Thread.__init__(self, name = Name )  
        self.queue = queue  
        self.result = result  
        self.Flcok = Flcok  
        self.inittime = inittime  
        self.mainway = downloadway  
        self.configfile = configfile  
        self.num = 0          #已下载的网页个数  
        self.maxnum = maxnum  
        self.way = downloadway + self.getName() + '\\'  
        self.list=list
        self.urltest=Urltest()#链接的相关操作对象
        #加入了主  home_url
        #
        self.home_list=[
                'http://www.cau.edu.cn',
                #'http://202.205.80.215',
                'http://org.wusetu.cn/hsz',
                #'http://202.205.91.91/hsz'
                #五色土开始
                #'http://wusetu.cn/logok.htm',
                'http://online.wusetu.cn',#社区论坛 无需要登录
                #'http://home.wusetu.cn',  #个人空间,需要登录 价值不大
                #'http://flash.wusetu.cn', #福来乐娱乐游戏 不许要登录
                #'http://vod.cau.edu.cn', #机网中心 影视剧场
                #'http://music.cau.edu.cn',#音乐
                #'http://v.cau.edu.cn',#校内在线 电影 校内浏览器
                #未爬PT

                        ]
        self.ip_list={
                #'http://202.205.80.215':'http://www.cau.edu.cn',
                'http://202.205.91.91':'http://org.wusetu.cn'
                }
        self.inqueue = queue#处理完后的URL的去处  有效queue
    def run(self):  
        opener = urllib2.build_opener()     #创建一个开启器  

        #通过urllib2.open的timeout 加入定时功能 对断链的等待时间

        while True:  
            print 'queue size:',self.queue.qsize()
            if self.queue.qsize()==0:
                print 'to break the while'
                break
            print 'start to get a queue'
            url = self.queue.get()          #从队列中取一个URL
            #print url
            if url == None:                 #当取得一个None后表示爬虫结束工作，用于外部方便控制爬虫的生命期  
                break
            print 'now:',self.name,url
            #parser = Basegeturls()          #创建一个网页分析器  
            request = urllib2.Request(url) #网页请求  
            request.add_header('Accept-encoding', 'gzip')#下载的方式是gzip压缩后的网页，gzip是大多数服务器支持的一种格式  

            #临时的url表 储存未经过处理的url 向下交给 trans_d 转化为局部home_url的url
            tem_url=[]
            try:                                      #这样可以减轻网络压力  
                page = opener.open(request,timeout=5)#发送请求报文  
                if page.code == 200:       #当请求成功  
                    predata = page.read() #下载gzip格式的网页  
                    pdata = StringIO.StringIO(predata)#下面6行是实现解压缩  
                    gzipper = gzip.GzipFile(fileobj = pdata)  
                    try:  
                        data = gzipper.read()  
                    except(IOError):  
                        print 'unused gzip'  
                        data = predata#当有的服务器不支持gzip格式，那么下载的就是网页本身  
                    try:  
                        #parser.feed(data)#分析网页  
                        print 'began to parse the html'
                        if len(data)<300:
                            continue
                        html=htmlctrl(data)
                    except:  
                        print 'I am here'#有的网页分析不了，如整个网页就是一个图片  
                    for item in html.gUrl():  
                        if item.find('#')<0:
                            #self.result.put(item)#分析后的URL放入队列中 不嫩听解析的url（文件）似乎也放不进去
                            tem_url.append(item)#将未处理的url加入到临时容器中
                            
                    
                     
                    self.num += 1 
                    self.way='store/html/'+self.getName()+str(self.num) 
                    #为了保证html后来的扩充性 重新决定保存为html源码
                    '''c=collector(data) 
                    #---------保存文件
                    #将使用   保存为document代替
                    file = open(self.way, 'w')  
                    file.write(c.xml().toxml()) #没有判断下载网页是否为空  到具体解析到时候再进行判断 
                    file.close()  '''
                    file=open(self.way,'w') #保存为短地址 如 s012
                    file.write(data)
                    file.close()
                    
                    #此处需要加入collector 提取相关信息
                    
                    #加入 总体 url表
                    self.Flcok.acquire()  
                    confile = open('store/config.txt', 'a')  
                    confile.write( self.getName()+str(self.num) + ' ' + url + '\n')  
                    confile.close()  
                    self.Flcok.release()  
                page.close()  
                if self.num >= self.maxnum:#达到最大量后退出  
                    break  
            except:  
                print 'end error'  

            #开始将新的raw_url 进行处理
            #包括 转化为 绝对地址  与局部home_url进行链接
            temHomeUrl=self.tem_home(url)
            self.trans_d(temHomeUrl,tem_url)
            if self.num>self.maxnum:
                for i in self.list:
                    print i
                break
                return True
                



    def trans_d(self,tem_url,rawurls):
        '将收获的url转化为 相对于局部主地址的绝对地址 并将其加入到inqueue中'
        urltest=Urltest() #对url的相关处理

        while True:
            if len(rawurls)>0:
                item=rawurls.pop()
            else:
                break
            if (item == None)or(len(item)<3):   
                break  
            if item[0:4] == '\r\n':   
                item = item[4:]   
            if item[-1] == '/':   
                item = item[:-1]   
            #ipurl
            #change url to direct url
            #already direct url
            if len(item) >= len('http://') and item[0:7] == 'http://':
                for homepage in self.home_list: 
                    #change wheather it is a subpage
                    length=len(homepage)
                    if len(item) >= length and item[0:length] == homepage:   
                        if self.list.find(item) == False:   
                            self.inqueue.put(item)   
                        break
                continue #return to while
            if item[0:5] == '/java' or item[0:4] == 'java':   
                pass
            else:
            #相对地址开始 tem_url为局部home_url
                #相对地址 #更新： 对于../进行退格处理
                if item[0:3]=='../':
                    item=self.urltest.absUrl(tem_url,item)
                elif item[0] != '/':   
                    item = '/' + item   
                    item = tem_url+ item   #使用局部home_url代替了homeurl
                elif item[:2]=='./':
                    item=tem_url+item[2:]
                #item=urltest.absDirUrl(item) #绝对地址再次进行处理
                if self.list.find(item) == False:   
                    self.inqueue.put(item) 
         

    def __backFind(self,home,s):
        thome=home[::-1] 
        i=thome.find(s)
        if i>-1:
            return len(home)-i-1
        else:
            return False

    def tem_home(self,url):
        #the situations:
        #hsz/index.php   can.edu.cn  cn/hsz   cn/hsz/
        #the most import thing is the last . and / pos
        askpos=self.__backFind(url,'?')
        if askpos:  #if ? exists
            url=url[:askpos]
        right_end=['cn','com','org']
        pos1=self.__backFind(url,'/') # pos of last /
        pos2=self.__backFind(url,'.') # pos of last .
        length=len(url)         #length of url
        #start to judge
        if pos1 and pos2:
            if pos1>pos2:
                #cn/hsz cn/hsz/
                print 'length is',length
                print 'pos1 is ',pos1
                if pos1==length-1:
                    return url[:-1]
                return url
            #cau.edu.cn   hsz.php
            end=url[pos2+1:]
            print 'ping: cau.edu.cn\n the end is:',end
            for i in right_end:
                if end==i: #like: cau.edu.cn
                    return url
            #like cau.edu.cn/index.php
            pos2=self.__backFind(url[:pos2],'/')
            return url[:pos2]



#和爬虫一样是个线程类,作用是将爬虫中的result中存入的URL加以处理。只要同一个服务器的网页  
#下面的是一个主函数过程  
#我下载的网站是http://bbs.hit.edu.cn  
#开始网页是http://bbs.hit.edu.cn/mainpage.php  
#FileName:test  

from Queue import Queue  
import threading  
import sys  
#num = int(raw_input('Enter the number of thread:'))  
#pnum = int(raw_input('Enter the number of download pages:'))
num=20
pnum=100
#mainpage = str(raw_input('The mainpage:'))  
#startpage = str(raw_input('Start page:'))  
mainpage='http://www.cau.edu.cn'
startpage='http://www.cau.edu.cn'
queue = Queue()  

key = Queue()  
inqueue = Queue()  
list = Newlist()  
thlist = []  
Flock = threading.RLock()  


for i in range(num):  
    th = reptile('s' + str(i), queue,list, key, Flock)  #创建进程  同时加入工作空间
    thlist.append(th)  
#pro = proinsight(key, list, mainpage, inqueue)  
#pro.start()  
for i in thlist:  
    i.start()  
queue.put(startpage)  
for i in range(pnum):  
    queue.put(inqueue.get())  
for i in range(num+10):  
    queue.put(None) 


