import os
import pyodbc
import pandas as pd

# Define Database file location
DB = """//10.24.9.41\Outsource_Sales_Register\DataBase\SalesData.mdb"""

# Define connection string
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ='+ DB +';'
    )

# Initate connection
con = pyodbc.connect(conn_str)

# list all table name
with con.cursor() as cur:
    # list all tables
    tables = [x.table_name for x in cur.tables(tableType='TABLE')]
    print('List of all tables in DB')
    print(tables)

# Pandas read sql ; cannot fetch table
table = 'SaleHis_Chang'

df = pd.read_sql(r'SELECT * from ' + table, con = con)
con.close()

# check data & convert columns names
df.shape
df.columns = [n.lower().replace(' ', '_') for n in df.columns]
df.dtypes

"""
Update to postgre
"""
import sqlalchemy

# initialized engine & connection
eng = sqlalchemy.create_engine('postgresql://postgres:dan1255599@localhost:5432/ktc')
con = eng.connect()

# list table in postgre
sql =   """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        """
tbl_list = pd.read_sql_query(sql, con = con)
print(tbl_list)

# write table to postgres
df.to_sql(con = con, name = table.lower() , if_exists = 'replace')
con.close()