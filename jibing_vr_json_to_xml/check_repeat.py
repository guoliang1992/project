#!/usr/bin/env python
#coding=gbk
#check url is weather repeat 
# if repeat print url disease_name other_name
import requests

video_url = dict()
for line in open("baikefinal.txt"):
	fields = line.split("\t")
	video_url[fields[0]] = 1
	
print len(video_url)
output = open("repeat_url","wa")
baseUrl = 'http://app.baikemy.com/disease/cs/31002333941249/'
for line in open("anthorName"):
	fields = line.split("\t")
	id = fields[2]
	othername = fields[1]
	
	realUrl = baseUrl + id
	data = requests.get(realUrl).json()
	
	vie_url = data['videoUrl']
	if vie_url in video_url:
		disease = data['diseaseName'].encode('gbk','ignore')
		line = vie_url.encode('gbk','ignore') +"\t"+disease+"\t"+ othername
		print line
