#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 17:37:39 2017

Copyright (c) 2017 Trevor James Smith

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import psycopg2 as pg2
# import getpass
import logging

logger = logging.getLogger()

def include(filename):
    if os.path.exists(filename): 
        execfile(filename)

include('exec_file.py')

"""
nm = raw_input('Enter Postgres Username: ')
pw = getpass.getpass('Enter Password: ')

include('psqlquery_run.py')

"""
mypath = os.path.dirname(os.path.realpath( __file__ ))
shapefiles=[]

print '\n', shapefiles, '\n'

initconn = pg2.connect(host = 'localhost', user='postgres', password='password')
initconn.set_session(autocommit = True)

"""
initconn.cursor().execute('DROP DATABASE psycopg2;')
"""

try:
    initconn.cursor().execute('CREATE DATABASE psycopg2;')
    print "CREATED DATABASE PSYCOPG2. Continuing..."
except Exception:
    print "DATABASE PSYCOPG2 already exists. Continuing..."
    pass
initconn.close()

conn = pg2.connect(host = 'localhost', dbname = 'psycopg2', user='postgres', password='password')
conn.set_session(autocommit = True)
cur = conn.cursor()

try:
    cur.execute('CREATE EXTENSION postgis;')
    print "CREATED EXTENSION POSTGIS. Continuing..."
except Exception:
    print "EXTENSION POSTGIS already exists. Continuing..."
    pass

#cur.execute('SELECT st_centroid(geom) FROM counties')
#print cur.fetchone()[0]
conn.close()


