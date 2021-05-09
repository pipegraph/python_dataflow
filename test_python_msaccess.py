#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 15:00:19 2017

@author: Danny
"""

# Test pandas_access

import pandas_access as mdb

# show tables in databases
for tbl in mdb.list_tables('/Users/Danny/Share Win7/2017OSSDatabase.accdb'):
    print(tbl)

# Read in table as pandas dataframe
# Limited capability to small tables
df = mdb.read_table('/Users/Danny/Share Win7/2017OSSDatabase.accdb', 'Region_KTC')

# test Meza
from meza import io

records = io.read('/Users/Danny/Share Win7/2017OSSDatabase.accdb')

# not success

# test JayDeBeAPI

import jaydebeapi

# Initiate Java runtiome file location 

ucanaccess_jars = [
        "/Users/Danny/Documents/UCanAccess-4.0.2-bin/ucanaccess-4.0.2.jar",
        "/Users/Danny/Documents/UCanAccess-4.0.2-bin/lib/commons-lang-2.6.jar",
        "/Users/Danny/Documents/UCanAccess-4.0.2-bin/lib/commons-logging-1.1.1.jar",
        "/Users/Danny/Documents/UCanAccess-4.0.2-bin/lib/hsqldb.jar",
        "/Users/Danny/Documents/UCanAccess-4.0.2-bin/lib/jackcess-2.1.6.jar",
        ]

# classpath = $PATH$ parameters for Java runtime file location

classpath = ":".join(ucanaccess_jars)

# Initate connection to MS Access files
cnxn = jaydebeapi.connect(
    "net.ucanaccess.jdbc.UcanaccessDriver",
    "jdbc:ucanaccess:///Users/Danny/Share Win7/2017OSSDatabase.accdb",
    ["", ""],
    classpath
    )

# From connection initiate cursor
crsr = cnxn.cursor()

# Run Query
crsr.execute("SELECT * FROM Region_KTC")

# Fetch Query result
for row in crsr.fetchall():
    print(row)

# Close cursor
crsr.close()
# Close connection
cnxn.close()
