function mknamemap(){
		awk -F"\t" '$4~/医院:/&&$3~/\)$|）$/{
			if($2~/dianping/)
				next
			ori=$3
			gsub("（","(",$3)
			gsub("（","(",$3)
			gsub("）",")",$3)
			gsub("）",")",$3)
			len=split(substr($3,1,length($3)-1),lst,"(")
			if(len < 2)
				next
			a = lst[1]
			for(i=2;i<len;i++)
				a=a"("lst[i]
			b = lst[len]
			if(!(b~/部$|区$|店$/)&&length(b)>=5&&length(a)>=5)
				cat[ori"\t"a"\t"lst[len]]=1
		}END{
			for(i in cat)
				print i
		}' tmp/6tuple.norm.0 > conf/hospital.namemap
}


function namenorm(){
		awk -F"\t" 'BEGIN{OFS="\t"}
		function trim(str) {
			gsub(/(^[ 　]+|[  　]+$)/, "", str)
			gsub(/^(|\r||)+/, "", str)
			return str
		}
		{
			if(FILENAME~/.norm$/){
				if($5~/编辑整理/||$5=="无法复制"||$5=="不能复制"||$5=="复制不了"||$5=="复制不了文字"||$5=="")
					next
				# 过滤掉360医疗的交通攻略
				if ($2~/www.360jk.com/ && $4~/交通攻略/) {
					next
				}

				# 归一化多余空格，换行符
				$5 = trim($5)
				gsub(/|\r||/,"\\&#10;",$5);
				gsub(/[\t　 ]+/, " ", $5);
				gsub("(\\&#10;)+", "\\&#10;", $5);

				len=split($4,lst,":|_|@");
				if(len!=4 || lst[1]==""||lst[2]==""||lst[3]==""||lst[4]==""||$5==""){
					print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6 > "tmp/6tuple.norm.bad"
				}else{
					print $1"\t"trim($2)"\t"trim($3)"\t"trim($4)"\t"trim($5)"\t"$6;
				}
			}
		}' $1  > tmp/6tuple.norm.0

		mknamemap

		awk -F"\t" 'BEGIN{
				while(getline<"conf/namemap.black">0) {
					bl[$0]=1
				}
				while(getline<"conf/hospital.synname.suspect">0) {
					sus[$0]=1
				}
				while(getline<"conf/namemap/hospital.hdf.namemap.norm">0) {
					if($0 in bl)
						continue
					if($1 in sus || $2 in sus)
						continue
					gsub("#","",$1)
					cat[$2]=$1
				}
				}NR==FNR{
				cat[$1]=$2
				}NR>FNR{
				if($4~/医院:/){
					if($3 in cat)
						$3=cat[$3]
				}
				if($4~/科室:/){
					len=split($3,lst,"_")
					if(len==2&& lst[1] in cat)
						$3=cat[lst[1]]"_"lst[2]
				}
				if($4~/医院评价:/){
					len=split($3,lst,"_")
					if(len==3&& lst[1] in cat)
						$3=cat[lst[1]]"_"lst[2]"_"lst[3]
				}
				if($4~/医生:就职医院_content/||$4~/医院评价:医院名称_content/||$4~/科室:所属医院_content/){
					if($5 in cat)
						$5=cat[$5]
				}
				print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6
		}' conf/hospital.namemap tmp/6tuple.norm.0 > tmp/6tuple.norm.1

		# 归一化电话
		/usr/bin/python bin/norm-hospital-tel.py tmp/6tuple.norm.1 > tmp/6tuple.norm.1.1

		# url黑名单过滤
		awk -F"\t" 'ARGIND==1{
			cat[$1]=1
		}ARGIND>=2{
			if(!($2 in cat))
				print
		}' conf/url.bad tmp/6tuple.norm.1.1  > tmp/6tuple.norm.2

		
		# 属性/值 归一化
		awk -F"\t" 'ARGIND==1{
			cat[$1]=$2
		}
		ARGIND==2{
			dict[$1]=$2
		}
		ARGIND==3{
			if($4 in cat)
				$4=cat[$4]
			if($5 in dict)
				$5=dict[$5]
			split($4,lst,"@")
			if(lst[1] in cat)
				$4=cat[lst[1]]"@"lst[2]
			print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6
		}' conf/attr.map conf/attrval.map tmp/6tuple.norm.2 > $2

}
#mknamemap
#namenorm tmp/6tuple.norm.0 tmp/6tuple.norm

function normTel() {
		# 这是第一版归一化 电话的，已不再使用
		awk -F"\t" '{
		if($4~/医院:电话_content/){
			split($4,p,"@");
			split($5,t," |,|，|/");
			if(index(t[1],"（")!=0 ){
				if(index(t[1],":")!=0) be=index(t[1],":")+1;
				else if(index(t[1],"：")!=0) be=index(t[1],"：")+1;
				else be=1;
				tel=substr(t[1],be,index(t[1],"（")-1);
			}else if(index(t[1],"(")!=0){
				if(index(t[1],":")!=0) {
					if(index(t[1],":")<index(t[1],"("))
						be=index(t[1],":")+1;
				}
				else if(index(t[1],"：")!=0) {
					if(index(t[1],"：")<index(t[1],"("))
						be=index(t[1],"：")+1;
				}
				else be=1;
				tel=substr(t[1],be,index(t[1],"(")-1);
				}
			else{
				if(index(t[1],":")!=0) be=index(t[1],":")+1;
				else if(index(t[1],"：")!=0) be=index(t[1],"：")+1;
				else be=1;
				tel=substr(t[1],be);
			}
			split(tel,telnum,"转|或");
			gsub(")","-",telnum[1]);
			gsub("－","-",telnum[1]);
			if(length(telnum[1])>13){
				if(length(telnum[1])%2==0 && length(telnum[1])>=24){
					teln=substr(telnum[1],1,length(telnum[1])/2);
				}else{
					teln=substr(telnum[1],1,12);
				}
			}else{
				teln=telnum[1];
			}
			print $1"\t"$2"\t"$3"\t医院:电话_num@"p[2]"\t"teln"\t"$6;
			print $1"\t"$2"\t"$3"\t医院:电话_desc@"p[2]"\t"$5"\t"$6;
		}
			print
		}'tmp/6tuple.norm.1 > tmp/6tuple.norm.11
}

