#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 23:04:20 2017
"""

def executeScriptsFromFile(filename):
    # Open and read the file as a single buffer
    infile = open(filename, 'r')
    sqlFile = infile.read()
    infile.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cur.execute(command)
        except Exception:
            print "Command skipped: ",
            
def listShapefiles(mypath, shapefiles):
    for filename in os.listdir(mypath):
        if filename.endswith(".shp"):
            filepath = mypath + '/' + filename
            shapefiles.append(filepath)
            

            