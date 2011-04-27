from pyquery import PyQuery as pq

f=open('ss')
c=f.read()
f.close()
root=pq(c)
title=root('title').eq(0)
print title.attr('text')
b=root('b item')
print b.eq(2).attr('text')
print 'the length is ',len(b)
b.eq(2).attr('text','chunwei is the best!')
print b.eq(2).attr('text')

