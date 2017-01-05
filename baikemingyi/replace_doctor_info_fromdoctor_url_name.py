#!/usr/bin/env python
#coding:gbk

def getdoc_dic(filename):
	doc_dict = dict()
	for line in open(filename):
		fields = line.rstrip("\n").split("\t")
		doc_dict[fields[0]] = fields[1]
	return doc_dict

def replacename(filename2, docdic):
#80050071        http://www.haodf.com/docto       栾海飞  79203443        住院医师        3.5     南京医科大学第二附属医院        外科      普外科
	output = open("extract_hospital_doctor_info_new","wa")
	for line in open(filename2):

		fields = line.split("\t")
		if fields[1] in docdic:
			name = fields[2]
			newline = line.replace(name, docdic[fields[1]])
			output.write(newline)
		else:
			output.write(line)
	output.close()
		
	


filename = "extract_hospital_doctor_url_name"
#filename = 'test1'
docdic = getdoc_dic(filename)
filename2 = "extract_hospital_doctor_info"
#filename2 = 'test2'
replacename(filename2,docdic)
