#coding=gb2312
import requests
class tools:
	
	def __init__(self):
		self.video_url_map = dict()
		for line in open('output_video_url'):
			fields = line.rstrip("\n").split("\t")
			resource_url = fields[0][fields[0].rfind('=')+1:len(fields[0])]
			video_url_map[resource_url] = fields[1]
		
		self.mingyi_url = dict()
		for line in open('mingyiUrl'):
			fields = line.split("\t")
			doctor_name = fields[0]
			mingyi_url[doctor_name] = line.rstrip("\n")


	@staticmethod
	def  isNone(obj):
		if obj:
			return obj.strip().replace("\r\n","@@@")

		else:
			return ""
	def replace(self, obj):
		if obj:
			return video_url_map[obj]
	
	def replace_doctor_url(self, doctor_name, doctor_url):
		doctor_name_4_gbk = doctor_name.strip('\t').encode('gbk','ignore')
		if doctor_name_4_gbk in mingyi_url:
			fields = mingyi_url[doctor_name_4_gbk].strip().split("\t")
			if doctor_url == fields[1]:
				return  fields[2]

			elif (not doctor_url) and fields[2]:
				return fields[2]
		else:
			return doctor_url

	def replace_xml_val(self, key, xml_key, item_dict, hospitalXmlNode):
		if key in item_dict:
			hospitalXmlNode = hospitalXmlNode.replace(xml_key,item_dict[key])	
		else:
			hospitalXmlNode = hospitalXmlNode.replace(xml_key, "")
		return hospitalXmlNode

	def getjsondata(self,filename,hospitalXml,expert,zhiliao):
		anthor_name_dic = dict()
		baseUrl = 'http://app.baikemy.com/disease/cs/31002333941249/'
		output = open("finalxml","wa")
		output.write('<?xml version="1.0" encoding="utf-8"?>'+"\n")
		output.write('<DOCUMENT>')
 		for line in open(filename): 
			hospitalXmlNode = hospitalXml
			expertNode = expert
			zhiliaoNode = zhiliao
			fields = line.rstrip("\n").split("\t")

			id = fields[2]
			realUrl = baseUrl+id
			
			item_dict = dict()
		
			data = requests.get(realUrl).json()
			
			item_dict['diseasename'] = self.isNone(data['diseaseName'])
			
			item_dict['anthor_name'] = fields[1].replace('，',';').decode('gbk','ignore')
			item_dict['viderUrl'] = self.isNone(data['videoUrl'])
			item_dict['videoImg'] = self.replace(data['videoImg']) 
			item_dict['summaryUrl'] = self.isNone(data['url'])
			item_dict['summarykey'] = data['id']

			#basic
			for items in data['basic']:
				for item in items:
					name = items['name']
					if name == u'概述':
						item_dict['basic_namegaishu'] = self.isNone(items['content'])
					elif name == u'科室':
						item_dict['basic_name=keshi'] = self.isNone(items['content'])
					elif name == u'症状':
						item_dict['basic_name=zhengzhuang'] = self.isNone(items['content'])
					elif name == u'诊断':
						item_dict['basic_name=zenduan'] = self.isNone(items['content'])
					elif name == u'治疗':
						item_dict['basic_name=zhiliao'] = self.isNone(items['content'])
					elif name == u'治愈性':
						item_dict['basic_name=zhiyuxing'] = self.isNone(items['content'])
					elif name == u'流行病学':
						item_dict['basic_name=liuxingbingxue'] = self.isNone(items['content'])
					elif name == u'指导':
						item_dict['basic_name=zhidao'] = self.isNone(items['content'])
					elif name == u'高发人群':
						item_dict['gao_fa_ren_qun'] = self.isNone(items['content'])
					elif name == u'病因':
						item_dict['basic_bingyin'] = self.isNone(items['content'])
			#symptom
			for items in data['symptom']:
				for item in items:
					name = items['name']
					if name == u'典型症状':
						item_dict['symptom_name=dianxingzhenzhuang'] = self.isNone(items['content'])
				 	elif name == u'其他症状':
					 	item_dict['symptom_name=qitazhengzhuang'] = self.isNone(items['content'])
					elif name == u'并发症':
					 	item_dict['symptom_name=bing_fa_zheng'] = self.isNone(items['content'])

			#cure
			cure_list = data['cure']
			item_dict['cure'] = cure_list
			#expert
			expert_list = data['expert']
			item_dict['expert'] = expert_list
								 
			#get item_dict contain all item about xml and then splice xml
				#splice zhiliao
			zhiliaoitems = ""
			zhiliaorank_val = 1
			for cureitem in item_dict['cure']:
				if zhiliaorank_val > 3:
					break
				
				if cureitem['name'] and cureitem['content']:
					itemXml = zhiliaoNode.replace('zhi_liao_fang_zhen',self.isNone(cureitem['name']))
					itemXml = itemXml.replace('cure_name=zhiliaofangzhen',self.isNone(cureitem['content']))
					itemXml = itemXml.replace('zhiliaorank_val',str(zhiliaorank_val))
					zhiliaorank_val += 1
					zhiliaoitems += itemXml

			hospitalXmlNode = hospitalXmlNode.replace('zhiliao_item',zhiliaoitems)
			#key, xml_key, itemdic, hospitalXmlNode
			hospitalXmlNode = self.replace_xml_val('symptom_name=qitazhengzhuang', 'symptom_name=qitazhengzhuang', item_dict, hospitalXmlNode) 
			hospitalXmlNode = self.replace_xml_val('symptom_name=dianxingzhenzhuang', 'symptom_name=dianxingzhenzhuang', item_dict, hospitalXmlNode)
			hospitalXmlNode = self.replace_xml_val('symptom_name=bing_fa_zheng', 'symptom_name=bing_fa_zheng', item_dict, hospitalXmlNode)	
			
			
			expertNode_item = ""
			rank_val = 1
			for expert_item in item_dict['expert']:
				if rank_val > 3:
					break

				itemXml = expertNode.replace('expert_expertName',self.isNone(expert_item['expertName']))
				itemXml = itemXml.replace('expert_status',self.isNone(expert_item['status']))
				itemXml = itemXml.replace('expert_lastFirstInstitutionName',self.isNone(expert_item['lastFirstInstitutionName']))
				itemXml = itemXml.replace('expert_lastSecondInstitutionName',self.isNone(expert_item['lastSecondInstitutionName']))
				itemXml = itemXml.replace('expertposition',self.isNone(expert_item['position']))
				itemXml = itemXml.replace('expert_expertUrl',self.isNone(self.replace_doctor_url(expert_item['expertName'], expert_item['expertUrl'])))
				itemXml = itemXml.replace('rank_val',str(rank_val))
				rank_val += 1
				expertNode_item += itemXml

			hospitalXmlNode = hospitalXmlNode.replace('expert_item',expertNode_item)
			
			hospitalXmlNode = hospitalXmlNode.replace('diseasename',item_dict['diseasename'])
			hospitalXmlNode = hospitalXmlNode.replace('viderUrl',item_dict['viderUrl'])
			hospitalXmlNode = hospitalXmlNode.replace('video_Img',item_dict['videoImg'])
			hospitalXmlNode = hospitalXmlNode.replace('basic_namegaishu',item_dict['basic_namegaishu'])
			hospitalXmlNode = hospitalXmlNode.replace('basic_bingyin',item_dict['basic_bingyin'])
			hospitalXmlNode = hospitalXmlNode.replace('basic_name=keshi',item_dict['basic_name=keshi'])
			hospitalXmlNode = hospitalXmlNode.replace('basic_name=zhengzhuang',item_dict['basic_name=zhengzhuang'])
			hospitalXmlNode = hospitalXmlNode.replace('basic_name=zenduan',item_dict['basic_name=zenduan'])
			hospitalXmlNode = hospitalXmlNode.replace('basic_name=zhiliao',item_dict['basic_name=zhiliao'])
			hospitalXmlNode = self.replace_xml_val('basic_name=liuxingbingxue', 'basic_name=liuxingbingxue', item_dict, hospitalXmlNode)
			hospitalXmlNode = self.replace_xml_val('basic_name=zhidao', 'basic_name=zhidao', item_dict, hospitalXmlNode)
			hospitalXmlNode = hospitalXmlNode.replace('summaryUrl',item_dict['summaryUrl'])
			hospitalXmlNode = hospitalXmlNode.replace('summaryKey',str(item_dict['summarykey']))
			hospitalXmlNode = hospitalXmlNode.replace('anthorName',item_dict['anthor_name'])
			hospitalXmlNode = hospitalXmlNode.replace('defaultzhengzhuang',u'症状')
			hospitalXmlNode = hospitalXmlNode.replace('defaultzhiliao',u'治疗')
			
			hospitalXmlNode = self.replace_xml_val('gao_fa_ren_qun', 'gao_fa_ren_qun', item_dict, hospitalXmlNode)
			hospitalXmlNode = self.replace_xml_val('basic_name=zhiyuxing', 'basic_name=zhiyuxing', item_dict, hospitalXmlNode)
			print hospitalXmlNode.encode('utf-8','ignore')	
			output.write(hospitalXmlNode.encode('utf-8','ignore'))
		output.write('</DOCUMENT>')

hospitalXml = u'''
<item>
	<key><![CDATA[summaryKey]]></key>
	<display>
		<title><![CDATA[diseasename]]></title>
	  	<other_name><![CDATA[anthorName]]></other_name>
	  	<url><![CDATA[viderUrl]]></url>
	  	<videoImg_url><![CDATA[video_Img]]></videoImg_url>
	  	<summary><![CDATA[basic_namegaishu]]></summary>
		<summary_link><![CDATA[summaryUrl]]></summary_link>
		<basic>
	  		<department><![CDATA[basic_name=keshi]]></department>
			<symptom><![CDATA[basic_name=zhengzhuang]]></symptom>
			<symptom_keyword><![CDATA[]]></symptom_keyword>
			<diagnose><![CDATA[basic_name=zenduan]]></diagnose>
			<treatment><![CDATA[basic_name=zhiliao]]></treatment>
			<cure_rate><![CDATA[basic_name=zhiyuxing]]></cure_rate>
			<infect><![CDATA[]]></infect>
			<pathogeny><![CDATA[basic_bingyin]]></pathogeny>
			<rate><![CDATA[basic_name=liuxingbingxue]]></rate>
			<people><![CDATA[gao_fa_ren_qun]]></people>
			<inspection><![CDATA[]]></inspection>
			<price><![CDATA[]]></price>
		 </basic>
		 <special><![CDATA[basic_name=zhidao]]></special>
		<zhengzhuang>
			<classical_symptom><![CDATA[symptom_name=dianxingzhenzhuang]]></classical_symptom>
			<other_symptom><![CDATA[symptom_name=qitazhengzhuang]]></other_symptom>
			<complication><![CDATA[symptom_name=bing_fa_zheng]]></complication>
		</zhengzhuang>
		<zhiliao_more>
			zhiliao_item
	    </zhiliao_more>
		<tab2><![CDATA[defaultzhengzhuang]]></tab2>
		<tab3><![CDATA[defaultzhiliao]]></tab3>
		<experts>
			expert_item
		</experts>
	</display>
</item>
'''
expert = u'''
	     <expert>
		     <expert_name><![CDATA[expert_expertName]]></expert_name>
			 <expert_pic><![CDATA[]]></expert_pic>
			 <expert_title><![CDATA[expert_status]]></expert_title>
		     <expert_hospital><![CDATA[expert_lastFirstInstitutionName]]></expert_hospital>
		     <expert_dep><![CDATA[expert_lastSecondInstitutionName]]></expert_dep>
		     <expert_position><![CDATA[expertposition]]></expert_position>
		     <expert_link><![CDATA[expert_expertUrl]]></expert_link>
		     <expert_rank><![CDATA[rank_val]]></expert_rank>
		 </expert>
'''
zhiliao = u'''
		 <zhiliao>
			 <therapies_name><![CDATA[zhi_liao_fang_zhen]]></therapies_name>
			 <therapies_detail><![CDATA[cure_name=zhiliaofangzhen]]></therapies_detail>
	         <therapies_rank><![CDATA[zhiliaorank_val]]></therapies_rank>
	     </zhiliao>
'''
#http://img03.16&url=http://pic.baikemy.net/v/2016/bb984c41-b76b-44bf-9a86-0c32e89dafc6.jpg	http://img04.sogoucdn.com/app/a/10010016/c23f7c7ad0555f050ef6fce824b526d3

video_url_map = dict()
for line in open('output_video_url'):
	fields = line.rstrip("\n").split("\t")
	resource_url = fields[0][fields[0].rfind('=')+1:len(fields[0])]
	video_url_map[resource_url] = fields[1]

mingyi_url = dict()
for line in open('mingyiUrl'):
	fields = line.split("\t")
	doctor_name = fields[0]
	mingyi_url[doctor_name] = line.rstrip("\n")


tool = tools()
filename = "anthorName"
tool.getjsondata(filename,hospitalXml,expert,zhiliao)
