# -*- CODING: UTF-8 -*-
"""
CREATED ON MON OCT  9 15:32:51 2017

@AUTHOR: THANAKRIT.B
"""

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client import file

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# OAUTH2 secret string
# API_KEY = "nryvUmJWHO4dOHXq4JtED5y6"

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
2. Grant access process
"""

# autorized with http protocal
http = creds.authorize(httplib2.Http())

# autorized with http protocal
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')

service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

"""
3. Accessing data
"""
spreadsheetId = '1l2cJLTjxjNZpX-v2Z48Q6s3oy5casXltcR5IriWuRCw'
rangeName = 'data!A1:D5'
result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()

values = result.get('values', [])

if not values:
    print('No data found.')
else:
    print('Id, Eng Name, Eng Surname, Thai Name')
    for row in values:
        for col in row:
            print('%s' % col)