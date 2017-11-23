#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 22:59:32 2017

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
#import getpass
import logging

logger = logging.getLogger()
dirpath = os.path.dirname(os.path.realpath( __file__ ))

def include(filename):
    if os.path.exists(filename): 
        execfile(filename)

include('exec_file.py')

#nm = raw_input('Enter Postgres Username: ')
#pw = getpass.getpass('Enter Password: ')

nm='postgres'
pw='password'

shapefiles=[]

listShapefiles(dirpath, shapefiles)

print '\n', shapefiles, '\n'

#conn = pg2.connect(host = 'localhost', dbname = 'psycopg2', user=nm, password=pw)
#conn.set_session(autocommit = True)
#cur = conn.cursor()

#cur.execute('SELECT st_centroid(geom) FROM counties')
#print cur.fetchone()[0]

#executeScriptsFromFile('sql_queries.psql')

#conn.close()