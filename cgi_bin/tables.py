#!/usr/bin/python

import hashlib
import pymysql
import sys
import cgi
import cgitb
import json

cgitb.enable()

## FUNCTIONS ##
def connect_db():
        #connect to database
        connection = pymysql.connect()
        #get cursor
        cursor = connection.cursor()
        return cursor, connection

def disconnect_db(cursor, connection):
        #close cursor and connection
        cursor.close()
        connection.close()

def ask(cursor,query):
    cursor.execute(query)
    results = cursor.fetchall()
    return results


##----MAIN CODE----##

#we still need to set the headers
print("Content-type: text/javascript")
print()
##CALL ASK FUNCTION HERE with INPUTS##
cursor, connection = connect_db()
#define query
query = """
SELECT id,uName,pword,fName,lName,email, DATE_FORMAT(access_expir, '%m/%d/%Y') AS access_expir,Approval
FROM Users"""
#Obtain data from users table
results = ask(cursor,query)
print(json.dumps(results))
# print end_date
disconnect_db(cursor, connection)
