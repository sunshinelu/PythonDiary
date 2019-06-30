nation_sql = 'SELECT name,sort FROM `dict_new` where classify="民族" ORDER BY sort'
political_status_sql = 'SELECT name,sort FROM `dict_new` where classify="政治面貌" ORDER BY sort'
identification_type_sql = 'SELECT name,sort FROM `dict_new` where classify="证件类型" ORDER BY sort'
country_sql = 'SELECT name,sort FROM `dict_new` where classify="国家" ORDER BY sort'
highest_education_sql = 'SELECT name,sort FROM `dict_new` where classify="学历" ORDER BY sort'
highest_degree_sql = 'SELECT name,sort FROM `dict_new` where classify="学位" ORDER BY sort'
# 专业技术职务
profession_post_sql = 'SELECT name,sort FROM `profession_post_dict`'
# 行政区划
district_sql = 'SELECT SUBSTRING_INDEX(full_name, "省-", -1),1 FROM `district_dict` where `level`=1 UNION SELECT SUBSTRING_INDEX(full_name, "省-", -1),1 FROM `district_dict` where `level`=2'
# 职业
job_sql = 'SELECT name,1 from `job_dict`'
# 学科
subject_sql = 'SELECT name,1 from `subject_dict`'
# 学校
school_sql = "SELECT NAME ,rank FROM `university_dict` where NAME is not null UNION SELECT en_name ,rank FROM `university_dict` where en_name is not null UNION SELECT alias ,rank FROM `university_dict` where alias is not null"
# 性别
sex_sql = 'SELECT name,sort FROM `dict_new` where classify = "性别" or classify = "性别（数字）" ORDER BY sort'
# 身份证编码对应日期
area_sql = 'SELECT code,full_name FROM `gb/t_2260`'
# 单位
unit_sql = "SELECT NAME ,rank FROM `university_dict` where NAME is not null UNION SELECT en_name ,rank FROM `university_dict` where en_name is not null UNION SELECT alias ,rank FROM `university_dict` where alias is not null UNION SELECT NAME ,1 FROM `unit_dict` where NAME is not null UNION SELECT cym ,1 FROM `unit_dict` where cym is not null "
# provice_sql = 'SELECT `name` FROM `district_dict` where `level`=0 UNION SELECT short_name FROM `district_dict` where `level`=0'
provice_sql = 'SELECT `name` FROM `district_dict` where `level`=0 and LENGTH(name)<10  and name like "%%省"'
# 多字典列
multi_fields = ['country', 'professional_title', 'research_field', 'ids']
provices = ['河北', '山西', '辽宁', '吉林', '江苏', '浙江', '安徽', '福建', '江西', '山东',
            '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', ]
