#!/usr/bin/python

import pymysql
import cgi
import cgitb
import sys
import json
import math

cgitb.enable()

##----FUNCTIONS----##

#def connect_db():
        #connect to database
        #connection = pymysql.connect()
        #get cursor
        #cursor = connection.cursor()

        #return cursor, connection


##----MAIN CODE----##

#get data from client
form = cgi.FieldStorage()
#first form result
evirus = form.getvalue("evirus")
mvirus = form.getvalue("mvirus")
lvirus = form.getvalue("lvirus")


#get datatypes and make a list if any specified
datatype1 = form.getvalue("type1")
datatype2 = form.getvalue("type2")
datatype3 = form.getvalue("type3")
datatype = []

#if datatype1:
        #datatype.append(datatype1)

#if datatype2:
        #datatype.append(datatype2)

#if datatype3:
        #datatype.append(datatype3)

estrain = form.getvalue("estrain1")
lstrain = form.getvalue("lstrain")
mstrain = form.getvalue("mstrain")

#study = form.getvalue("studytype")
#genes = form.getvalue("genes")
#if genes:
        #split genes into a list
        #genelist = genes.split()


#check for ensemblIDs entered
#ensIDs = form.getvalue("ensemblID")
#if ensIDs:
        #split ensIDs into list
        #enslist = ensIDs.split()


#get the headers
print("Content-type: text/json")
print()
print()

print(json.dumps(evirus))



#all_results = []

#results will be a list of dictionaries (for each output type)
