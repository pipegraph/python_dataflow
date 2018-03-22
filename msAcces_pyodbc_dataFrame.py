# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 14:04:56 2018

@author: Thanakrit.B
"""

import os
import pyodbc
import pandas as pd

[x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]

os.chdir('D:\\Backup\\OSS & TS - Performance')

# Connection string
conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=D:\\Backup\\OSS & TS - Performance\\2018\\OSS DataSales 201802.mdb;'
    )
# Initate Connection
cnxn = pyodbc.connect(conn_str)

# Instantiate Curser
crsr = cnxn.cursor()

# Print all view in database
for view_info in crsr.tables(tableType='TABLE'):
    print(view_info.table_name)

# Print all view in database
for view_info in crsr.tables(tableType='VIEW'):
    print(view_info.table_name)

# Print all table statistic
for stat in crsr.statistics(table='MIS_CC_OS_Data_2018', unique=True):
    print(stat.cardinality)

# Show column name
for row in crsr.columns(table = 'MIS_CC_OS_Data_2018'):
    print(row.column_name)
#
# Count number of row
row = crsr.execute("select count (*) as n from MIS_CC_OS_Data_2018")
print(row.n)


# View column name
for col in crsr.columns(table = 'MIS_FL_OS_Data_60_2018'):
    print(col.column_name + " : "
          + str(col.type_name) + " ( "
          + str(col.column_size) + " ) ")

# test fetchone / fetchall
crsr.execute("select * from MIS_FL_OS_Data_60_2018")
rows = crsr.fetchall()
while row is not None:
    crsr.skip(10)
    row = crsr.fetchone()
    print(row.AGE)

## List table name & records

dict_tbl = {'name': "", "row" : 0}
list_dict_tbl = []

# Print all tables in database + number of row
for table_info in crsr.tables(tableType = 'TABLE'):
    list_dict_tbl.append({'name' : table_info.table_name, 'row' : 0})
print(list_dict_tbl)

for dict_tbl in list_dict_tbl:
    print("table : " + dict_tbl['name'])
    for stat in crsr.statistics(table=dict_tbl['name'], unique=True):
        print("row no : " + str(stat.cardinality))
        dict_tbl['row'] = stat.cardinality

## Sampling data
# Retrive column name
tbl_idx = 2
crsr.execute("select * from " + list_dict_tbl[tbl_idx]['name'])
columns = [column[0] for column in crsr.description]

# Retrive Row and create list of row
list_row = []
crsr.execute("select * from " + list_dict_tbl[tbl_idx]['name'])
row = crsr.fetchone()
while row is not None:
    list_row.append(row)
    crsr.skip(10)  # skip 10 parts = sample 10% of data
    row = crsr.fetchone()

# convert list of row to dataframe with column names
df = pd.DataFrame([tuple(t) for t in list_row], columns = columns)

# View Sample data
df.head()

# save dataframe
os.chdir("C:\\Users\\Thanakrit.B\\Documents\\Python\\Data sanitization")
df.to_pickle('mis_cc_2018_sample.pkl')

# close connection
cnxn.close()

## Exploratory Data analysis

import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

os.chdir("C:\\Users\\Thanakrit.B\\Documents\\Python\\Data sanitization")
df = pd.read_pickle('mis_cc_2018_sample.pkl')

df.head()
sns.lmplot(data = df, x = 'Month', y = 'Monthly_Salary')
sns.boxplot(data = df['Monthly_Salary'].groupby(['Month']))
