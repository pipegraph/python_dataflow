import os
import pyodbc
import csv

"""
Exporting from MS Access as .csv
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
DB = """//10.24.9.41\Outsource_Sales_Register\DataBase\SalesData.mdb"""
conn_str = (
    r'DRIVER=' + driver_param + ';'
    r'DBQ='+ DB +';'
    )
# Initate Connection
con = pyodbc.connect(conn_str)
with con.cursor() as cur:
    # list all tables
    views = [x.table_name for x in cur.tables(tableType='VIEW')]
    print('List of all tables in DB')
    print(views)

    # Export each table to temp_csv
    os.chdir(r'C:\Users\Thanakrit.B\Downloads\temp_csv')
    views = ['DataAllType']

    for view in views:
        if view != '':
            filename = view.replace(" ","_") + ".csv"

            print("Dumping " + view)
            # retrive table
            rows = cur.execute("SELECT * FROM " + "[" + view + "]")

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
con.close()

"""
Import to Postgre
"""