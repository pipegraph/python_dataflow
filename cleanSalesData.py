# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 19:29:58 2017

@author: Thanakrit.B
"""
import os
import xlrd as xd
import pandas as pd

# Chenge to data folder
os.chdir('D:\Backup\OSS - Disclose Sales Data\Data Sentback - 20170612')

# Read file in dir
fl = os.listdir()

def read_sales_data(fl):
    out = pd.DataFrame()
    for f in fl:
        wb = xd.open_workbook(f)
        sh = wb.sheet_names()
        shLen = len(sh)
        if shLen > 1:
            df = pd.read_excel(f, sheetname = 1)
        else:
            df = pd.read_excel(f, sheetname = 0)
        out = out.append(df)
    return(out)

o = read_sales_data(fl)

os.chdir('D:\Backup\OSS - Disclose Sales Data')

writer = pd.ExcelWriter('out.xlsx')
o.to_excel(writer, 'sheet1')
writer.save()
