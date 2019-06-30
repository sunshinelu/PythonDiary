# -*- coding: utf-8 -*-

import re
import numpy
import pandas
import constant
from sqlalchemy import create_engine

from pyspark.sql import SparkSession
import pyspark.sql.functions as func
from pyspark.sql.window import Window

from pyspark.sql.types import StringType

spark = SparkSession\
        .builder\
        .appName("join data")\
        .getOrCreate()

# Loading data from a JDBC source
url = "jdbc:mysql://localhost:3306/talentscout?useUnicode=true&characterEncoding=UTF-8&user=root&password=root"
ds_area = spark.read.jdbc(url=url,table="gb_t_2260",properties={"driver": 'com.mysql.jdbc.Driver'}).select("code","full_name").dropna()
# 身份证编码对应日期
# area_sql = "SELECT code,full_name FROM talentscout.gb/t_2260"
# ds_area = spark.sql(area_sql)
# ds_area.show()

ds = spark.read.jdbc(url=url,table="rc_jbxx").dropna(subset=['ch_name'])
# ds.show()


def replace(column, value):
    return func.when(column == value, func.lit(None)).otherwise(column)

for c_name in ds.columns:
    # 每列数据去除前后空格
    ds = ds.withColumn(c_name, func.trim(func.col(c_name)))
    # 每列数据将无替换为null
    ds = ds.withColumn(c_name, replace(func.col(c_name),"无"))

# ds.show()
# ds.select("job","position").show()


# job为None,position不为None position填充job
def job_position(job, position):
    return func.when((job !=None),job).otherwise(position)

# position为None,job不为None,job填充position
def position_job(position, job):
    return func.when((position !=None),position).otherwise(job)

ds = ds.withColumn("job",job_position(func.col("job"), func.col("position")))\
    .withColumn("position", position_job(func.col("position"), func.col("job")))


# ds.select("job","position").show()
ds.write.jdbc(mode="overwrite",url = url,table="sunlu_step1",properties={"driver": 'com.mysql.jdbc.Driver'})
ds.select("sex").drop_duplicates().show(truncate = False)

#######################################################################
engine = create_engine("mysql+pymysql://root:123456@192.168.44.4/talentscout_source", pool_size=5, echo_pool=True)
conn = engine.connect()

match_symbol_regex = re.compile('[\s,，、]+')


def get_field_similarity(target, source):
    """获取两个字段的相似度"""
    target = list(target)
    source = list(source)
    s1 = set(target)
    s2 = set(source)
    actual_jaccard = round(len(s1.intersection(s2)) / len(s1.union(s2)), 2)
    return actual_jaccard

def takeSecond(elem):
    return elem[2]

def __to_standard(string, dicts, match=1, multi=False):
    """
    标准换到字典
    :param string: 需要进行标准化的内容
    :param dicts: 标准
    :param match:匹配度大于等于该值是不进行继续匹配
    :param multi 是否可通过分隔符来清洗，清洗完通过,拼接
    :return: 标准话之后的内容(匹配内容，匹配度，重要度)
    """
    # 查看是否存在多项 是否有,来分割
    strings = string.split('、')
    results = []
    for dict_str in strings:
        result_match_degree = 0
        result = None
        # print(string)
        for dict_item in dicts.values:
            # damerau_levenshtein = textdistance.damerau_levenshtein.normalized_similarity(dict_str, item[0])
            # jaro_winkler = textdistance.jaro_winkler.normalized_similarity(dict_str, item[0])
            # smith_waterman = textdistance.smith_waterman.normalized_similarity(dict_str, item[0])
            # average_match_degree = damerau_levenshtein * 0.65 + jaro_winkler * 0.25 + smith_waterman * 0.1
            # average_match_degree = Simhash(item[0]).hamming_distance(Simhash(dict_str))
            index = dict_str.find('$')
            if index != -1:
                dict_str = dict_str[:index]
            for item in dict_item[0].split(' '):  # 存在空格隔开多值情况
                average_match_degree = get_field_similarity(item, dict_str)
                # print(item[0] + ',' + dict_str + ":" + str(average_match_degree))
                if average_match_degree > result_match_degree:
                    result_match_degree = average_match_degree
                    result = (item, result_match_degree, dict_item[1])
                    # if result_match_degree >= match:
                    #    break
                    # print("result:" + result + ";" + str(result_match_degree))
        if result:
            results.append(result)

    if not results:
        # 没有匹配
        return None
    if multi:
        # 需要多值
        results = [t for t in set(_ for _ in results)]
        key = "、".join(list(map(lambda x: x[0], results)))
        value = "、".join(list(map(lambda x: str(x[1]), results)))
        return (key, value, 1)
    else:
        # 不需要多值
        results.sort(key=takeSecond)
        return (results[0][0], results[0][1], results[0][2])



def split_standard(string, dicts, match=1, multi=False):
    """
    替换分隔符进行标准化,将空格、替换为中文，
    :param string: 需要进行标准化的内容
    :param dicts: 标准
    :param multi 是否可通过分隔符来清洗，清洗完通过,拼接
    :return: 标准话之后的内容(原内容，匹配内容，匹配度，重要程度，值越小越重要)
    """
    if not string or string.strip() == '':
        return None
    # 替换
    string_after = re.sub(match_symbol_regex, "、", string).strip('、').strip()
    result = __to_standard(string_after, dicts, match, multi)
    index = string.find('$')
    if index != -1:
        index = index + 1
        string = string[index:]
    if not result:
        return (string, None, 0, 1)
    return (string, result[0], result[1], result[2])


def clean_to_sql(source, dict_source, source_type, match=1.0, multi=False):
    """
    将字段值按照字典清洗，保存到数据库中，数据库数据类型字段为type
    :param source: 待清洗的字段值
    :param dict_source: 字典
    :param source_type: 清洗的数据类型
    :param match:匹配度大于等于该值是不进行继续匹配
    :param multi:清洗的字段是否为多值
    """

    dict_content = pandas.read_sql(dict_source, conn)
    source_content = source.drop_duplicates()

    result = source_content.map(lambda item: split_standard(item, dict_content, match, multi))
    results = []
    for key, value in result.iteritems():
        if value:
            results.append(value)
    data = {'field': list(map(lambda x: x[0], results)), 'dict': list(map(lambda x: x[1], results)),
            'similarity': list(map(lambda x: x[2], results)), 'sort': list(map(lambda x: x[3], results)),
            'type': source_type, 'prefix': list(map(lambda x: x[0][:1], results))}
    df = pandas.DataFrame(data)
    df.to_sql('clean_field', conn, index=False, if_exists='append')

provices = ['河北', '山西', '辽宁', '吉林', '江苏', '浙江', '安徽', '福建', '江西', '山东',
            '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', ]

def split_provice(address):
    min_len = 3
    if len(address) > min_len:
        for provice in provices:
            if address.find(provice) != -1:
                return address.replace(provice, '').replace('省', '')
    return address


def find_area(field):
    """
    查找是否存在，区县旗
    :param field:
    :return:
    """
    index = field.find('区')
    if index != -1:
        return index
    index = field.find('县')
    if index != -1:
        return index
    index = field.find('旗')
    return index


def replace_address(address):
    # 去除省份
    after_address = split_provice(address)
    after_address = after_address.replace('-', '').strip()
    # 地址裁剪，通过县区旗裁剪或者通过长度裁剪
    max_len = 6
    index = find_area(after_address)
    if index != -1:
        after_address = after_address[:index]
    elif len(after_address) > max_len:
        after_address = after_address[:max_len]
    after_address = after_address + '$' + address
    return after_address


def address_remove_provice(address):
    # 清洗地市去掉省份
    address = address.drop_duplicates().dropna()
    address = address.map(lambda item: replace_address(item))
    return address



def base_info_standard_match(sql_data):
    """
    需要进行标准化清洗的字段进行分组去重，将分组去去重后的字段进行清洗，并保存到数据库中
    :param sql_data: 源数据
    """
    # 性别
    clean_to_sql(sql_data['sex'], constant.sex_sql, 'sex',
                 multi='sex' in constant.multi_fields)
    # 民族
    clean_to_sql(sql_data['nation'], constant.nation_sql, 'nation',
                 multi='nation' in constant.multi_fields)
    # 政治面貌
    clean_to_sql(sql_data['political_status'], constant.political_status_sql, 'political_status',
                 multi='political_status' in constant.multi_fields)
    # 三类地址相似度比较大时，推荐整合成一列进行去重后匹配
    address = sql_data['csd']
    address = address.append(sql_data['native_place'])
    address = address.append(sql_data['address'])
    # 地址处理，便于地址标准化
    address = address_remove_provice(address)
    clean_to_sql(address, constant.district_sql, 'address', False)
    # pdb.set_trace()
    # 出生地
    # clean_to_sql(sql_data['csd_c'], constant.district_sql, 'csd',
    #             multi='csd' in constant.multi_fields)
    # 籍贯
    # clean_to_sql(sql_data['native_place_c'], constant.district_sql, 'native_place',
    #             multi='native_place' in constant.multi_fields)
    # 联系地址
    # clean_to_sql(sql_data['address_c'], constant.district_sql, 'address',
    #             multi='address' in constant.multi_fields)
    # 证件类型
    clean_to_sql(sql_data['identification_type'], constant.identification_type_sql, 'identification_type',
                 multi='identification_type' in constant.multi_fields)
    # 国籍
    clean_to_sql(sql_data['country'], constant.country_sql, 'country',
                 multi='country' in constant.multi_fields)
    # 工作单位,仅使用学校和科研机构
    clean_to_sql(sql_data['work_unit'], constant.unit_sql, 'work_unit',
                 multi='work_unit' in constant.multi_fields)
    # pdb.set_trace()
    # 专业技术职务
    clean_to_sql(sql_data['professional_title'], constant.profession_post_sql, 'professional_title',
                 multi='professional_title' in constant.multi_fields)
    # pdb.set_trace()
    # 职业
    clean_to_sql(sql_data['job'], constant.job_sql, 'job',
                 multi='job' in constant.multi_fields)
    # pdb.set_trace()
    # 研究领域
    clean_to_sql(sql_data['research_field'], constant.subject_sql, 'research_field',
                 multi='research_field' in constant.multi_fields)
    # pdb.set_trace()
    # 毕业院校
    clean_to_sql(sql_data['graduated_university'], constant.school_sql, 'graduated_university',
                 multi='graduated_university' in constant.multi_fields)
    # pdb.set_trace()
    # 最高学历
    clean_to_sql(sql_data['highest_education'], constant.highest_education_sql, 'highest_education',
                 multi='highest_education' in constant.multi_fields)
    # pdb.set_trace()
    # 最高学位
    clean_to_sql(sql_data['highest_degree'], constant.highest_degree_sql, 'highest_degree',
                 multi='highest_degree' in constant.multi_fields)
    # pdb.set_trace()












spark.stop()