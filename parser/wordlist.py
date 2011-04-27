#coding=gb2312
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')


class wordList(list):
#传入词汇  通过find方法  将word以hash正顺传入list中
#以二分法查找
#如果返回true  则可以通过此词汇的hash 查找word库中hit的相关信息
#作为list 可以被线程使用
#为了防止重复,加入了对重复单词的处理
#需要对hash表进行扩充 
#对于重复单词的解决方法： 可以加入后续表，在第一张表中重复的，可以在第二张表中使用同样的方法进行储存
#这些表最后是可以压缩在一块的
#对重复词汇的处理方式：
#利用二分法   当查询到start 或者 end 的hash值与 word相等时，将指针相应从前后进行移动，直到确定了最终边界。
#当首尾都确定了边界后，在结果中穷举查询
    def find(self,word):
        #print word
        l=len(self)
        first=0
        end=l-1
        mid=0
        num=hash(word)  #the word's hash
        if l==0:
            self.insert(0,word)
            return False
        while first<end:
            #while 的目的： 确定边界
            mid=(first+end)/2
            if num>hash(self[mid]):
                first=mid+1
            elif num<hash(self[mid]):
                end=mid-1
            else:
                #hash值相等
                #mid 的hash值相等
                #开始重新确定first和end
                first=mid
                end=mid
                while hash(self[first])==num and first>=0:
                    #向前扩展查找
                    if self[first]==word:
                        return True
                    first-=1

                while hash(self[end])==num and end<l:
                    #向后扩展茶渣
                    if self[end]==word:
                        return True 
                    end=end+1

                self.insert(mid+1,word)
                return False
            
        if first==end:
            if hash(self[first])>num:
                self.insert(first,word)
                return False
            elif hash(self[first])<num:
                self.insert(first+1,word)
                return False
            else:
                #hash值相等 但是也许word并不相等
                if self[first]==word:
                    #hash值相等 且词汇也相等
                    return True
                else:
                    #hash值相等 但是词不相等
                    # ?只存在此一个hash值？  如果 只需要插入新词
                    self.insert(first+1,word)
                    return False

        elif first>end:
            self.insert(first,word)
            return False
        else:
            return True

if __name__=='__main__':
    print 'begin to add world'
    word=wordList()
    print 'hello',hash('hello')
    print 'world',hash('world')
    print '你好',hash('你好')
    print 'he',hash('he')
    print 'wold',hash('wold')

    word.find('hello')
    word.find('world')
    word.find('你好')
    word.find('he')
    word.find('wold')
    print word
    while True:
        inword=raw_input('input>>')
        if inword=='000':
            break
        elif inword=='111':
            for i in word:
                print hash(i),i
        else:
            word.find(inword)
            print 'the word is here'
            print word
    print 'hello'
    print 'hello'
