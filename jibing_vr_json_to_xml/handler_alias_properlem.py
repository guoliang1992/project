#!/usr/bin/env python
#coding=gbk
import re
#handler not_match_but_name_in_doctorinfo data 

hospital_alias = dict()
hospital_name = dict()
hospital_title = dict()
hospital_urls = dict()

#http://www.haodf.com/hospital/DE4r0Fy0C9LuwWhaRujuSlReozGolC54J.htm     alias   南城市人民医院,南城市人民医院,
for item in open("haodf_hospital_names.names"):
	fields = item.rstrip("\n").split("\t")
	hospital_urls[fields[0]] = 1
	if fields[1] == 'title':
		hospital_title[fields[0]] = fields[2]
	if fields[1] == 'alias':
		hospital_alias[fields[0]] = fields[2].split(",")
	if fields[1] == 'name':
		hospital_name[fields[0]] = fields[2]

alias_name = dict()
for urlitem in hospital_urls:
	key = hospital_title[urlitem].strip('\n').strip(' ')
	other_key = hospital_name[urlitem].strip('\n').strip(' ')
	alias_list = hospital_alias[urlitem]
	if key == other_key:
		alias_name[key] = alias_list
	else:
		alias_name[key] = alias_list
		alias_name[other_key] = alias_list

doc_name = dict()
hospital_alias.clear()
hospital_alias.clear()
hospital_title.clear()
hospital_urls.clear()
#魏慎海  http://m.baikemy.com/expert/15319108647937/index        清华大学一附院
for line in open("not_match_but_name_in_doctorinfo"):
	fields = line.split("\t")
	doc_name[fields[0]] = line.rstrip("\n")

#79291057        http://www.haodf.com   齐宗华  79200387        主任医师        3.6     河南科技大学第一附属医院        外科    胸外科
output = open("outname",'wa')
names = dict()
doc_info = dict()
for line in open("extract_hospital_doctor_info_new"):
	fields = line.split("\t")
	doctor_name = fields[2]
	if doctor_name in doc_name :
		hospital_name = doc_name[doctor_name].split("\t")[2].split(" ")[0]
		
		if fields[6] in alias_name:
			if hospital_name in alias_name[fields[6]]:
				names[doctor_name] = 1
				print doc_name[doctor_name]+"\t"+fields[2]+"\t"+fields[1]+"\t"+fields[6]
				del doc_name[doctor_name]
			else:
				key = doc_name[doctor_name]+"\t"+fields[2]+"\t"+fields[1]+"\t"+fields[6];
				doc_info[key] = key
		else:
			key = doc_name[doctor_name]+"\t"+fields[2]+"\t"+fields[1]+"\t"+fields[6];
			doc_info[key] = key

for key in doc_info:
	doc_name = doc_info[key].split("\t")[0]
	if doc_name not in names:
		output.write(key+"\n")
 
	
