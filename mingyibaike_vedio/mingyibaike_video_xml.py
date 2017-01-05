#coding=gb2312

#����ҽ�ٿ���Ƶ׵�excel to xml
class tools:
	@staticmethod
	def isNone(obj):
		if obj:
			return obj.strip(' ').strip("\n")
		else:
			return ""

	def get_data(self,filename, mingyibaike_video_xml):
		output = open("mingyibaike_video.xml",'wa')
		counter = 0
		output.write('<?xml version="1.0" encoding="gbk"?>'+"\n")
		output.write('<DOCUMENT>')
#ר��΢url��link	 ��ƵPC��pclink	headline doctor	ְ��rank    ҽԺhospital   ���ڿ���dept	ר��ͷ���ַ	��Ƶ����summary	ʱ��duration	��Ƶ��ͼ��ַimg	  ������disease	#m.baikemy.com0    www.baikemy.com1	��ͷ��2	 �ٻ���3 ������ҽʦ4  ��ԷҽԺ5	   Ƥ����6  	http://pic.bai7"7   ҽ��Ϊ������8  03:26 9	    ic.baikemy.netjpg10 ��ͷ��11
		for line in open(filename):
			mingyibaike_xml = mingyibaike_video_xml
			mingyibaike_dic = dict()

			fields = line.rstrip("\n").split("\t")
			
			if len(fields) < 12:
				print fields[0] 
				counter += 1
				continue
			
			mingyibaike_dic['item_title'] = self.isNone(fields[2].rstrip("��"))+"_"+'ר����Ƶ_�ٿ���ҽ'
			mingyibaike_dic['pc_url'] = self.isNone(fields[1])
			mingyibaike_dic['video_title'] = self.isNone(fields[2])
			mingyibaike_dic['video_content'] = self.isNone(fields[8])
			
			phone_url = fields[0]
			mingyibaike_dic['phone_url'] = self.isNone(fields[0])
			video_id = phone_url[phone_url.rfind('/')+1 : len(phone_url)]
			mingyibaike_dic['video_id'] =  self.isNone(video_id)
			mingyibaike_dic['video_hot_word'] = self.isNone(fields[11].replace('|',';'))
			mingyibaike_dic['hospital_department'] = self.isNone(fields[6])
			mingyibaike_dic['doctor_name'] =  self.isNone(fields[3])
			mingyibaike_dic['doctor_title'] = self.isNone(fields[4])
			mingyibaike_dic['hospital_name'] = self.isNone(fields[5])
			mingyibaike_dic['video_img'] = self.isNone(fields[10])
			mingyibaike_dic['vedio_time'] = self.isNone(fields[9])
			
			#mingyibaike_dic['video_pv'] = ""
			#mingyibaike_dic['vedio_type'] = ""
			#mingyibaike_dic['disease_tag'] = ""
			#mingyibaike_dic['disease_body'] = ""
			#mingyibaike_dic['disease_label'] = ""
			#mingyibaike_dic['disease_longword'] = ""
			#mingyibaike_dic['disease_sub_label'] = ""
			#mingyibaike_dic['vedio_publish_time'] = ""

			for key in mingyibaike_dic:
				mingyibaike_xml = mingyibaike_xml.replace(key, mingyibaike_dic[key])

			output.write(mingyibaike_xml)

		output.write("</DOCUMENT>")
		print counter

mingyibaike_video_xml = '''
  <item>
    <key><![CDATA[video_id]]></key>
    <display>
      <title><![CDATA[item_title]]></title>
      <url><![CDATA[phone_url]]></url>
      <pcurl><![CDATA[pc_url]]></pcurl>
      <link><![CDATA[phone_url]]></link>
      <pclink><![CDATA[pc_url]]></pclink>
      <headline><![CDATA[video_title]]></headline>
      <summary><![CDATA[video_content]]></summary>
      <rank_default><![CDATA[video_id]]></rank_default>
      <disease><![CDATA[video_hot_word]]></disease>
      <dept><![CDATA[hospital_department]]></dept>
      <doctor><![CDATA[doctor_name]]></doctor>
      <rank><![CDATA[doctor_title]]></rank>
      <hospital><![CDATA[hospital_name]]></hospital>
      <img><![CDATA[video_img]]></img>
      <duration><![CDATA[vedio_time]]></duration>
    </display>
  </item>
'''

tool = tools()
filename = 'baikemingyi_video'
tool.get_data(filename, mingyibaike_video_xml)
