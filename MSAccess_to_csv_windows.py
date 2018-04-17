import os
import pyodbc
import csv

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
DB = 'C:\\Users\\Thanakrit.B\\Downloads\\OSS DataSales 201802.mdb'
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
    os.chdir('..\\temp_csv')

    for table in tables[2:]:
        if table != '':
            filename = table.replace(" ","_") + ".csv"
            print("Dumping " + table)
            rows = cur.execute("SELECT * FROM " + table)
            # specify newline = '', no extra \r before \r\n in line ending
            with open(filename, 'w', newline = '', encoding = 'utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([x[0] for x in cur.description])
                for row in rows:
                    writer.writerow(row)
finally:
    con.close()