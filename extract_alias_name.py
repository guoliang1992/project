#!/usr/bin/env python
#coding=gbk
import re

field_separator = '\t'
line_separator = '\n'

hospital_alias = dict()
hospital_name = dict()
hospital_title = dict()
hospital_urls = dict()

'''
http://www.haodf.com/hospital/DE4r0Fy0C9LuwWwnkFGdcuLPECdSRGpar.htm     name    江山市清湖镇卫生院
http://www.haodf.com/hospital/DE4r0Fy0C9LuwWwnkFGdcuLPECdSRGpar.htm     title   江山市清湖镇卫生院
http://www.haodf.com/hospital/DE4r0Fy0C9LuwWwnkFGdcuLPECdSRGpar.htm     alias   江山市清湖镇卫生院,江山市清湖镇卫生院,
'''

for item in open("haodf_hospital_names.names"):
	(hospital_url, type, val) = item.rstrip(line_separator).split(field_separator)
	hospital_urls[hospital_url] = 1

	if type == 'title':
		hospital_title[hospital_url] = val
	if type == 'alias':
		hospital_alias[hospital_url] = val.split(",")
	if type == 'name':
		hospital_name[hospital_url] = val

alias_name = dict()
for urlitem in hospital_urls:
	
	key = hospital_title[urlitem]
	other_key = hospital_name[urlitem]
	alias_list = hospital_alias[urlitem]
	
	if key == other_key:
		alias_name[key] = alias_list
	else:
		alias_name[key] = alias_list
		alias_name[other_key] = alias_list

hospital_alias.clear()
hospital_alias.clear()
hospital_title.clear()
hospital_urls.clear()

output = open("hospital_alias_name", "wa")
for key in alias_name:
	alias_name_str = ""
	
	for item in alias_name[key]:
		if item == "":
			continue
		alias_name_str += item +";"
	outname = [key, alias_name_str]
	
	print >> output ,(field_separator.join(outname))
