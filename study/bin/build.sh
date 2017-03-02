#!/bin/sh
. /etc/profile
. ~/.bash_profile

# 归一化
function normalize(){
. bin/namenorm.sh
namenorm "data/oridata/*" tmp/6tuple.norm
}

# 合并
function merge(){
. bin/mergedata.sh
mergedata tmp/6tuple.norm tmp/6tuple.id
}

# 推理
function inference(){
. bin/selector.sh
selector tmp/6tuple.id tmp/6tuple.sel
. bin/posinf.sh
posinf tmp/6tuple.sel tmp/6tuple.inf.pos
. bin/idinf.sh
idinf tmp/6tuple.inf.pos conf/hospital_fix_id_name.select tmp/6tuple.inf.id
. bin/cmtnuminf.sh
cmtnuminf tmp/6tuple.inf.id tmp/6tuple.inf.cmtnum
. bin/syninf.sh
syninf tmp/6tuple.inf.cmtnum tmp/6tuple.inf.syn
. bin/siteinf.sh
siteinf tmp/6tuple.inf.syn tmp/6tuple.inf.site

# 科室的擅长推导，使用了idinf步骤，输出的东西
if [ ! -f tmp/doctor.keshis -o ! -f tmp/doctor.goodat ]; then
	echo "before keshi_goodat_inf, error! "
	exit -1
fi
. bin/keshi_goodat_inf.sh 
keshi_goodat_inf tmp/6tuple.inf.site tmp/6tuple.inf

}


# 过滤
function filter() {
. bin/filter.sh
filter_non_biaozhu_hospitals tmp/6tuple.inf tmp/6tuple.filter
}


# 转json 上线
function json(){
. bin/idsort.sh
idsort tmp/6tuple.filter  tmp/6tuple.re.sort
cat tmp/6tuple.re.sort|php bin/6tuple2json.php 1>tmp/6tuple.all.json 2>json.1.err
scp tmp/6tuple.all.json root@10.134.24.44:/search/odin/yangtuo/mingyi/data/6tuple.all.json

# old verson, 没有拆分
php bin/selector.php tmp/6tuple.all.json 1>tmp/6tuple.sel.json 2>json.err
scp tmp/6tuple.sel.json root@10.134.24.44:/search/odin/yangtuo/mingyi/data/6tuple.sel.json

# 将医院与医生拆分
#php bin/selector.php tmp/6tuple.all.json 1>json.std 2>json.err
#scp tmp/6tuple.hospital.sel.json root@10.134.24.44:/search/odin/yangtuo/mingyi/data/
#scp tmp/6tuple.doctor.sel.json root@10.134.24.44:/search/odin/yangtuo/mingyi/data/


scp bin/selector.php root@10.134.24.44:/search/odin/yangtuo/mingyi/bin/

ssh 10.134.24.44 'cd /search/odin/yangtuo/mingyi; sh import_mingyi.sh'

}


# 从患者评论数据推导实际条数，所患疾病等，不用每次都执行，comment数据更新时执行一次即可
#python bin/pre_inf_doctor_comment.py > data/oridata/haodf_patient_comment_inf.norm


date

normalize
merge
inference
filter
json

date
