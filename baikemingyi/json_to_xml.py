#!/usr/env/bin python

from json2xml.json2xml import Json2xml

def json_to_xml(baseUrl,filename):
	output = open("baike_data_xml","wa")
	output.write("<items>")
	for id in open(filename):
		realUrl = baseUrl+id.rstrip("\n")
	
		data = Json2xml.fromurl(realUrl).data
		data_object = Json2xml(data)
		output.write("<item>"+str(data_object.json2xml())+"</item>")


	output.write("</items>")


baseUrl = 'http://app.baikemy.com/disease/cs/31002333941249/'
json_to_xml(baseUrl,"soureid")
