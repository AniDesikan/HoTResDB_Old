#!/usr/bin/python3

import pymysql
import cgi
import cgitb
import sys
import json
import os
import re

cgitb.enable()

# #----FUNCTIONS----# #


# def log(output, header="", buffer=True, fname="/home/students_24/adesikan/python_log.txt"):
#         """
#         # PURPOSE: to make it easier to send to the log file
#         #
#         # INPUT:
#         # output - What information do you want to send to the log?
#         #                  Can be any variable that can be converted to a string using str().
#         # header - What do you want to say about this piece of information. Can be left empty.
#         # buffer - If True, then the output is buffered by the default settings.
#         #                  If False, you have to format the text yourself, and will only write output and header to file.
#         # fname  - Where should the stuff be written
#         """
#         f=open(fname,"a+")
#         f.write(header + ("\n\t" if buffer else ""))
#         f.write(str(output))
#         f.write("\n" if buffer else "")
#         f.close()


def connect_db():
        # connect to database
        connection = pymysql.connect()
        # get cursor
        cursor = connection.cursor()
        return cursor, connection


def getStudyNames(query_where):

        results = []

        query_select_NoGO = "SELECT DISTINCT STUDY_NAME as Study, VIRUS as Virus, STRAIN as Strain, SPECIES as Species, TISSUE_TYPE as Tissue, EXPOSURE_ROUTE as Exposure, SEQUENCING_TYPE as DataType, PMID as PUBMED\
        FROM EXPERIMENT LEFT JOIN PUBLICATION using(PUBID)"

        query = query_select_NoGO + query_where

        cursor.execute(query)
        results = cursor.fetchall()

        return results
        # return query


def disconnect_db(cursor, connection):
        # close cursor and connection
        cursor.close()
        connection.close()

# #----MAIN CODE----# #

# get data from client
form = cgi.FieldStorage()

# Initialize variables for storage
Category_dict = {}
convert_dict = {"HumangenePart": "WikiGene_Name_human", "MMUgenePart": "WikiGene_Name_MMU", "DescgenePart": "WikiGene_Description", "GOPart": "GO_category"}
bool_dict = {"AND": [" AND ", " LIKE "], "OR": [" OR ", " LIKE "], "NOT": [" AND ", " NOT LIKE "]}
query_where = "WHERE "

# Turn field storage into dictionary
for i in form.keys():
        Category_dict[i] = form.getlist(i)
        if form.getlist(i)[0] != "All":
                if len(query_where) != 6:
                        query_where = query_where + " AND "
                query_where = query_where + str(i) + ' = ' + '"' + str(form.getlist(i)[0]) + '"'
if len(query_where) == 6:
        query_where = ""

# get the headers
print("Content-Type: text/json\n\n")

cursor, connection = connect_db()

exclude_template="""
SELECT DISTINCT EID
FROM PATIENT JOIN SAMPLE using (PID) JOIN %s using (SID)
"""

# edit this when you add in NANOSTRING data
datatypes = ["RNAseq", "RNAseq_bomv_tafv", "MICROARRAY"]

exclude_query="UNION".join([exclude_template % dt for dt in datatypes])

# get only things where data exists
if query_where == "":
        query_where = " WHERE EID in (" + exclude_query + ");"
else:
        query_where = query_where + " AND EID in (" + exclude_query + ");"

results = getStudyNames(query_where)

#log("end_of_sample search")

# print results
print(json.dumps(results))


# disconnect from db
disconnect_db(cursor, connection)
