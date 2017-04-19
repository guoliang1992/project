#!/usr/bin/env python
#coding:gbk

from kafka import KafkaConsumer
output = open('data/weixin_article',"wa")
consumer = KafkaConsumer("weixin_article", auto_offset_reset='earliest', enable_auto_commit=False, bootstrap_servers=['rsync.node01.mystra.nm.ted:6667','rsync.node10.mystra.nm.ted:6667'])
for message in consumer:
	print message.value
	break
