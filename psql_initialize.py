#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import psycopg2 as pg2
import getpass

def include(script):
    if os.path.exists(script): 
        execfile(script)

def listShapefiles(args):
    filepath=[]
    for filename in os.listdir(args):
        if filename.endswith(".shp"):
            shapefile = args + '/' + filename
            filepath.append(shapefile)
    return filepath

def psqlCredentials(args):
    dbname = str(raw_input('Enter Database Name: '))
    user = str(raw_input('Enter Postgres Username: '))
    passwd = str(getpass.getpass('Enter Password: '))
    args = ({
            "dbname": dbname,
            "user": user,
            "passwd": passwd
            })
    return args

def psqlInitialize():
    include('exec_file.py')
    include('psycopg2_connection.py')

    mypath = os.path.dirname(os.path.realpath( __file__ )) + "/data"
    shapefiles = []
    shapefiles.append(listShapefiles(mypath))

    print("The following shapefiles have been read from the working directory")
    print(shapefiles)

    cred={}
    cred.update(psqlCredentials(cred))
    createdb = str("host = 'localhost', user='{user}', password='{passwd}'").format(**cred)
    print(createdb)

    initconn = pg2.connect(createdb)
    initconn.set_session(autocommit = True)
    setupcur = initconn.cursor()
    
    setupcur.execute('DROP DATABASE psycopg2;')

    try:
        setupcur.execute('CREATE DATABASE psycopg2;')
        print ("CREATED DATABASE PSYCOPG2. Continuing...")
    except Exception:
        print("DATABASE PSYCOPG2 already exists. Continuing...")
        pass
    initconn.close()

    createPGIS = "host = 'localhost', dbname = '{dbname}', user='{user}', password='{passwd}'".format(**cred)
    conn = pg2.connect(createPGIS)
    conn.set_session(autocommit = True)
    cur = conn.cursor()

    try:
        cur.execute('CREATE EXTENSION postgis;')
        print("CREATED EXTENSION POSTGIS. Continuing...")
    except Exception:
        print("EXTENSION POSTGIS already exists. Continuing...")
        pass

    #cur.execute('SELECT st_centroid(geom) FROM counties')
    #print cur.fetchone()[0]
    conn.close()

if __name__ == "__main__":
    psqlInitialize()
