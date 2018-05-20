#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 15:40:31 2018

@author: Danny
"""

import pandas as pd
import os
from matplotlib import pyplot as plt
import seaborn as sns

os.chdir('/Users/Danny/Documents/Python Project/temp_csv')

app = pd.read_csv('AppControlReport.csv', 
                  parse_dates = ['system_date', 'receive_date', 
                                 'complete_doc_date','expried_date'])

# number of app by year and month

app['rcvd_year'] = app['receive_date'].dt.year
app['rcvd_month'] = app['receive_date'].dt.month

# count by year, month
app_by_mth = app.groupby(['rcvd_year', 'rcvd_month']).agg('count')['userid']

# max month, amount
print('Max month : {} with {:,} rcvd'.format(app_by_mth.idxmax(), 
      app_by_mth[app_by_mth.idxmax()]))

print('Min month : {} with {:,} rcvd'.format(app_by_mth.idxmin(),
      app_by_mth[app_by_mth.idxmin()]))

# line plot 
app_by_mth.plot()

# time series plot
ts = app.groupby(['receive_date', 'bundle']).agg('count')
sns.set()
ts['userid'].unstack().plot()
