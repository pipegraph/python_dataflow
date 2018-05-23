import os
import pyodbc
import csv
from tkinter import *
from tkinter.filedialog import askopenfilename
"""
Look for MSAccess driver install in windows
'Microsoft Access Driver (*.mdb)' : 32-bits 'Jet' driver, default with windows
'Microsoft Access Driver (*.mdb, *.accdb)' : 32-bits or 64-bits 'ACE' driver, come with MS Office
, could download from https://www.microsoft.com/en-US/download/details.aspx?id=13255
"""

# list all driver available
drivers = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]

# select best driver param, 1st 'ACE', 2nd 'Jet'
for driver in drivers:
    if driver == 'Microsoft Access Driver (*.mdb, *.accdb)':
        driver_param = '{Microsoft Access Driver (*.mdb, *.accdb)}'
    elif driver == 'Microsoft Access Driver (*.mdb)':
        driver_param = '{Microsoft Access Driver (*.mdb)}'
    else:
        driver_param = '{}'

# print selected driver param
dict_driver_param = {'{}':'Need to install MS Access driver.',
                     '{Microsoft Access Driver (*.mdb)}':'Windows support only .mdb',
                     '{Microsoft Access Driver (*.mdb, *.accdb)}':'Windows support .mdb, .accdb'}
print('Found driver : ' + driver_param + '\n' + dict_driver_param[driver_param])

# create connection string
root = Tk()
root.withdraw()
DB = askopenfilename()
root.destroy()
# DB = 'C:\\Users\\Thanakrit.B\\Downloads\\OSS DataSales 201803.mdb'
conn_str = (
    r'DRIVER=' + driver_param + ';'
    r'DBQ='+ DB +';'
    )
# Initate Connection
con = pyodbc.connect(conn_str)
try:
    with con.cursor() as cur:
        # list all tables
        tables = [x.table_name for x in cur.tables(tableType='TABLE')]
        print('List of all tables in DB')
        print(tables)

    # Create temp csv directory for store files
    try:
        os.mkdir('..\\temp_csv')
    except:
        print('temp_csv dir created')

    # Export each table to temp_csv
    os.chdir('temp_csv')

    for table in tables:
        if table != '':
            filename = table.replace(" ","_") + ".csv"

            print("Dumping " + table)
            # retrive table
            rows = cur.execute("SELECT * FROM " + "[" + table + "]")

            # convert column name to match postgresql
            old_col_name = [desc[0] for desc in cur.description]
            new_col_name = [c.strip().replace(' ', '_').replace('/', '_') for c in old_col_name]

            # specify newline = '', no extra \r before \r\n in line ending
            with open(filename, 'w', newline = '', encoding = 'utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # write new_col_name
                writer.writerow(new_col_name)

                # write data
                for row in rows:
                    writer.writerow(row)
finally:
    con.close()