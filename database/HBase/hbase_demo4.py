# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/23 下午9:04 
 @File    : hbase_demo4.py
 @Note    : 
 https://www.e-learn.cn/content/wangluowenzhang/2176263
 """

import happybase

CDH6_HBASE_THRIFT_VER='0.98'

hbase_cnxn = happybase.Connection(
    host="192.168.37.21", port=9090,
    table_prefix=None,
    compat=CDH6_HBASE_THRIFT_VER,
    table_prefix_separator=b'_',
    timeout=None,
    autoconnect=True,
    transport='framed',  # Default: 'buffered'  <---- Changed.
    protocol='compact'   # Default: 'binary'    <---- Changed.
)

print('tables:', hbase_cnxn.tables()) # Works. Output: [b'ns1:mytable', ]


"""
from thrift.protocol import TCompactProtocol             # Notice the import: TCompactProtocol [!]
from thrift.transport.TTransport import TFramedTransport # Notice the import: TFramedTransport [!]
from thrift.transport import TSocket
from hbase import Hbase
   # -- This hbase module is compiled using the thrift(1) command (version >= 0.10 [!])
   #    and a Hbase.thrift file (obtained from http://archive.apache.org/dist/hbase/
   # -- Also, your "pip freeze | grep '^thrift='" should show a version of >= 0.10 [!]
   #    if you want Python3 support.

(host,port) = ("192.168.37.21","9090")
transport = TFramedTransport(TSocket.TSocket(host, port))
protocol = TCompactProtocol.TCompactProtocol(transport)
client = Hbase.Client(protocol)

transport.open()

# Do stuff here ...
print(client.getTableNames()) # Works. Output: [b'ns1:mytable', ]

transport.close()

"""