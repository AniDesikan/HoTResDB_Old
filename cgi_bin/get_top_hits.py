#!/usr/bin/python


#######################
#    TOP SEARCHES     #
#######################


import pymysql
import cgi
import cgitb
import sys
import json



cgitb.enable()

##----FUNCTIONS----##

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

##----MAIN FUNCTION----##

#connect to db
cursor, connection = connect_db()

#get the headers
print("Content-type: text/json")
print()
print()

results_table = []
results_chart = []
results_categories = []
count = 0
cursor.execute("""
        SELECT gene_name, search_count
        FROM top_hits
        ORDER BY search_count DESC
        LIMIT 20;
        """)
rows = cursor.fetchall()
if rows:
        for row in rows:
                #new array for each row
                results_row = []
                results_row.append(row[0])
                results_row.append(row[1])
                results_table.append(results_row)

                results_chart_row = {'name': row[0], 'data': [{'x':count, 'y':row[1]}]}
                results_chart.append(results_chart_row)
                results_categories.append(row[0])
                count += 1

all_results_table=[]
all_results_chart = []
all_results_categories = []
all_count = 0
cursor.execute("""
        SELECT gene_name, search_count
        FROM top_hits
        ORDER BY search_count DESC;
        """)
rows = cursor.fetchall()
count2 = 0
if rows:
        for row in rows:
                #new array for each row
                results_row = []
                results_row.append(row[0])
                results_row.append(row[1])
                all_results_table.append(results_row)

                results_chart_row = {'name': row[0], 'data': [{'x':count2, 'y':row[1]}]}
                all_results_chart.append(results_chart_row)
                all_results_categories.append(row[0])
                count2 += 1

results = []
results.append(results_table)
results.append(results_chart)
results.append(results_categories)
results.append(all_results_table)
results.append(all_results_chart)
results.append(all_results_categories)
print(json.dumps(results))


#disconnect from db
disconnect_db(cursor,connection)

