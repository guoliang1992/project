#!/usr/bin/env python
#coding=gbk
import requests
import os, sys, time,socket, urllib, urllib2, socket, gzip, StringIO, re
from bs4 import BeautifulSoup
#set default timeout
socket.setdefaulttimeout(30)



def crawer_page(original_url, retry = 3):
	time.sleep(1)
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
	new_page = page.decode('utf-8','ignore').encode('utf-8', 'ignore')
	artical_types_url = dict()
	pattern_list = pattern.split("@@@")
	try:
		pattern2 = re.compile(pattern_list[0], re.I)
		print pattern_list[0]
		artical_type_list = re.findall(pattern2, new_page)
		print len(artical_type_list)
		for artical_type_item in artical_type_list:
			if type(artical_type_item) == type(tuple()):
				artical_type_item = max(artical_type_item)	
			
			pattern3 = re.compile(pattern_list[1], re.I)
			type_items = re.findall(pattern3, artical_type_item+"</h2>")
			artical_type_name, artical_type_url = type_items[0][1],  pattern_list[len(pattern_list) - 1]+ type_items[0][0]
			artical_types_url[artical_type_url] = artical_type_name
				
	except Exception, e:
		print e
		pass
	return artical_types_url	


def process(infile_name, pattern):
	artical_types_url = dict()
	for line in open(infile_name):
		print line
		print '######################'
		url = line.strip("\n")
		raw_page = crawer_page(url)
		if raw_page == None:
			raw_page = ''
		raw_page = to_line(raw_page)
		artical_types_url.update(parse_url(raw_page, pattern))
	return artical_types_url

def to_line(page):
	return re.sub('[\r\n]', '\t\t\t', page)

def save_to_file(outfile_name, artical_types_url):
	outputStream = open(outfile_name, 'wa')
	for key in artical_types_url:
		outputStream.write(key.strip() + "\t" + artical_types_url[key].strip() + "\n")
if __name__ == '__main__':
	infile_name = sys.argv[1]
	outfile_name = sys.argv[2]
	pattern = sys.argv[3]
	artical_types_url = process(infile_name, pattern)
	
	save_to_file(outfile_name, artical_types_url)
