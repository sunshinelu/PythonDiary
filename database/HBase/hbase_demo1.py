# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/23 下午5:04 
 @File    : hbase_demo1.py
 @Note    : 
 https://www.cnblogs.com/junle/p/7611540.html
https://blog.csdn.net/y472360651/article/details/79055875

 pip install thrift
pip install hbase-thrift
 """

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from hbase import Hbase
from hbase.ttypes import *

transport = TSocket.TSocket('192.168.37.21', 9090)

transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)

client = Hbase.Client(protocol)
transport.open()

contents = ColumnDescriptor(name='cf:', maxVersions=1)
# client.deleteTable('test')
client.createTable('test', [contents])

print(client.getTableNames())

# insert data
transport.open()

row = 'row-key1'

mutations = [Mutation(column="cf:a", value="1")]
client.mutateRow('t_sunl', row, mutations)

# get one row
tableName = 't_sunl'
rowKey = 'row-key1'

result = client.getRow(tableName, rowKey)
print(result)
for r in result:
    print('the row is ', r.row)
    print('the values is ', r.columns.get('cf:a').value)