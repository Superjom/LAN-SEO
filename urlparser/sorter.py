# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class sorter:
    def __init__(self,datalist):
        self.dali=datalist

    def gvalue(self,data):
        return data[1]

    def run(self):
        self.quicksort(0,len(self.dali)-1)

    def quicksort(self,p,q):
        a=self.dali
        st=[]
        while True:
            while p<q:
                j=self.partition(a,p,q)
                if (j-p)<(q-j):
                    st.append(j+1)
                    st.append(q)
                    q=j-1
                else:
                    st.append(p)
                    st.append(j-1)
                    p=j+1
            if(len(st)==0):
                return
            q=st.pop()
            p=st.pop()

    def partition(self,a,low,high):
        gv=self.gvalue
        v=a[low]
        while low<high:
            while low<high and gv( a[high] ) >= gv( v ):
                high-=1
            a[low]=a[high]

            while low<high and gv( a[low] )<=gv( v ):
                low+=1
            a[high]=a[low]

        a[low]=v
        return low

    def showlist(self):
        for i in self.dali:
            print i

class voteSortTo(sorter):
    '对vote进行排序,通过to对比进行排序'
    def __init__(self,datalist):
        sorter.__init__(self,datalist)

    def gvalue(self,data):
        return int(data[1]) #因为docid为str 必须转化格式

class voteSortFr(sorter):
    '对vote进行排序,通过from对比进行排序'
    def __init__(self,datalist):
        sorter.__init__(self,datalist)

    def gvalue(self,data):
        return data[0]

class urlsorter(sorter):
    '根据url的hash值进行排序'
    def __init__(self,path,savepath):
        #格式类似于  [ [doc ,url] ]
        self.sp=savepath #保存的路将

        dlist=[]
        print 'the path is',path
        f=open(path)
        lines=f.readlines()
        f.close()
        print 'the lines is'
        for l in lines:
            print l
            dlist.append(l.split())
        sorter.__init__(self,dlist)

    def gvalue(self,data):
        print 'the data is',data
        return hash(data[1])

    def savelist(self):
        '保存排序后的结果'
        f=open(self.sp,'w')
        strr=''
        for i in self.dali:
            strr+=i[0]+' '+i[1]+'\n'
        f.write(strr)
        f.close()

if __name__=='__main__':
    dali=[ [12,12] , [34,2] , [0,0] , [1,32] ]
    sort=voteSortTo(dali)
    sort.showlist()
    sort.run()
    sort.showlist()










