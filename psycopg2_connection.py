#!/usr/bin/python

"""
Example adapted from the official PostgreSQL Wiki
https://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL
"""

import psycopg2 as pg2
import pprint
import getpass

def psql_analysis(script):
    dbname = str(raw_input('Enter Database Name: '))
    user = str(raw_input('Enter Postgres Username: '))
    passwd = str(getpass.getpass('Enter Password: '))
    cred = ({
            "dbname": dbname,
            "user": user,
            "passwd": passwd
            }
    )

    conn_string = "host='localhost' dbname='%(dbname)s' user='%(user)s' password='%(passwd)s'" % (cred)
    # print the connection string we will use to connect
    print "Connecting to database\n	->%s" % (conn_string)
 
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = pg2.connect(conn_string)
 
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
 
    # execute Query
    try:
        cursor.execute(script)
    except ValueError:
        print("Script failed to run")
 
    # retrieve the records from the database
    try: 
        records = cursor.fetchone()
    except ValueError:
        print("No values to return")
    # print out the records using pretty print
    # note that the NAMES of the columns are not shown, instead just indexes.
    # for most people this isn't very useful so we'll show you how to return
    # columns as a dictionary (hash) in the next example.
    pprint.pprint(records)
 
    
    