# -*- coding: utf-8 -*-
"""
Created on Mon May 21 19:37:57 2018

@author: Thanakrit.B
"""

import psycopg2 as pg
import pandas as pd

# create connection, cursor
con = pg.connect(host="localhost", database="ktc",
                       user="postgres", password="dan1255599")
cur = con.cursor()

# print Postgresql version
cur.execute('select version()')
db_ver = cur.fetchone()
print('DB version : {}'.format(db_ver[0]))

# count number of rows
sql = r'select "Month", count (*) from mis_cc_os_data_2017 group by 1'
cur.execute(sql)
no_row = cur.fetchall()
print(no_row)

# use pandas
sql = r'select "Month", count (*) from mis_cc_os_data_2017 group by 1'
df = pd.read_sql_query(sql, con = con)