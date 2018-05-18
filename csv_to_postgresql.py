#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 14:45:49 2018

@author: Danny
"""
"""
import psycopg2 as pg

con = pg.connect('dbname=ktc user=postgres password=dan1255599')

cur = con.cursor()

cur.execute('create table test (id serial primary key, num integer, data varchar);')

cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

cur.execute('select * from test;')

cur.fetchone()

con.commit()
cur.close()
con.close()
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
        force_dtype = {'AMSup':object, 'TL_Code':object, 'Agent_Code':object,\
           'ZipCode':object, 'Month':object, 'Application_ID':object,\
           'Criteria_Code':object, 'Occupation_Code':object, \
           'Criteria_Code_C':object, 'Result_Description':object}
        parse_date_col = ['DOB', 'CLOSE_DATE']
    else:
        # for mis_cc
        force_dtype = {'AMSup':object, 'TL_Code':object, 'Agent_Code':object,\
                   'ZipCode':object, 'Month':object, 'Application_ID':object,\
                   'Criteria_Code':object, 'Occupation_Code':object,\
                   'Criteria_Code_C':object, 'Result_Description':object}
        parse_date_col = ['DOB']

    # read csv file as dataframe
    df = pd.read_csv(file, parse_dates = parse_date_col, dtype = force_dtype)
    df.to_sql(con = con, name = file.split('.', 1)[0].lower(), if_exists = 'replace')
