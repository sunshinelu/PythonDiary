# 测试用例

1. 缺失值处理接口

(1) ml_info_type表中table_name为空的，将table_name字段为空值的全部数据保存出来。
Post:

http://localhost:8080/preprocess

{
	"input_sql_url":{
		"sql_type":"mysql",
		"username":"root",
		"password":"root",
		"host":"127.0.0.1:3306",
		"database":"gongdan"
	},
	"output_sql_url":{
		"sql_type":"mysql",
		"username":"root",
		"password":"root",
		"host":"127.0.0.1:3306",
		"database":"gongdan"
	},
	"temp_table": "ml_info_type",
    "new_table": "ml_info_type_copy_data_invalid101",
    "process": ["data_null", "save"],
    "params": ["TABLE_NAME"]
}