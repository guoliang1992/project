#!/usr/env/bin python
#coding:gbk
import requests

def count(baseUrl):
	for line in open("soureid"):
		realUrl = baseUrl+str(line.rstrip("\n"))
		data = requests.get(realUrl).json()
		print data['diseaseName'].encode('gbk','ignore')


baseUrl = 'http://app.baikemy.com/disease/cs/31002333941249/'
dict = count(baseUrl)

