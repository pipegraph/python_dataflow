#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 12:02:48 2018

@author: Danny
"""
import os
from io import StringIO
import sys
import pandas as pd
import multiprocessing as mp

# Check number of core avaliable
num_core = mp.cpu_count()

print('This cpu has', num_core, 'core(s) available for use')

# list of file start with MIS
mis_files = [x for x in os.listdir(os.path.join('..','temp_csv')) if x.startswith('MIS')]

## keep old stdio config, divert all print to var 'result'

old_stdout = sys.stdout
result = StringIO()
sys.stdout = result

## Show each file, row num & summarizing

for file in mis_files:
    old_dir = os.getcwd()
    os.chdir(os.path.join('..', 'temp_csv'))

    # count row num of csv file, define chunk size by 10%
    row_count = sum(1 for line in open(file, 'rt', encoding = 'utf-8'))
    chunk_no = 10
    chunk_size = row_count // chunk_no

    # print row num
    print(file, 'have', row_count, 'rows')

    # define column to be force dtype , to be summarized by Month
    if file.find('CC') == -1:
        # for mis_fl, mis_rl
        force_dtype = {'AMSup':object, 'TL_Code':object, 'Agent_Code':object,\
           'ZipCode':object, 'Month':object, 'Application_ID':object,\
           'Criteria_Code':object, 'Occupation_Code':object}
        column_count_by_month = ['Application_ID']
        column_mean_by_month = ['Approve_Amount', 'Money_Transfer', 'Monthly_Salary']
    else:
        # for mis_cc
        force_dtype = {'AMSup':object, 'TL_Code':object, 'Agent_Code':object,\
                   'ZipCode':object, 'Month':object, 'Application_ID':object,\
                   'Criteria_Code':object, 'Occupation_Code':object,\
                   'Criteria_Code_P':object, 'Criteria_Code_C':object}
        column_count_by_month = ['Application_ID']
        column_mean_by_month = ['Approve_Amount', 'Monthly_Salary']

    # read data
    df = pd.read_csv(file, parse_dates = ['DOB'], dtype = force_dtype)

    # count by Month
    for col in column_count_by_month:
         print('Count of', col, 'by Month')
         print(df.groupby('Month')[col].count(), '\n')
    # avg by Month
    for col in column_mean_by_month:
         print('Average of', col, 'by Month')
         print(df.groupby('Month')[col].mean(), '\n')

# reversed stdout to original output
sys.stdout = old_stdout
# retrive result as string
result_str = result.getvalue()
# change back to original directory
os.chdir(old_dir)