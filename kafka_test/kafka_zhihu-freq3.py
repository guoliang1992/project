#!/usr/bin/env python
#coding:gbk

from kafka import KafkaConsumer
output = open('data/zhihu-freq3',"wa")
consumer = KafkaConsumer('zhihu-freq3',auto_offset_reset='earliest',enable_auto_commit=False,bootstrap_servers=['rsync.broker01.kafka02.sjs.ted:9092'])
counter = 0
for message in consumer:
	counter += 1
	if counter >= 1000000:
		break
	index_start = message.value.find('{')
	index_end = message.value.find("}")
	new_val = message.value[index_start:index_end+1]
	output.write(new_val+"\n")

