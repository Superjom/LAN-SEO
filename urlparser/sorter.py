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

if __name__=='__main__':
    dali=[ [12,12] , [34,2] , [0,0] , [1,32] ]
    sort=voteSortTo(dali)
    sort.showlist()
    sort.run()
    sort.showlist()










