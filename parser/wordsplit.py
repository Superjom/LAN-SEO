#!/usr/bin/env python
#-*- coding:gb2312 -*-
import ictclas
import wordlist

def wordsplit(s):
    '返回一个由  分割开的自符'
    str=''
    #print s
    ictclas.import_dict('./user.txt')
    ictclas.ict_init("./")
    li = ictclas.process_str_ret_list(s)
    for i in li:
        #print i.start, i.length, i.word_id, s[i.start:(i.start+i.length)]
        # print s[i.start:(i.start+i.length)],hash(s[i.start:(i.start+i.length)]) 
        str=str+s[i.start:(i.start+i.length)]+' '
    ictclas.ict_exit()
    return str

def fsplit(path):
    f=open(path,'r')
    c=f.read()
    print c
    print wordsplit(c)
    f.close()

def filesplit(f,n,tag):
    ictclas.import_dict('./user.txt')
    ictclas.ict_init("./")
    li=ictclas.process_file(f,n,tag)

    ictclas.ict_exit()
   

if __name__=='__main__':
    '''f=open('html/s011')
    c=f.read()
    cc=c.encode('gb2312','ignore')
    print cc'''
    import sys
    reload(sys)
    sys.setdefaultencoding('gb2312')
    s='hello worldh你好,我来自中国农业大学'
    print wordsplit(s)



