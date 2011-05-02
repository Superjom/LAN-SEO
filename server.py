#!/usr/bin/env python2.6
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from twisted.internet import protocol, reactor
from time import ctime
from Query import Query
PORT = 21567

#查询库初始化
query=Query('hello','../store/sortedwidhits')
print 'succeed init query'

class TSServProtocol(protocol.Protocol):
    def connectionMade(self):
        clnt = self.clnt = self.transport.getPeer().host
        print '...connected from:', clnt
    def dataReceived(self, data):
        print data
        strr=query.query(data)
        print 'the res is',strr
        self.transport.write(strr)

factory = protocol.Factory()
factory.protocol = TSServProtocol
print 'waiting for connection...'
reactor.listenTCP(PORT, factory)
reactor.run()
