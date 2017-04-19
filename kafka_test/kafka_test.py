#!/usr/bin/env python
#coding:gbk

from pykafka import KafkaClient
import logging

client = KafkaClient(hosts="rsync.broker01.kafka02.sjs.ted:9092,rsync.broker02.kafka02.sjs.ted:9092,rsync.broker03.kafka02.sjs.ted:9092,rsync.broker04.kafka02.sjs.ted:9092,rsync.broker05.kafka02.sjs.ted:9092,rsync.broker06.kafka02.sjs.ted:9092,rsync.broker07.kafka02.sjs.ted:9092,rsync.broker08.kafka02.sjs.ted:9092")
 
topic = client.topics['weixin_article']
  
balanced_consumer= topic.get_balanced_consumer(
consumer_group='guoliang_test_group',
auto_commit_enable=True,
#    reset_offset_on_start=True,
zookeeper_connect='rsync.jnode01.mystra.nm.ted:2181,rsync.jnode02.mystra.nm.ted:2181,rsync.jnode03.mystra.nm.ted:2181,rsync.jnode04.mystra.nm.ted:2181,rsync.jnode05.mystra.nm.ted:2181')
			   
for message in balanced_consumer:
	if message is not None:
		print message.offset, message.value
