#!/usr/bin/env python
#coding=utf-8
import requests
import os, sys, time,socket, urllib, urllib2, socket, gzip, StringIO, re
from bs4 import BeautifulSoup
#set default timeout

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

def parse_url(page, artical_types_url, pattern_list):
	try:
		new_page = page.decode('gbk','ignore').encode('utf-8', 'ignore')
		artical_page_pattern = re.compile(pattern_list[0], re.S)
		artical_detail_page = re.findall(artical_page_pattern, new_page)
		if len(artical_detail_page) <= 0:
			pass	
		url_list_pattern = re.compile(pattern_list[1], re.I)
		artical_url_list = re.findall(url_list_pattern, artical_detail_page[0])
		for artical_url_item in artical_url_list:
			artical_url = artical_url_item[0]
			artical_title = artical_url_item[1]
			print '%s\t%s' % (artical_url, artical_title)
			artical_types_url[artical_url] = artical_title.decode('utf-8', 'ignore').encode('gbk')		

		page_next_pattern = re.compile(pattern_list[2], re.U)
		next_page_url = re.findall(page_next_pattern, new_page)
		if len(next_page_url) > 0:
			return  pattern_list[len(pattern_list) - 1] + next_page_url[0]
			#return  'http://www.shca.org.cn/' + next_page_url[0]
		else:
			return None

	except Exception, e:
		print e
		pass

def process(type_url, pattern_list):
	artical_types_url = dict()
	
	while type_url:
		print type_url
		pre_type_url = type_url
		raw_page = crawer_page(type_url)
		if raw_page == None:
			raw_page = ''
		raw_page = to_line(raw_page)

		type_url = parse_url(raw_page, artical_types_url, pattern_list)
		if type_url.strip() == pre_type_url.strip():
			return artical_types_url
	return artical_types_url


def to_line(page):
	return re.sub('[\r\n]', '\t\t\t', page)

def save_to_file(outfile_name, artical_dict, type_name, outputStream, pattern_list):
	outputStream.write(type_name+"\t"+"artical_type_name"+"\n")
	for key in artical_dict:
		new_key = pattern_list[len(pattern_list) - 1] + key	
		print '%s\t%s' % ('new_key', new_key)
		outputStream.write(new_key.strip() + "\t" + artical_dict[key].strip() + "\n")


if __name__ == '__main__':
	infile_name = sys.argv[1]
	outfile_name = sys.argv[2]
	pattern = sys.argv[3]
	pattern_list = pattern_list = pattern.split("@@@")
	outputStream = open(outfile_name, 'wa')
	for line in open(infile_name):
		type_url, type_name = line.strip("\n").split("\t")
		artical_dict = process(type_url, pattern_list)
		if len(artical_dict) == 0:
			artical_dict = process(type_url, pattern_list)

		save_to_file(outfile_name, artical_dict, type_name, outputStream, pattern_list)


