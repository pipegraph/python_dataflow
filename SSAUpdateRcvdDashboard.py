# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 17:17:20 2017

@author: Thanakrit.B
"""
"""
Use pyodbc to connect with MSAccess
"""

import pyodbc

# Check if MS Access driver available
[x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]

# Connection String
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\\Users\\Thanakrit.B\\Documents\\Python\\Run_Appcontrol_new.mdb;'
    )

# Initiate connection
cnxn = pyodbc.connect(conn_str)

# Initiate cursor
crsr = cnxn.cursor()


import pandas as pd

query = "select * from Channel;"
df = pd.read_sql(query, cnxn)

# close connection
cnxn.close()

"""
Starting OAuth process
"""
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client import file

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

"""
1. Define Credential argument
"""

# Define scope
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# Define secret file
CLIENT_SECRET_FILE = 'client_secret.json'

# Registerd application name
APPLICATION_NAME = 'Google Sheets API Python Sales Support Dashboard'

# Storage of access granted token file (.json)
store = file.Storage('sheets.googleapis.python-googlesheet.json')

# Get credential details from token file (.json)
creds = store.get()

# In case credentail not available / valid
if not creds or creds.invalid:
    # Define flow of granting access with stored secret key (file client_secret.json)
    # with scoped defined
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME

    # get credential from flow defiened then store in token file
    creds = tools.run_flow(flow, store, flags)

"""
2. Accessing data
"""
import gspread

# Authorized application
gc = gspread.authorize(creds)

# Initiate first worksheet
wks = gc.open('Agent_Channel_Group.xls').sheet1

# clear data in worksheet
wks.clear()

# update header
header = df.columns.values.tolist()
header_range = 'A1:' + gspread.utils.rowcol_to_a1(1, df.shape[1])

cell_list = wks.range(header_range)
for cell in cell_list:
    cell.value = header[cell.col-1]
wks.update_cells(cell_list)

# update value
data = df.values.tolist()
data_range = 'A2:' + wks.get_addr_int(df.shape[0] + 1, df.shape[1])

cell_list = wks.range(data_range)
for cell in cell_list:
    cell.value = data[cell.row-2][cell.col-1]
wks.update_cells(cell_list)

