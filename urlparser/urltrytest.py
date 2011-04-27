
ph='../store/config.txt'

maxlen=100

f=open(ph)
lines=f.readlines()
'''for l in lines:
    t=l.split()
    if len(t[1])>maxlen:
        print t[1]'''
res=''

for l in lines:
    t=l.split()
    s=t[0][11:]
    #print s
    res+=s+' '+t[1]+'\n'
f.close()
f=open(ph,'w')
f.write(res)
f.close()


