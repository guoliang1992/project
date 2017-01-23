#!/bin/bash
#coding=gbk
# 抓取医院的文章
# 1. 根据规律线下生成文章列表页的url文件
# 2. 抓取列表页html
# 3. 解析列表页html，得到详情页url列表
# 4. 抓取详情页html
# 5. 解析详情页html，得到 title  author  content(html块)

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








