#!/usr/bin/python


############################
#  TOP SEARCHES GENERATOR  #
############################


import pymysql
import cgi
import cgitb
import sys
import json
#import VHFqueries


cgitb.enable()

##----FUNCTIONS----##

def connect_db():
        #connect to database
        connection = pymysql.connect()
        #get cursor
        cursor = connection.cursor()

        return cursor, connection

def gene_check(cursor, top_hits_table, f):
        cursor.execute("""
        SELECT gene_name, search_count
        FROM top_hits
        ORDER BY search_count DESC
        LIMIT 10;
        """)
        rows = cursor.fetchall()

        #go through results of top 10 searches and write to file
        if rows:
                for row in rows:
                        #write file name
                        f.write(row[0])
                        f.write('\t')
                        #list search count
                        f.write(str(row[1]))
                        f.write('\n')
        return top_hits_table

def disconnect_db(cursor, connection):
        #close cursor and connection
        cursor.close()
        connection.close()

##----MAIN FUNCTION----##

#empty file
open('top_hits.txt', 'w').close()

#open writefile
f = open('top_hits.txt', 'w')

#connect to db
cursor, connection = connect_db()

#get top 10 hits as table
top_hits_table = []
top_hits_table = gene_check(cursor, top_hits_table, f)



#disconnect from db
disconnect_db(cursor,connection)
