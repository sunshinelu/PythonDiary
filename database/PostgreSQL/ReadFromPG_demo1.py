
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

"""
参考链接：
Python之Postgresql数据库操作
http://blog.sina.com.cn/s/blog_178bde9220102zx9j.html
"""

"""
conn = psycopg2.connect(database="gongdan", user="postgres", password="root", port="5432")
with conn:
    cur=conn.cursor()
    cur.execute("select * from ml_info_item")
    rows = cur.fetchall()
    t=pd.DataFrame(rows)

print(t)
"""

conn_mysql = create_engine('mysql+pymysql://root:root@localhost:3306/gongdan?'
                           'charset=utf8')


# create the database connection:
conn_pg = create_engine('postgresql://postgres:root@127.0.0.1:5432/gongdan')
# prepare the query:
ls_sql = 'SELECT * FROM ml_info_item'
# read data to a pandas DataFrame from a SQL query:
df_t = pd.read_sql(ls_sql, conn_mysql)
print(df_t[1:5])

# write a pandas DataFrame to the database:
df_t.to_sql("ml_info_item", conn_pg, if_exists='replace', index=False)

"""

# Update and retrival commands:

import psycopg2
conn = psycopg2.connect(database="dbname", user="username", password="pwd", host="127.0.0.1", port="5432")

cur = conn.cursor()
cur.execute('CREATE TABLE tab_c (ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL')
conn.commit()

cur.execute("INSERT INTO tab_c (ID,NAME) VALUES (1, 'a'");
cur.execute("INSERT INTO tab_c (ID,NAME) VALUES (2, 'b'");
conn.commit()

cur.execute("SELECT id, name from tab_c")
rows = cur.fetchall()
for row in rows:
   print("ID = ", row[0], "NAME = ", row[1])
conn.close()

"""