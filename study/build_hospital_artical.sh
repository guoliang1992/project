#!/bin/bash
#coding=gbk
.bin/tool.sh

function crawler() {
	local inout=$1; local output=$2;
	cd /search/odin/DataCenter/Crawler/
		python2.7 bin/crawer_xwhosp.py $input $output
	cd -
}


function parser() {
	local input=$1; local output=$2; local parseScript=$3;
	cd /search/odin/DataCenter/Parser/
		python $parseScript $input > $output
	cd -
}


function getArticalUrlList() {
	local input=$1; local output=$2
	awk -F'\t' '{print $1}' $input > $output
}


function main() {
	INFO"begin to crawler hospital artical list page ..."
	crawler $ArticalListUrl $ArticalListPage

	INFO "begin to parse hospital artical list page ..."
	parser $ArticalListPage $ArticalListResult $ArticalListParser

	INFO "begin to get hospital artic"
}

if [ $# -lt 1 ]; then
	INFO "[Usage]: sh $0 config"
	exit -1
fi

if [ ! -f $ $1 ]; then
	ERROR "config file [$1] is not exist!"
	exit -1
fi
source $1
 
main


