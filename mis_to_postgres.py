
# coding: utf-8

# In[ ]:


import os
import pyodbc
import pandas as pd
import numpy as np


# In[ ]:


# list all driver available
drivers = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]


# In[ ]:


# select best driver param, 1st 'ACE', 2nd 'Jet'
for driver in drivers:
    if driver == 'Microsoft Access Driver (*.mdb, *.accdb)':
        driver_param = '{Microsoft Access Driver (*.mdb, *.accdb)}'
    elif driver == 'Microsoft Access Driver (*.mdb)':
        driver_param = '{Microsoft Access Driver (*.mdb)}'
    else:
        driver_param = '{}'


# In[ ]:


# print selected driver param
dict_driver_param = {'{}':'Need to install MS Access driver.',
                     '{Microsoft Access Driver (*.mdb)}':'Windows support only .mdb',
                     '{Microsoft Access Driver (*.mdb, *.accdb)}':'Windows support .mdb, .accdb'}
print('Found driver : ' + driver_param + '\n' + dict_driver_param[driver_param])


# In[ ]:


# create connection string
DB = """D:\\Backup\\OSS & TS - Performance\\2017\\2017OSSDatabase.accdb"""
conn_str = (
    r'DRIVER=' + driver_param + ';'
    r'DBQ='+ DB +';'
    )


# In[ ]:


# Initate Connection & cursor
ms_con = pyodbc.connect(conn_str)
ms_cur = ms_con.cursor()


# ### Connect MsAccess get file and check Monthly Salary data

# In[ ]:


# list all table
tables = [x.table_name for x in ms_cur.tables(tableType='TABLE')]
tables


# In[ ]:


# select only mis tables
mis_tables = [x for x in tables if x.startswith('MIS')]
mis_tables


# In[ ]:


sql = 'select * from ' + mis_tables[1]


# In[ ]:


df = pd.read_sql(sql, con = ms_con)


# In[ ]:


df.shape


# In[ ]:


df.columns


# In[ ]:


# change 'column with ' ' to '_'
df.columns = [n.lower().replace(' ', '_').replace('/','_') for n in df.columns]


# In[ ]:


df.groupby(['month']).mean()['monthly_salary']


# ### Connect Postgres same and read data for comparing structor with MsAccess data

# In[ ]:


import sqlalchemy
import psycopg2 as pg


# In[ ]:


# sqlalchemy engine
pg_engine = sqlalchemy.create_engine('postgresql://postgres:dan1255599@localhost:5432/ktc')
pg_con = pg_engine.connect()

# use psycopg 2 connenction
con = pg.connect(host="localhost", database="ktc", user="postgres", password="dan1255599")
cur = con.cursor()

# drop old table
sql = """drop table mis_proud_os_data_60_2018 cascade"""
cur.execute(sql, con)

# commit change
con.commit()
# In[ ]:


# List all table
sql = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
"""
pd.read_sql_query(sql, con = pg_con)


# In[ ]:


# update df to postgresql
df.to_sql(con = pg_con, name = 'mis_proud_os_data_60_2017', if_exists = 'replace', index = False)

