# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 17:24:30 2018

@author: Thanakrit.B
"""

import psycopg2 as pg
import pandas as pd

# create connection, cursor
con = pg.connect(host="localhost", database="ktc",
                       user="postgres", password="dan1255599")
cur = con.cursor()

# list table in postgre
sql = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
"""
cur.execute(sql)
cur.fetchall()


# create view
sql = """
TRUCTCATE IF EXIST view_telesale_office
CREATE VIEW view_telesales_office
AS
SELECT *
FROM