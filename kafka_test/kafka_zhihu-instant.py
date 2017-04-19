#!/usr/bin/env python
# -*- coding: GBK-*- 
import json
from kafka import KafkaConsumer
output = open('data/zhihu-instant',"wa")
consumer = KafkaConsumer('zhihu-instant',auto_offset_reset='earliest',enable_auto_commit=False,bootstrap_servers=['rsync.broker01.kafka02.sjs.ted:9092'])
num=0
for message in consumer:
	val = message.value
	idx_start = val.find('{')
	idx_end = val.find('}') + 1
	js = val[idx_start : idx_end]
	num+=1
	if num >= 1000000:
		break
	output.write(js+"\n")
