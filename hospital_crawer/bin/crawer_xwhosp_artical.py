#!/usr/bin/env python
#coding=utf-8
import requests
import os, sys, time,socket, urllib, urllib2, socket, gzip, StringIO, re
from bs4 import BeautifulSoup

def crawer_page(original_url, retry = 3):
	time.sleep(1)
	print '%s,%s' % ('crawer_page', original_url)
	t = 0
	while t < retry:
		try:
			data = requests.get(original_url)
			return data.content
		except Exception, e:
			if hasattr(e, 'code') and e.code == 404:
				return ''
			t += 1
			time.sleep(0.5 * t)

	return ''

def parse_url(page, pattern):
	pattern_list = pattern.split("@@@")
	try:
		key = value = ""
		new_page = page.decode('gbk','ignore').encode('utf-8', 'ignore')
		artical_title_pattern = re.compile(pattern_list[0], re.S)
		artical_detail_page = re.findall(artical_title_pattern, new_page)
		if len(artical_detail_page) > 0:
			key = artical_detail_page[0]	
		
		artical_detail_pattern = re.compile(pattern_list[1], re.S)
		artical_detail = re.findall(artical_detail_pattern, new_page)
		if len(artical_detail) > 0:
			value =  pattern_list[len(pattern_list) - 2]+ artical_detail[0].decode('utf-8','ignore').encode('utf-8','ignore') + pattern_list[len(pattern_list) - 1]
			return key.strip() + "\t" + value
		
	except Exception, e:
		print e
		pass

def process(type_url):
	raw_page = crawer_page(type_url)
	
	if raw_page == None:
		raw_page = ''
	raw_page = to_line(raw_page)
	return raw_page 


def to_line(page):
	return re.sub('[\r\n]', '\t\t\t', page)

def save_to_file(artical_detail_url,artical_detail, outputStream):
	try:
		new_line ='\t'.join([artical_detail_url, artical_detail])
		outputStream.write(new_line+"\n")
	except:
		pass
	
if __name__ == '__main__':
	infile_name = sys.argv[1]
	outfile_name = sys.argv[2]
	pattern = sys.argv[3]

	outputStream = open(outfile_name, 'wa')
	
	for line in open(infile_name):
		artical_detail_url, artical_title = line.strip("\n").split("\t")
		artical_type_name = ""
		if artical_title == "artical_type_name":
			artical_type_name = artical_detail_url
			outputStream.write(artical_type_name+"\n")
			pass
		else:
			raw_page = process(artical_detail_url)
			artical_detail = parse_url(raw_page, pattern)
			save_to_file(artical_detail_url,artical_detail, outputStream)
