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

def admin_check(cursor,query):
    cursor.execute(query)
    results = cursor.fetchall()
    return results

##----MAIN CODE----##
#get data from html
form = cgi.FieldStorage()
username = form.getvalue("username")


#we still need to set the headers
print("Content-type: text/json")
print()
print()

#CALL INSERT LOGIN FUNCTION HERE with INPUTS##
if username is not None:
    cursor, connection = connect_db()

    #define update query
    query = """
    SELECT Admin
    FROM Users
    WHERE uName = %s;"""%('\''+username+'\'')

    results = admin_check(cursor,query)

    print(json.dumps(results))


    #disconnect from db
    disconnect_db(cursor,connection)


