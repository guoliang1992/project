#!/bin/bash
#coding=gbk
# ץȡҽԺ������
# 1. ���ݹ����������������б�ҳ��url�ļ�
# 2. ץȡ�б�ҳhtml
# 3. �����б�ҳhtml���õ�����ҳurl�б�
# 4. ץȡ����ҳhtml
# 5. ��������ҳhtml���õ� title  author  content(html��)

. bin/tool.sh

function crawler_base_hosp_url() {
	local input=$1; local output=$2;local pattern=$3;
	cd /search/odin/DataCenter/Crawler/
		python2.7 bin/crawer_xwhosp.py $input $output $pattern
	cd -
}

function crawler_artical_type_url() {
	local input=$1; local output=$2;local pattern=$3;
	cd	/search/odin/DataCenter/Crawler/ 
		python2.7 bin/crawer_xwhosp_type.py $input $output $pattern
	cd -
}

function get_artical_detail_list() {
	local input=$1; local output=$2;local pattern=$3
	cd /search/odin/DataCenter/Crawler/ 
		python2.7 bin/crawer_xwhosp_artical.py $input $output $pattern
	cd -
}


function main() {
	INFO "begin to crawl hospital article list page ..."
	#crawler_base_hosp_url $OriginalArticleUrlList $ArticleTypeUrlList $ArticleTypePattern	

	INFO"begin to crawler hospital article type page ..."
	#crawler_artical_type_url $ArticleTypeUrlList $ArticleUrlList $ArticalTypePattern

	INFO "begin to parse hospital article lisdt page ..."
	get_artical_detail_list $ArticleUrlList $ArticleDetailResult $ArticalDetailPattern

}



if [ $# -lt 1 ]; then
	INFO "[Usage]: sh $0 config"
	exit -1
fi
if [ ! -f $1 ]; then
	ERROR "config file [$1] is not exist!"
	exit -1
fi
source $1


main








