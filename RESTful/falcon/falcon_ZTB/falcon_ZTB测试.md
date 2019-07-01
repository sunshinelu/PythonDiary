测试用例
1. 项目类型区域分布
在collect_ccgp表中根据区域招投标情况（分区域），分析本区域信息化建设情况, 把ID、区域(provinces)、类型（type）、数量、分析时间、分析人、删除标记、删除时间输出到表test_01中
Post:
http://localhost:8080/preprocess
{
	"input_sql_url":{
		"sql_type":"mysql",
		"username":"root",
		"password":"123456",
		"host":"127.0.0.1:3306",
		"database":"test"
	},
	"output_sql_url":{
		"sql_type":"mysql",
		"username":"root",
		"password":"123456",
		"host":"127.0.0.1:3306",
		"database":"test"
	},
	"temp_table": "collect_ccgp",
    "new_table": "test_01",
    "process":"area_type",
    "time": ["2019-5-30","2019-7-1"]
}
2. 采购人项目类型分布
在collect_ccgp表中对采购人/代理人的项目类型分布进行统计分析, 把ID、机构类别（代理人/采购人）、机构名称、类型（13类）、数量、分析时间、分析人、删除标记、删除时间输出到表test_01中
Post:
http://localhost:8080/preprocess
{
	"input_sql_url":{
		"sql_type":"mysql",
		"username":"root",
		"password":"123456",
		"host":"127.0.0.1:3306",
		"database":"test"
	},
	"output_sql_url":{
		"sql_type":"mysql",
		"username":"root",
		"password":"123456",
		"host":"127.0.0.1:3306",
		"database":"test"
	},
	"temp_table": "collect_ccgp",
    "new_table": "test_01",
    "process":"person_type",
    "time": ["2019-5-30","2019-7-1"]
}
3. 词云图分析
在collect_ccgp表中，对采购人/代理人的项目标题进行词云图分析, 把ID、机构类别（代理人/采购人）、机构名称、词云图所需数据（词：词频；）、分析时间、分析人、删除标记、删除时间输出到表test_01中
Post:
http://localhost:8080/ZTB
{
	"input_sql_url":{
		"sql_type":"mysql",
		"username":"root",
		"password":"root",
		"host":"127.0.0.1:3306",
		"database":"ylzx"
	},
	"output_sql_url":{
		"sql_type":"mysql",
		"username":"root",
		"password":"root",
		"host":"127.0.0.1:3306",
		"database":"ylzx"
	},
	"temp_table": "collect_ccgp",
    "new_table": "test_person_title",
    "process":"person_title",
    "time": ["2019-5-30","2019-7-1"]
}


4. 社交关系分析
在collect_ccgp表中，对采购人/代理人合作次数进行统计, 把ID、机构类别（代理人/采购人）、机构名称、关系者类别（代理人/采购人）、关系者名称、关系权重、分析时间、分析人、删除标记、删除时间,关系输出到表test_01中
Post:
http://localhost:8080/ZTB

{
	"input_sql_url":{
		"sql_type":"mysql",
		"username":"root",
		"password":"root",
		"host":"127.0.0.1:3306",
		"database":"ylzx"
	},
	"output_sql_url":{
		"sql_type":"mysql",
		"username":"root",
		"password":"root",
		"host":"127.0.0.1:3306",
		"database":"ylzx"
	},
	"temp_table": "collect_ccgp",
    "new_table": "social",
    "process":"social",
    "time": ["2019-5-30","2019-7-1"]
}

=====================




