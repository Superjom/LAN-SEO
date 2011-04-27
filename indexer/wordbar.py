# -*- coding:utf-8 -*-
import sys
import chardet
import SortFind as sortfind
reload(sys)
sys.setdefaultencoding('utf-8')

#重载了SortFind 方法

class Wordbar(sortfind.SortFind):
    '词库的相关操作'
    def __init__(self,wbph):
        '初始化词库'
        f=open(wbph)
        c=f.read()
        f.close()
        wb=c.split()
        sortfind.SortFind.__init__(self,wb)
    
    def gvalue(self,word):
        return hash(word)

    def showlist(self):
        for w in self.wlist:
            print hash(w),w


if __name__=='__main__':
    word=Wordbar('wordbar')
    word.showlist()
    wlist=['放假','像','哈哈','严','严肃','理学院']
    for w in wlist:
        print w,hash(w),word.find(w)





