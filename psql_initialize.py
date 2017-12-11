#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import psycopg2 as pg2
import getpass

def include(script):
    if os.path.exists(script): 
        execfile(script)

def findShapefiles(args):
    filepath = []
    for filename in os.listdir(args):
        if filename.endswith(".shp"):
            shapefile = args + '/' + filename
            filepath.append(shapefile)
    return filepath

def psqlCredentials(args):
    print("Enter credentials needed to create the database")
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

    datapath = os.path.dirname(os.path.realpath( __file__ )) + "/data"
    shapefiles = []
    shapefiles = findShapefiles(datapath)

    print("The following shapefiles have been read from the working directory")
    try:
        for shape in shapefiles:
            print(shape)
        print("All shapefiles loaded. Continuing...\n")
    except:
        print("No shapefiles found. Continuing...\n")

    cred={}
    cred.update(psqlCredentials(cred))
    createdb = str("host='localhost' dbname='postgres' user='{user}' password='{passwd}'").format(**cred)
    print(createdb)

    initconn = pg2.connect(createdb)
    initconn.set_session(autocommit = True)
    setupcur = initconn.cursor()
    
    setupcur.execute(str('DROP DATABASE IF EXISTS {dbname};').format(**cred))

    try:
        setupcur.execute(str('CREATE DATABASE {dbname};').format(**cred))
        print (str("CREATED or REPLACED DATABASE {dbname}. Continuing...").format(**cred))
    except Exception:
        print(str("DATABASE {dname} already exists. Continuing...").format(**cred))
        pass
    initconn.close()

    createPGIS = "host='localhost' dbname='{dbname}' user='{user}' password='{passwd}'".format(**cred)
    print(createPGIS)
    conn = pg2.connect(createPGIS)
    conn.set_session(autocommit = True)
    cur = conn.cursor()

    try:
        cur.execute('CREATE EXTENSION postgis;')
        print("CREATED EXTENSION POSTGIS. Continuing...")
    except Exception:
        print("EXTENSION POSTGIS failed to build. Continuing...")
        pass

    #cur.execute('SELECT st_centroid(geom) FROM counties')
    #print cur.fetchone()[0]
    conn.close()

if __name__ == "__main__":
    psqlInitialize()
