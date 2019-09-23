# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/23 下午6:22 
 @File    : hbase_demo2.py
 @Note    : 

 https://blog.csdn.net/luanpeng825485697/article/details/81048468

 http://www.manongjc.com/article/44908.html
 https://github.com/626626cdllp/infrastructure/tree/master/hbase
 """

from thrift.transport import TSocket,TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase

# thrift默认端口是9090
socket = TSocket.TSocket("192.168.37.21",9090)
socket.setTimeout(500000)

transport = TTransport.TBufferedTransport(socket)
protocol = TBinaryProtocol.TBinaryProtocol(transport)

client = Hbase.Client(protocol)
socket.open()

print(client.getTableNames())
# print(client.get('t_student_sunlu','row1','info:name'))

"""
Traceback (most recent call last):
  File "/Users/sunlu/Workspaces/PyCharm/PythonDiary/database/HBase/hbase_demo2.py", line 29, in <module>
    print(client.getTableNames())
  File "/Users/sunlu/.pyenv/versions/3.6.2/lib/python3.6/site-packages/hbase/Hbase.py", line 738, in getTableNames
    return self.recv_getTableNames()
  File "/Users/sunlu/.pyenv/versions/3.6.2/lib/python3.6/site-packages/hbase/Hbase.py", line 748, in recv_getTableNames
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
  File "/Users/sunlu/.pyenv/versions/3.6.2/lib/python3.6/site-packages/thrift/protocol/TBinaryProtocol.py", line 134, in readMessageBegin
    sz = self.readI32()
  File "/Users/sunlu/.pyenv/versions/3.6.2/lib/python3.6/site-packages/thrift/protocol/TBinaryProtocol.py", line 217, in readI32
    buff = self.trans.readAll(4)
  File "/Users/sunlu/.pyenv/versions/3.6.2/lib/python3.6/site-packages/thrift/transport/TTransport.py", line 60, in readAll
    chunk = self.read(sz - have)
  File "/Users/sunlu/.pyenv/versions/3.6.2/lib/python3.6/site-packages/thrift/transport/TTransport.py", line 162, in read
    self.__rbuf = BufferIO(self.__trans.read(max(sz, self.__rbuf_size)))
  File "/Users/sunlu/.pyenv/versions/3.6.2/lib/python3.6/site-packages/thrift/transport/TSocket.py", line 132, in read
    message='TSocket read 0 bytes')
thrift.transport.TTransport.TTransportException: TSocket read 0 bytes
"""