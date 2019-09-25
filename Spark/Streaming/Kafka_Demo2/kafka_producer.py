# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/24 下午8:19 
 @File    : kafka_producer.py
 @Note    : 


cd /Users/sunlu/Software/kafka_2.11-0.10.2.0/bin
 # 启动Kafka
./zookeeper-server-start.sh ../config/zookeeper.properties
./kafka-server-start.sh ../config/server.properties

# 创建topic
./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

# 查看topic
./kafka-topics.sh --list --zookeeper localhost:2181


# 消费消息
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning

# 消费spark生成的消息
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic ages --from-beginning




 参考链接：
kafka+spark streaming代码实例(pyspark+python)
 https://blog.csdn.net/chenyulancn/article/details/79420522
 """

from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import time


def main():
    ##生产模块
    producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'])
    with open("/Users/sunlu/Workspaces/PyCharm/PythonDiary/results/json.txt/part-00000-cebef46f-507a-49b9-9782-298f65654e12-c000.txt", 'r') as f:
        for line in f.readlines():
            time.sleep(1)
            producer.send("test", line)
            print
            line
            # producer.flush()


if __name__ == '__main__':
    main()