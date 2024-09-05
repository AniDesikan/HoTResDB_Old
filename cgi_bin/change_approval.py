#!/usr/bin/python

import hashlib
import pymysql
import sys
import cgi
import cgitb
import json
from datetime import datetime
from datetime import date
from datetime import timedelta

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

# def user_check(cursor,query): #Check if user already exists
#     #insert entered registration information
#     cursor.execute(query)
#     results = cursor.fetchall()
#     return results

def approval(cursor,query):
    #change approval
    cursor.execute(query)
    #commit changes
    connection.commit()



##----MAIN CODE----##
#get data from html
form = cgi.FieldStorage()
id_num = form.getvalue("id")
appr = form.getvalue("approval")
end_date = form.getvalue("expir")

# if "-" in end_date:
#     end_date = datetime.strptime(end_date, '%Y-%m-%d')
#     end_date = str(end_date.strftime("%Y-%m-%d"))
if appr == "Yes" or appr == "Pending":
    if end_date == "null" or end_date == "01/01/1999":
        end_date = date.today()
        end_date = str(end_date + timedelta(days=30))
    else:
        end_date = datetime.strptime(end_date, '%m/%d/%Y')
        end_date = str(end_date.strftime("%Y-%m-%d"))

else:
    end_date = "1999-01-01"

#we still need to set the headers
print("Content-type: text/javascript")
print()
##CALL INSERT LOGIN FUNCTION HERE with INPUTS##
if appr is not None and id is not None:
    cursor, connection = connect_db()

    #define update query
    query = """
    UPDATE Users
    SET Approval = '{0}', access_expir = '{1}', pword_expir = '{1}'
    WHERE id = '{2}';""".format(appr, end_date, id_num)

    #Need to escape quotations because mysql is reading the variables in without the quotes
    #update data in users table
    approval(cursor,query)
    disconnect_db(cursor, connection)
