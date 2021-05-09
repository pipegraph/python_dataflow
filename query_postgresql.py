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
#cur = con.cursor()

# print Postgresql version
#cur.execute('select version()')
#db_ver = cur.fetchone()
#print('DB version : {}'.format(db_ver[0]))
#
## count number of rows
#sql = r'select "Month", count (*) from mis_cc_os_data_2017 group by 1'
#cur.execute(sql)
#no_row = cur.fetchall()
#print(no_row)

"""
Use pandas
"""
# list table in postgre
sql = \
"""
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
"""
df = pd.read_sql_query(sql, con = con)
print(df)

# data all type team
data_all = pd.read_sql_table('dataalltypeteam', con = con)

# read list tl to be check
tl_file = r'D:\Backup\OSS - Activities\2018\2018 TL - Exclusive Night - 6-7 Jul\TL Name list\check_tl_list.xlsx'
tl = pd.read_excel(tl_file, dtype = {'TLCode':object})
print(tl)

# left join on df
tl_data = pd.merge(tl, data_all, left_on = 'TLCode', right_on = 'Agent_Code', how = 'left')

# export to excel
tl_data.to_excel('tl_data.xls')
