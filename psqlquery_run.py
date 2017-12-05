#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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
