def __backFind(home,s):
    thome=home[::-1] 
    i=thome.find(s)
    if i>-1:
        return len(home)-i-1
    else:
        return False

def tem_home(url):
    #the situations:
    #hsz/index.php   can.edu.cn  cn/hsz   cn/hsz/
    #the most import thing is the last . and / pos
    #control with .php?kidn=hello
    askpos=__backFind(url,'?')
    if askpos:  #if ? exists
        url=url[:askpos]

    right_end=['cn','com','org']
    pos1=__backFind(url,'/') # pos of last /
    pos2=__backFind(url,'.') # pos of last .
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
        pos2=__backFind(url[:pos2],'/')
        return url[:pos2]

if __name__=='__main__':
    urls=['http://www.cau.edu.cn/hsz','http://www.cau.edu.cn/hsz/index.php',\
          'http://www.cau.edu.cn','http://www.cau.edu.cn/',\
          'http://www.cau.edu.cn/hsz/',\
          'http://www.cau.edu.cn/hsz/index.php?kind=hello'\
          ]
    for url in urls:
        print 'former:',url
        print tem_home(url)

                



    
    
