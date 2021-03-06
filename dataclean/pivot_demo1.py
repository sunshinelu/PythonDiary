# -*- coding: utf-8 -*-

import pandas as pd
import pymysql
import numpy as np
from sqlalchemy import create_engine

from datetime import datetime

"""
对pivot_table透视表结果进行取数

"""

## 加上字符集参数，防止中文乱码
dbconn = pymysql.connect(
    host="localhost",  # 127.0.0.1
    database="gongdan",
    user="root",
    password="root",
    port=3306,
    charset='utf8'
)
table = "country_data_export"
# sql语句
sqlcmd = "select * from " + table

# 利用pandas 模块导入mysql数据
df = pd.read_sql(sqlcmd, dbconn)

df1 = pd.pivot_table(df, values=['USD', 'RMB'], index=['MONTH', 'COUNTRY'],
                     columns=['YEAR'], aggfunc=np.sum)
# print(df1)
"""
                           RMB                ...           USD             
YEAR                      2015          2016  ...          2018         2019
MONTH COUNTRY                                 ...                           
1     不丹                   NaN      173400.0  ...       52629.0          NaN
      东帝汶            6944634.0     6766136.0  ...     1425363.0    1144017.0
      中非              301833.0      703315.0  ...           NaN     251455.0
      丹麦           544728586.0   386098895.0  ...   101355679.0   98972448.0
      乌克兰          153671817.0   171862440.0  ...    43203781.0   42679584.0
      乌兹别克斯坦       120249540.0    57046705.0  ...    19855106.0   28181957.0
      乌干达           22206908.0    28885302.0  ...     6450808.0    4252166.0
      乌拉圭           75668126.0    72688769.0  ...     7430304.0    7718721.0
      ...

"""
df0 = df1.query('COUNTRY == ["美国"]')['USD']['2015']
# print(df0)
"""
MONTH  COUNTRY
1      美国         2036455362.0
10     美国         2377931455.0
11     美国         3052724335.0
12     美国         2711057131.0
2      美国         1800299509.0
3      美国         1433013025.0
4      美国         2154591982.0
5      美国         2122758258.0
6      美国         2124273327.0
7      美国         2185935479.0
8      美国         2106440641.0
9      美国         2092380152.0
Name: 2015, dtype: object
"""

# print(df1["美国"]["USD"]["2015"]) # 此方法不对
print(df.xs(3))


df2 = pd.pivot_table(df, values=['USD', 'RMB'], index=['MONTH'],
                     columns=['COUNTRY', 'YEAR'], aggfunc=np.sum)
# print(df2)
"""
              RMB                      ...        USD                      
COUNTRY        不丹                      ...         黑山                      
YEAR         2015      2016      2017  ...       2017       2018       2019
MONTH                                  ...                                 
1             NaN  173400.0       NaN  ...  1863100.0   649818.0   892165.0
10       179931.0  121781.0  100790.0  ...  1284824.0   614067.0        NaN
11        16457.0       0.0  270878.0  ...   661103.0   591031.0        NaN
12            0.0   79410.0       0.0  ...  1344046.0  1154593.0        NaN
2             NaN  129302.0  170088.0  ...   446437.0  1453558.0   790674.0
3             NaN  153236.0  177022.0  ...   608187.0  1626922.0   977015.0
4        113486.0    5474.0  177308.0  ...  1014198.0  1947009.0   735430.0
5        149862.0  225344.0  179840.0  ...   974245.0  1749905.0  1042158.0
6        173618.0   17589.0  330335.0  ...   932779.0  1398274.0        NaN
7             0.0  150756.0     204.0  ...  1566853.0   916155.0        NaN
8        287406.0  248772.0  648828.0  ...   810944.0   660676.0        NaN
9             0.0   15853.0  157842.0  ...   770300.0  1384076.0        NaN
"""
# print(df2['USD']['美国']['2015'])
"""
MONTH
1     2036455362.0
10    2377931455.0
11    3052724335.0
12    2711057131.0
2     1800299509.0
3     1433013025.0
4     2154591982.0
5     2122758258.0
6     2124273327.0
7     2185935479.0
8     2106440641.0
9     2092380152.0
Name: 2015, dtype: object
"""

table = "country_data_import"
# sql语句
sqlcmd = "select * from " + table

# 利用pandas 模块导入mysql数据
df = pd.read_sql(sqlcmd, dbconn)

df["USD"] = pd.to_numeric(df["USD"])
df["RMB"] = pd.to_numeric(df["RMB"])
print(df.dtypes)

df3 = pd.pivot_table(df, values=['USD', 'RMB'], index=['YEAR'],
                     columns=['COUNTRY'], aggfunc=np.sum)
print(df3)

# 对透视表进行排序
print(df3.sort_values(axis = 1, by='2015',ascending=False))

# 获取排序后的透视表部分数据
print(df3.sort_values(axis = 1, by='2019',ascending=False).iloc[4, 0:10])