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

def user_check(cursor,query): #Check if user already exists
    #insert entered registration information
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def insert_login(cursor,query):
    #insert entered registration information
    cursor.execute(query)
    #commit changes
    connection.commit()



##----MAIN CODE----##
#get data from html
form = cgi.FieldStorage()
username = form.getvalue("uname")
firstname = str(form.getvalue("fname"))
lastname = str(form.getvalue("lname"))
email = str(form.getvalue("email"))
s = form.getvalue("pword")

#we still need to set the headers
print("Content-type: text/javascript")
print()
##CALL INSERT LOGIN FUNCTION HERE with INPUTS##
if username is not None and s is not None:
    #hash password upon receipt
    password = hashlib.md5(s.encode()).hexdigest()
    cursor, connection = connect_db()
    #define query
    query = """
    SELECT *
    FROM Users
    WHERE uName = %sOR email = %s;"""%('\''+username+'\'','\''+email+'\'')

    #define Insert query
    query2 = """
    INSERT
    INTO Users (uName,pword,fName,lName,email,Approval)
    VALUES (%s,%s,%s,%s,%s,'Pending');"""%('\''+username+'\'','\''+password+'\'','\''+firstname+'\'','\''+lastname+'\'','\''+email+'\'')

    #Need to escape quotations because mysql is reading the variables in without the quotes
    results = user_check(cursor,query)  # Check if users credentials already exist
    # status = [x[2] for x in result] # check existing users
    if results == ():
        #insert data into users table
        insert_login(cursor,query2)
        disconnect_db(cursor, connection)
        print("Your Registration Request was Processed. We will be in contact shortly.")
    else:
        disconnect_db(cursor, connection)
        print("Your Username or Email is already registered")
else:
    print("Please Enter a Username and Password")
