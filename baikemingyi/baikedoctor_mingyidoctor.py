#!/usr/env/bin python
#coding:gbk
import requests
import re
def count(baseUrl):
	doctorDict = dict()
	for line in open('resourceid'):
		realUrl = baseUrl+str(line.rstrip("\n"))
		data = requests.get(realUrl).json()
	
		for items in data['expert']:
			for item in items:
				name = items['expertName']
				if name is None:
					continue
				url = items['expertUrl']
				hospital = items['lastFirstInstitutionName']
				
				if url is None:
					url = ""
				if hospital is None:
					hospital = ""

			doctorDict[name.encode('gbk','ignore')] =name.encode('gbk','ignore')+"\t"+ url.encode('gbk','ignore')+ "\t" + hospital.encode('gbk','ignore')
		
	return doctorDict

def get_selation_about_mingyi_and_jibing(mignyi_doctor_filename,doctor_name_dict):
	output = open("selation_about_mingyi_and_jibing",'wa')
	outnamein = open("not_match_but_name_in_doctorinfo",'wa')
	outnotin = open('not_match_and_name_notin_doctorinfo','wa')
	namedic = dict()
	namenotmatch = dict()
	namenotmatch2 = dict()
	for line in open(mingyi_doctor_filename):
		#79238452        http://www.haodf.com/doctor/DE4r0BC   于学忠  79202392        主任医师        3.7     东营市人民医院  骨外科  脊柱外科
		fields = line.split("\t")
		
		if fields[2] in doctor_name_dict:
			#依荷芭丽.迟     http://m.baikemy.com/expert/3575/index  中国医学科学院肿瘤医院
			jibindoctorfields = doctor_name_dict[fields[2]].split("\t")
			flag = jibindoctorfields[2] !=""  and re.match(jibindoctorfields[2],fields[6],re.U)
			flag2 = fields[6] !=""  and re.match(fields[6], jibindoctorfields[2], re.U)
			if flag  or flag2:
				line = doctor_name_dict[fields[2]] +"\t"+fields[2] + "\t" + fields[1] +"\t" + fields[6]
				output.write(line+"\n")
				
				if doctor_name_dict[fields[2]] in namenotmatch:
					del namenotmatch[doctor_name_dict[fields[2]]]

				del doctor_name_dict[fields[2]]
			else:
				line = doctor_name_dict[fields[2]]
				namenotmatch[line] = 1 
				namedic[fields[2]] = 1
	for key in doctor_name_dict:
		if key not in namedic:
			outnotin.write(doctor_name_dict[key]+"\n")
	for key in namenotmatch:
		outnamein.write(key+"\n")
#baseUrl = 'http://app.baikemy.com/disease/cs/31002333941249/'
#dict = count(baseUrl)
#print len(dict)
docnamedit = dict()
mingyi_doctor_filename = "extract_hospital_doctor_info_new"
for key in open("docname"):
	fields = key.split("\t")
	docnamedit[fields[0]] = key.rstrip("\n")

get_selation_about_mingyi_and_jibing(mingyi_doctor_filename,docnamedit)
