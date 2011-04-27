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
#           �޸Ĵ�
# ��spider and collecter �����������  ȥ��ԭ�Ͽ�����  ֱ��תΪ document ֪ʶ��
# ��url��ֱ��д��֪ʶ����
# ��ȡ��url�ķ�����Ϊ ��׼ pyquery����
# �� iframe��srcҲͬʱ��������

#�������⣺
#       url��ģ���� ������Ҫ�ļ��������棨��1���ģ�ϣ� �о�url-list���ļ�����Ͳ���
#       �Ͼ����ӵ�ȥ��

#���url��������
#       1. ��cau����ҳ�ظ����أ� �ж�title������titleֻ����һ��
#       2. �԰���#��url��������
#       3. ��iframe �� frame��ҳ��ֻ������

#�Թ�����������bug���䣺
#   bug��
#       ֻ������һ����ҳ �磺 cau.edu.cn/hongdou.html
#       ��url�� ��������磺 cau.edu.cn/hsz/index.php �����
#       ���༶url�������ܹ�����������ҳ��       
#   solve��
#       ʹ������ list-find ���㷨����̬����ο�home-url
#       ��ÿ��url��ת��Ϊ���Ե�ַ֮�� �ж����Ƿ�����༶url ÿһ��url
#       ���ظ��ر��浽homeurl��

#��url���Ի���bug����
#   bug��
#       ԭ����url���Ի�ʹ��һ��

##############################################

class Newlist(list):#�������ʵ��һ�������find������LIST����num������LIST�У�����True,������LIST�У�����False����num�����ַ�����LIST��  
    def find(self, num):  
        #���ҵ�ʱ�򣬺�С�ĵ�Ŷ
        #����ʱ Ĭ�ϲ��Ҵ�url����ip  ���Ϊip��ͷ  ���Զ���ipתΪ��Ӧurl
        #�Բ��ܽ������ļ����й��ˣ�
        #���ĩβ��.���ڣ��Ҳ�Ϊcn com org��  ȥ��
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
#�����reptile����˼����һ������          
class reptile(threading.Thread):  
    #configfile: �������ļ��������ҳ��URL�������º��·��  
    #maxnum:     ÿ�������и����������������������ô����ҳ������dead  
    #��Ҫ���һ�����⣺
    #У��������վ����ʹ��ip���н�������Ҫ���url��ip�Ĳ���
    #������ʽ��
    #   ���������һ�����У��������濪ʼ�ڴ˶����н��в��ң������Զ��ж�ip�������Ĳ��죬����ip������˫�ж�
    
    #��Ҫ����һ������������һЩվ�㲻Ҫ
    
    def __init__(self, Name, queue, list,result, Flcok, inittime = 0.00001, downloadway = './',configfile = 'D:\\bbs\\conf.txt', maxnum = 10000):  
        threading.Thread.__init__(self, name = Name )  
        self.queue = queue  
        self.result = result  
        self.Flcok = Flcok  
        self.inittime = inittime  
        self.mainway = downloadway  
        self.configfile = configfile  
        self.num = 0          #�����ص���ҳ����  
        self.maxnum = maxnum  
        self.way = downloadway + self.getName() + '\\'  
        self.list=list
        self.urltest=Urltest()#���ӵ���ز�������
        #��������  home_url
        #
        self.home_list=[
                'http://www.cau.edu.cn',
                #'http://202.205.80.215',
                'http://org.wusetu.cn/hsz',
                #'http://202.205.91.91/hsz'
                #��ɫ����ʼ
                #'http://wusetu.cn/logok.htm',
                'http://online.wusetu.cn',#������̳ ����Ҫ��¼
                #'http://home.wusetu.cn',  #���˿ռ�,��Ҫ��¼ ��ֵ����
                #'http://flash.wusetu.cn', #������������Ϸ ����Ҫ��¼
                #'http://vod.cau.edu.cn', #�������� Ӱ�Ӿ糡
                #'http://music.cau.edu.cn',#����
                #'http://v.cau.edu.cn',#У������ ��Ӱ У�������
                #δ��PT

                        ]
        self.ip_list={
                #'http://202.205.80.215':'http://www.cau.edu.cn',
                'http://202.205.91.91':'http://org.wusetu.cn'
                }
        self.inqueue = queue#��������URL��ȥ��  ��Чqueue
    def run(self):  
        opener = urllib2.build_opener()     #����һ��������  

        #ͨ��urllib2.open��timeout ���붨ʱ���� �Զ����ĵȴ�ʱ��

        while True:  
            print 'queue size:',self.queue.qsize()
            if self.queue.qsize()==0:
                print 'to break the while'
                break
            print 'start to get a queue'
            url = self.queue.get()          #�Ӷ�����ȡһ��URL
            #print url
            if url == None:                 #��ȡ��һ��None���ʾ������������������ⲿ������������������  
                break
            print 'now:',self.name,url
            #parser = Basegeturls()          #����һ����ҳ������  
            request = urllib2.Request(url) #��ҳ����  
            request.add_header('Accept-encoding', 'gzip')#���صķ�ʽ��gzipѹ�������ҳ��gzip�Ǵ����������֧�ֵ�һ�ָ�ʽ  

            #��ʱ��url�� ����δ���������url ���½��� trans_d ת��Ϊ�ֲ�home_url��url
            tem_url=[]
            try:                                      #�������Լ�������ѹ��  
                page = opener.open(request,timeout=5)#����������  
                if page.code == 200:       #������ɹ�  
                    predata = page.read() #����gzip��ʽ����ҳ  
                    pdata = StringIO.StringIO(predata)#����6����ʵ�ֽ�ѹ��  
                    gzipper = gzip.GzipFile(fileobj = pdata)  
                    try:  
                        data = gzipper.read()  
                    except(IOError):  
                        print 'unused gzip'  
                        data = predata#���еķ�������֧��gzip��ʽ����ô���صľ�����ҳ����  
                    try:  
                        #parser.feed(data)#������ҳ  
                        print 'began to parse the html'
                        if len(data)<300:
                            continue
                        html=htmlctrl(data)
                    except:  
                        print 'I am here'#�е���ҳ�������ˣ���������ҳ����һ��ͼƬ  
                    for item in html.gUrl():  
                        if item.find('#')<0:
                            #self.result.put(item)#�������URL��������� ������������url���ļ����ƺ�Ҳ�Ų���ȥ
                            tem_url.append(item)#��δ�����url���뵽��ʱ������
                            
                    
                     
                    self.num += 1 
                    self.way='store/html/'+self.getName()+str(self.num) 
                    #Ϊ�˱�֤html������������ ���¾�������ΪhtmlԴ��
                    '''c=collector(data) 
                    #---------�����ļ�
                    #��ʹ��   ����Ϊdocument����
                    file = open(self.way, 'w')  
                    file.write(c.xml().toxml()) #û���ж�������ҳ�Ƿ�Ϊ��  �����������ʱ���ٽ����ж� 
                    file.close()  '''
                    file=open(self.way,'w') #����Ϊ�̵�ַ �� s012
                    file.write(data)
                    file.close()
                    
                    #�˴���Ҫ����collector ��ȡ�����Ϣ
                    
                    #���� ���� url��
                    self.Flcok.acquire()  
                    confile = open('store/config.txt', 'a')  
                    confile.write( self.getName()+str(self.num) + ' ' + url + '\n')  
                    confile.close()  
                    self.Flcok.release()  
                page.close()  
                if self.num >= self.maxnum:#�ﵽ��������˳�  
                    break  
            except:  
                print 'end error'  

            #��ʼ���µ�raw_url ���д���
            #���� ת��Ϊ ���Ե�ַ  ��ֲ�home_url��������
            temHomeUrl=self.tem_home(url)
            self.trans_d(temHomeUrl,tem_url)
            if self.num>self.maxnum:
                for i in self.list:
                    print i
                break
                return True
                



    def trans_d(self,tem_url,rawurls):
        '���ջ��urlת��Ϊ ����ھֲ�����ַ�ľ��Ե�ַ ��������뵽inqueue��'
        urltest=Urltest() #��url����ش���

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
            #��Ե�ַ��ʼ tem_urlΪ�ֲ�home_url
                #��Ե�ַ #���£� ����../�����˸���
                if item[0:3]=='../':
                    item=self.urltest.absUrl(tem_url,item)
                elif item[0] != '/':   
                    item = '/' + item   
                    item = tem_url+ item   #ʹ�þֲ�home_url������homeurl
                elif item[:2]=='./':
                    item=tem_url+item[2:]
                #item=urltest.absDirUrl(item) #���Ե�ַ�ٴν��д���
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



#������һ���Ǹ��߳���,�����ǽ������е�result�д����URL���Դ���ֻҪͬһ������������ҳ  
#�������һ������������  
#�����ص���վ��http://bbs.hit.edu.cn  
#��ʼ��ҳ��http://bbs.hit.edu.cn/mainpage.php  
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
    th = reptile('s' + str(i), queue,list, key, Flock)  #��������  ͬʱ���빤���ռ�
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


