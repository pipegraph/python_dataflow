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

#old_stdout = sys.stdout
#result = StringIO()
#sys.stdout = result

## Show each file, row num & summarizing
print("Sampling data from file : ", mis_files)

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
        force_dtype = {'amsup':object, 'tl_code':object, 'agent_code':object,\
           'zipcode':object, 'month':object, 'application_id':object,\
           'criteria_code':object, 'occupation_code':object, \
           'criteria_code_c':object, 'result_description':object}
        parse_date_col = ['dob', 'close_date']
        column_count_by_month = ['application_id']
        column_mean_by_month = ['approve_amount', 'money_transfer', 'monthly_salary']
    else:
        # for mis_cc
        force_dtype = {'amsup':object, 'tl_code':object, 'agent_code':object,\
                   'zipcode':object, 'month':object, 'application_id':object,\
                   'criteria_code':object, 'occupation_code':object,\
                   'criteria_code_c':object, 'result_description':object}
        parse_date_col = ['dob']
        column_count_by_month = ['application_id']
        column_mean_by_month = ['approve_amount', 'monthly_salary']

    # read data
    df = pd.read_csv(file, parse_dates = parse_date_col, dtype = force_dtype)

    # count by Month
    for col in column_count_by_month:
         print('Count of', col, 'by Month')
         print(df.groupby('month')[col].count(), '\n')
    # avg by Month
    for col in column_mean_by_month:
         print('Average of', col, 'by Month')
         print(df.groupby('month')[col].mean(), '\n')

# reversed stdout to original output
#sys.stdout = old_stdout
# retrive result as string
#result_str = result.getvalue()
# change back to original directory
os.chdir(old_dir)