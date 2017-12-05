#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import psycopg2 as pg2
import getpass

def include(filename):
    if os.path.exists(filename): 
        execfile(filename)

def listShapefiles(mypath, shapefiles):
    for filename in os.listdir(mypath):
        if filename.endswith(".shp"):
            filepath = mypath + '/' + filename
            shapefiles.append(filepath)

def psqlCredentials():
    dbname = str(raw_input('Enter Database Name: '))
    user = str(raw_input('Enter Postgres Username: '))
    passwd = str(getpass.getpass('Enter Password: '))
    cred = ({
            "dbname": dbname,
            "user": user,
            "passwd": passwd
            }
    )

include('exec_file.py')
include('psycopg2_connection.py')

mypath = os.path.dirname(os.path.realpath( __file__ ))
shapefiles=[]
listShapefiles(mypath,shapefiles)

print '\n', shapefiles, '\n'



initconn = pg2.connect(host = 'localhost', user='postgres', password='password')
initconn.set_session(autocommit = True)

initconn.cursor().execute('DROP DATABASE psycopg2;')


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


