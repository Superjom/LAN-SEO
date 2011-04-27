def tem_home(url):
    #   cau.edu.cn/hsz
    #   cau.edu.cn/index.php
    #   cau.edu.cn/hsz/
    #print ll
    index1=0
    index2=0 
    index_t=len(url) 
    #get the sub string before ?
    ll=len(url)
    for i in range(ll):
        index=ll-i-1
        if url[index]=='?':
            index_t=index
            break
    url=url[:index_t]
    #print 'sub the url to ',url
    ll=len(url)

    for i in range(ll):
        index=ll-i-1
        #print 'index',index
        if (url[index] == '.')and(index1==0):
            index1=index
        if (url[index] == '/')and(index2==0):
            index2=index
        if (index1!=0)and(index2!=0):
            break
    hometype=['cn','com','org']
    if index2==ll:
        return url
    elif index2>index1:
        return url[:-1]
    elif url[index1+1:] in hometype:
        return url
    else:
        return url[:index2]
if __name__=='__main__':
    inn=raw_input('input:')
    while inn!='0':
        print tem_home(inn)
        inn=raw_input('input:')

