#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 14:41:34 2018

@author: Danny
"""
from read_csv_aggregrate import result_str
import smtplib

SERVER = 'smtp.office365.com'
body = \
"""From: Automatic Emailer <thanakrit.b@ktc.co.th>
To: Thanakrit.b <thanakrit.b@ktc.co.th>
Subject: [Automatic Emailer] data sanity check completed

""" + result_str
try:
    smtp_ktc = smtplib.SMTP(SERVER, 587)
except Exception as e:
    print(e)
    smtp_ktc = smtplib.SMTP_SSL(SERVER, 465)

smtp_ktc.ehlo()
smtp_ktc.starttls()
smtp_ktc.login('thanakrit.b@ktc.co.th', 'CDOin47mth')
smtp_ktc.sendmail('thanakrit.b@ktc.co.th', 'thanakrit.b@ktc.co.th', body)
smtp_ktc.quit()