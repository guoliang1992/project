#!/usr/env/bin python
#coding:gbk
import requests
class Counter:
	def __init__(self):
		self.url_Img_videoUrl_diseaseName=0
		
		self.base_name_counter=0
		self.base_name_counter_dict = dict()

		self.name_gaishu_isnull=0
		self.name_keshi_isnull=0
		self.name_zhengzhuang_isnull=0
		self.name_zhiliao_isnull=0
		self.name_dianxingzhengzhuang_isnull=0
		
		self.cure_all_isnull=0

		self.expert_all_isnull=0


	def json_to_xml(self,baseUrl,filename):
		for id in open(filename):
			realUrl = baseUrl+id.rstrip("\n")
			data = requests.get(realUrl).json()
			print data

	def count(self,baseUrl,id):
		realUrl = baseUrl+str(id)
		data = requests.get(realUrl).json()

		if data['videoImg'] is None and data['videoUrl'] is None  and data['url'] is None and data['diseaseName'] is None:
			self.url_Img_videoUrl_diseaseName += 1
		
		self.base_name_counter_dict[data['id']] = len(data['basic'])
		
		print '%s,%s' % (data['id'],len(data['expert']))
		
		for key in data['basic']:
			for item in key:
				if key['name'] == u'概述' and key['content'] is None:
					print item['content']
					self.name_gaishu_isnull += 1
				
				if key['name'] == u'科室' and key['content'] is None:
					self.name_keshi_isnull += 1
				if key['name'] == u'症状' and key['content'] is None:
					self.name_zhengzhuang_isnull += 1
				if key['name'] == u'治疗' and key['content'] is None:
					self.name_zhiliao_isnull += 1
		for key in data['symptom']:
			for item in key:
				if key['name'] == u'典型症状' and key['content'] is None:
					self.name_dianxingzhengzhuang_isnull += 1					
		
		print '%s,%s' % (data['id'],len(data['basic']))
		
		for key in data['cure']:
			flag = 0
			for item in key:
				if key[item] is not None:
					flag += 1
			
			if flag == 0:
				self.cure_all_isnull += 1


		for key in data['expert']:
			flag = 0
			for item in key:
				if key[item] is not None:
					flag += 1
			
			if flag == 0:
				self.expert_all_isnull += 1




baseUrl = 'http://app.baikemy.com/disease/cs/31002333941249/'
counter = Counter()
for line in open("resourceid"):
	counter.count(baseUrl,line.rstrip("\n"))

#print '%s,%s', % ('diseaseName and videoImg and videoUrl and url all is null',counter.url_Img_videoUrl_diseaseName)
#print '%s,%s', % ('basic/概述 is null',counter.name_gaishu_isnull)
#print '', % ('basic/科室：'counter.name_keshi_isnull
#print counter.name_zhengzhuang_isnull
#print counter.name_zhiliao_isnull
#print counter.name_dianxingzhengzhuang_isnull
#print counter.cure_all_isnull
#print counter.expert_all_isnull

#for id in counter.base_name_counter_dict:
#	print '%s,%s' % (id,counter.base_name_counter_dict[id])
