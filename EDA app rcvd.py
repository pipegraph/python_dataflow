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

# scatterplot
date_bundle = ts['userid'].unstack()
sns.lmplot(data = date_bundle, x = 'N', y = 'Y')

# focus on source code like oss
oss = app[app['source_code'].str.startswith('O')]
ts = oss.groupby(['receive_date', 'bundle']).agg('count')
date_bundle = ts['userid'].unstack()
sns.lmplot(data = date_bundle, x = 'N', y = 'Y')

# filter before & after
before = date_bundle.loc[:'2017-07-31']
after = date_bundle.loc['2017-08-01':]

from scipy import stats

sns.lmplot(data = before, x = 'N', y = 'Y')
print('Pearson r : {:.5f}'.format(stats.pearsonr(before['N'], before['Y'])[0]))
sns.lmplot(data = after, x = 'N', y = 'Y')
print('Pearson r : {:.5f}'.format(stats.pearsonr(after['N'], after['Y'])[0]))

