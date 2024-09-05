#!/usr/bin/python

import hashlib
import pymysql
import sys
import cgi
import cgitb
import json
import os
from subprocess import Popen, PIPE, STDOUT
import random
import string
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

def newpass(cursor,query):
    #change password
    cursor.execute(query)
    #commit changes
    connection.commit()

# shell execute PHP
def php(code):
    # open process
    p = Popen(['php'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, close_fds=True)

    # read output
    o = p.communicate(code.encode('utf-8'))[0]

    # kill process
    try:
        os.kill(p.pid, signal.SIGTERM)
    except:
        pass

    # return
    return o

def passgene():
    length = 13
    chars = string.ascii_letters + string.digits  # + '!@#$%^&*'
    random.seed = (os.urandom(1024))
    passw = ''.join(random.choice(chars) for i in range(length))
    return passw

##----MAIN CODE----##
#get data from html
form = cgi.FieldStorage()
data = form.getvalue("uname")

#we still need to set the headers
print("Content-type: text/javascript")
print()
##CALL INSERT LOGIN FUNCTION HERE with INPUTS##
if data is not None:
    cursor, connection = connect_db()

    #define update query base on if username or email
    if "@" in data and "." in data:
        query = """
            Select email, uName
            FROM Users
            WHERE email = %s;""" % ('\'' + data + '\'')
    else:
        query = """
            Select email, uName
            FROM Users
            WHERE uName = %s;""" % ('\'' + data + '\'')



    #Need to escape quotations because mysql is reading the variables in without the quotes
    cursor.execute(query)
    results = cursor.fetchall()
    if results == ():
        results = None
    elif results:
        email = results[0][0]
        username = results[0][1]
        # Get temporary random password
        password = passgene()

        # Hash password
        hashed = hashlib.md5(password.encode()).hexdigest()

        # Execute shell commands to run php email code
        code = """<?php

                $to = "{0}"; // this is your Email address
                $subject = "Hotresdb Password Reset";
                $message = "Your username is {2}\r\nYour temporary password is: {1} \r\nPlease go to http://10.231.6.30/VHFNewPassword.html to reset your password\r\nYour temporary password will expire in 1 day";
                $from = "pushkar@bu.edu";
                $headers = "From:" . $from;
                mail($to,$subject,$message,$headers);

                ?>
                """.format(email, password, username)
        res = php(code)

        # Set temporary password expiration
        pass_expir = date.today()
        pass_expir = str(pass_expir + timedelta(days=1))

        # define new password query
        query2 = """
            UPDATE Users
            SET pword = '{0}', pword_expir = '{2}'
            WHERE uName = '{1}';""".format(hashed, username, pass_expir)

        # set temporary password
        newpass(cursor, query2)

        #if res:
            #print(res)
    print(json.dumps(results))
    disconnect_db(cursor, connection)
