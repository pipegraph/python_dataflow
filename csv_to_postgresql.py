#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 14:45:49 2018

@author: Danny
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
