#coding=gbk
import os

class List(list):
    def __init__(self,path):
        '用于重复性儿分法的实验'
        self.path=path
        
    def find(self,urls):
        '查找 并且加入url'
        print urls
        url=urls[1]
        l=len(self)
        ll=hash(url)
        fir=0
        end=l-1

        if fir>end:
            #空
            self.insert(0,urls)
            return False
        elif fir<end:
            #not empty, need to compare
            while fir<=end:
                mid=(fir+end)/2
                if hash(self[fir][1])>ll:
                    self.insert(fir,urls)
                    return False
                if mid == l-1:
                    if hash(self[mid][1])>ll:
                        self.insert(mid,urls)
                        return False
                    elif hash(self[mid][1])<ll:
                        self.insert(mid+1,urls)
                        return False
                    else:
                        if self[mid][1]==url:
                            return True
                        else:
                            self.insert(mid+1,urls)
                            return False
                        
                if hash(self[mid][1])>ll:
                    end=mid-1
                elif hash(self[mid][1])<ll:
                    fir=mid+1
                else:
                    if url == self[mid][1]:
                        return True
                        break
                    else:
                        #length equals but url is different
                        fir=mid
                        end=mid
                        while fir>=0 and hash(self[fir][1])==ll:
                            if self[fir][1]==url:
                                return True
                                break
                            fir-=1
                        while end<l and hash(self[end][1])==ll:
                            if self[end][1]==url:
                                return True
                                break
                            end+=1
                        self.insert(mid+1,urls)
                        return False
            if hash(self[fir][1])>ll:
                self.insert(fir,urls)
                return False


        else:
            #self mid equal length of url
            if self[fir][1]==url:
                return True
            elif hash(self[fir][1])>ll:
                self.insert(fir,urls)
                return False
            else:
                self.insert(fir+1,urls)
                return False
    def get_str(self):
        s=''
        print len(self)
        for i in range(len(self)):
            s+=str(self[i][0])+' '
            s+=str(self[i][1])+'\n'
        return s

    def savelist(self):
        '将内存在中的urllist存储为文件'
        #urllist中数据为字典
        str=''
        for i in self:
            str+=i[0]+' '+i[1]+'\n'
        f=open('htmlconfig\urllist.txt','w+')
        f.write(str)
        f.close()



    def transDocId(self):
        '将文件修改未相应的docID'
        '需要依照list的顺序进行更改'
        '需要将list中的urllist进行储存'
        #读取urllist文件 
        f=open('config.txt')
        lines=f.readlines()
        doclist=[]
        for line in lines:
            li=line.split()
            doclist.append(li[0])
        #print doclist
        for i,name in enumerate(doclist):
            docname=doclist[i]
            print i,name
            print self.path+name
            try:
                os.rename(name,self.path+str(i))
            except:
                print 'no such file'

if __name__=='__main__':
    l=List('html/')
    '''print l.find((1,'1'))
    print l.find((2,'www.cau.edu.cn'))
    print l.find((3,'www.sohu.com'))
    while True:
        data=raw_input('...')
        if(data=='111'):
            print l
            for i in l:
                print hash(i[1]),i
        elif(data=='000'):
            break
        else:
            data=data.split()
            print l.find((data[0],data[1]))
            print l.get_str()'''
    l.transDocId()





