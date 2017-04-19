#!/usr/bin/env python
#coding:gbk

from kafka import KafkaConsumer
output = open('data/zhihu-freq',"wa")
consumer = KafkaConsumer('zhihu-freq',auto_offset_reset='earliest',enable_auto_commit=False,bootstrap_servers=['rsync.broker01.kafka02.sjs.ted:9092'])

counter = 0
for message in consumer:
	counter += 1
	if counter > 1000000:
		break
	str_val = message.value
	index_start = str_val.find("{")
	index_end = str_val.find("}")
	new_val = str_val[index_start : index_end + 1]
	output.write(new_val+"\n")
