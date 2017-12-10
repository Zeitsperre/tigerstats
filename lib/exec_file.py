#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Example adapted from @Azeirah (CC-BY-SA) 
https://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python
"""

def executeScriptsFromFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            con.cursor().execute(command)
        except OperationalError, msg:
            print "Command skipped: ", msg