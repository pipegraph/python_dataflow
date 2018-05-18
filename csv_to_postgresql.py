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
    if file.find('CC') == -1:
        # for mis_fl, mis_rl
        force_dtype = {'amsup':object, 'tl_code':object, 'agent_code':object,\
           'zipcode':object, 'month':object, 'application_id':object,\
           'criteria_code':object, 'occupation_code':object, \
           'criteria_code_c':object, 'result_description':object}
        parse_date_col = ['dob', 'close_date']
    else:
        # for mis_cc
        force_dtype = {'amsup':object, 'tl_code':object, 'agent_code':object,\
                   'zipcode':object, 'month':object, 'application_id':object,\
                   'criteria_code':object, 'occupation_code':object,\
                   'criteria_code_c':object, 'result_description':object}
        parse_date_col = ['dob']

    # read csv file as dataframe
    print('Reading', file, '\n')
    df = pd.read_csv(file, parse_dates = parse_date_col, dtype = force_dtype)
    # write back to dbms
    print('Dumping', file, 'to Postgre\n')
    df.to_sql(con = con, name = file.split('.', 1)[0].lower(), if_exists = 'replace')
