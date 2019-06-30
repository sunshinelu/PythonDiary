# -*- coding: utf-8 -*-

import numpy
import pandas
from sqlalchemy import create_engine
from udf_function import *

# engine = create_engine("mysql+pymysql://localhost:3306/talentscout", pool_size=5, echo_pool=True)
engine = create_engine("mysql+pymysql://root:root@localhost:3306/talentscout", pool_size=5, echo_pool=True)
conn = engine.connect()

# 1.读取需要清洗的数据
sql_data = pandas.read_sql_table('rc_jbxx', conn, index_col='id')
sql_data = sql_data[sql_data['ch_name'].notnull()]
# 2.清洗前进行字段填充及去空处理

sql_data = sql_data.apply(lambda item: deal_item(item), axis=1)

print(sql_data[10])