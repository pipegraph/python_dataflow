#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 17:44:12 2018

@author: Danny
"""
import os
import sqlalchemy
import pandas as pd

# create engine, connection to mysql server
eng = sqlalchemy.create_engine('mysql+pymysql://root:dan1255599@localhost/ktc?charset=utf8')
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
        force_dtype = {'AMSup':object, 'TL_Code':object, 'Agent_Code':object,\
           'ZipCode':object, 'Month':object, 'Application_ID':object,\
           'Criteria_Code':object, 'Occupation_Code':object}
    else:
        # for mis_cc
        force_dtype = {'AMSup':object, 'TL_Code':object, 'Agent_Code':object,\
                   'ZipCode':object, 'Month':object, 'Application_ID':object,\
                   'Criteria_Code':object, 'Occupation_Code':object,\
                   'Criteria_Code_P':object, 'Criteria_Code_C':object}
        
    # read csv file as dataframe
    df = pd.read_csv(file, parse_dates = ['DOB'], dtype = force_dtype)
    df.to_sql(con = con, name = file.split('.', 1)[0], if_exists = 'replace')

## read sales data
sales_data_files = [x for x in os.listdir('../temp_csv') if x.startswith('Data')]
# dtype for sales data
for file in sales_data_files:
    force_dtype = {'TL_Code':object, 'Agent_Code':object, 'ProvinceCode':object}
    df = pd.read_csv(file, parse_dates = ['OpenDate'], dtype = force_dtype)    
    df.to_sql(con = con, name = file.split('.', 1)[0], if_exists = 'replace')
