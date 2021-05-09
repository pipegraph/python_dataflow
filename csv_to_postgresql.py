#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 14:45:49 2018

@author: Danny
"""
import os
import sqlalchemy
import pandas as pd

# create engine, connection to mysql server
eng = sqlalchemy.create_engine('postgresql://postgres:dan1255599@localhost:5432/ktc')
con = eng.connect()

# list of file start with MIS
mis_files = [x for x in os.listdir('../temp_csv') if x.startswith('MIS')]

# read csv, create table in mysql
for file in mis_files:
    old_dir = os.getcwd()
    os.chdir('../temp_csv')

    # define column to be force dtype , to be summarized by Month

    # 2018 data type
    if file.find('2018'):
        # if file name contain 'CC'
        if file.find('CC'):
            # define dtype for mis_cc
            force_dtype = {'AMSup':object, 'TL_Code':object, 'Agent_Code':object,
                           'ZipCode':object, 'Month':object, 'Application_ID':object,
                           'Criteria_Code':object, 'Occupation_Code':object,
                           'Criteria_Code_C':object, 'Result_Description':object}
            parse_date_col = ['DOB']
        # if file name not contain 'CC'
        else:
            # define dtype for rl, fl
            force_dtype = {'AMSup':object, 'TL_Code':object, 'Agent_Code':object,
                           'ZipCode':object, 'Month':object, 'Application_ID':object,
                           'Criteria_Code':object, 'Occupation_Code':object,
                           'Criteria_Code_C':object, 'Result_Description':object}
            parse_date_col = ['DOB', 'CLOSE_DATE']

    # 2017 data type
    else:
        if file.find('CC'):
            # define dtype for mis_cc
            force_dtype = {'AMSup':object, 'TL_Code':object, 'Agent_Code':object,
                           'ZipCode':object, 'Month':object, 'Application_ID':object,
                           'Criteria_Code':object, 'Occupation_Code':object,
                           'Criteria_Code_C':object, 'Result_Description':object}
            parse_date_col = ['DOB']
        # if file name not contain 'CC'
        else:
            # define dtype for rl, fl
            force_dtype = {'AMSup':object, 'TL_Code':object, 'Agent_Code':object,
                           'ZipCode':object, 'Month':object, 'Application_ID':object,
                           'Criteria_Code':object, 'Occupation_Code':object,
                           'Criteria_Code_C':object, 'Result_Description':object}
            parse_date_col = ['DOB', 'CLOSE_DATE']


    # read csv file as dataframe
    print('Reading', file, '\n')
    df = pd.read_csv(file, parse_dates = parse_date_col, dtype = force_dtype)
    # write back to dbms
    print('Dumping', file, 'to Postgre\n')
    df.to_sql(con = con, name = file.split('.', 1)[0].lower(), if_exists = 'replace', index = False)

# close connection & dispose engine
con.close()
eng.dispose()
