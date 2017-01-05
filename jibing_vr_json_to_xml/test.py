#!/usr/bin/env python
name = dict()
for line in open("outname"):
	fields = line.split("\t")
	name[fields[0]] = line
for key in name:
	print key

