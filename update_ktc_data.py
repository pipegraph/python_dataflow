import pyodbc
import pandas as pd
import sqlalchemy


# Define Database file location
DB = """D:\\Backup\\OSS & TS - Performance\\OSSDatabase.accdb"""

# Define connection string
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ='+ DB +';'
    )

# Initate connection
ms_con = pyodbc.connect(conn_str)

# list all table name
with ms_con.cursor() as ms_cur:
    # list all tables
    tables = [x.table_name for x in ms_cur.tables(tableType='TABLE')]
    print('List of all tables in DB')
    print(tables)

# list of tables to be injested to postgresql
tables = ['KTC_FrontEnd_Occupation_Code', 'KTC_FrontEnd_Reason_Code',
          'KTC_Occupation_Code_2018', 'KTC_Province_Type']

# initialized engine & connection to postgresql
pg_eng = sqlalchemy.create_engine('postgresql://postgres:dan1255599@localhost:5432/ktc')
pg_con = pg_eng.connect()

# copy msaccess to postgresql
for table in tables:
    print('Reading {} from MsAccess'.format(table))
    df = pd.read_sql(r'SELECT * from ' + table, con = ms_con)
    df.columns = [n.lower().replace(' ', '_') for n in df.columns]
    print('Dumping table {} to Postgresql'.format(table.lower()))
    df.to_sql(con = pg_con, name = table.lower() , if_exists = 'replace',
              index = False)

# clear connection
ms_cur.close()
ms_con.close()
pg_con.close()
pg_eng.dispose()