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

def connect_db():
        # connect to database
        connection = pymysql.connect()
        # get cursor
        cursor = connection.cursor()

        return cursor, connection


def getGeneNames(query_where):

        results = []
        query_select_GO = "SELECT DISTINCT ensembl_MMU, ensembl_human, WikiGene_Name_MMU, WikiGene_Name_human, WikiGene_Description, GO_category, definition \
        FROM GENES inner join GO_TERM on ensembl_MMU = ensembl "

        query_select_NoGO = "SELECT DISTINCT ensembl_MMU, ensembl_human, WikiGene_Name_MMU, WikiGene_Name_human, WikiGene_Description, ' ' as Go_category, ' ' as definition\
        FROM GENES "

        query_groupby = " GROUP BY gene_id;"

        if "GO_category" in query_where:
                query = query_select_GO + query_where
        else:
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

form = cgi.FieldStorage()

# Initialize variables for storage
Category_dict = {}
convert_dict = {"HumangenePart": "WikiGene_Name_human", "MMUgenePart": "WikiGene_Name_MMU", "DescgenePart": "WikiGene_Description", "GOPart": "GO_category"}
bool_dict = {"AND": [" AND ", " LIKE "], "OR": [" OR ", " LIKE "], "NOT": [" AND ", " NOT LIKE "]}
query_where = ""

# Turn field storage into dictionary
for i in form.keys():
        Category_dict[i] = form.getlist(i)

# Parse Dictionary in SQL commands
for key in Category_dict:
        if re.match("^START\s", key):
                category = convert_dict[re.search("\w*$", key).group(0)]
                part = "\"%" + Category_dict[key][0] + "%\""
                query_where = "WHERE " + category + " LIKE " + part + query_where  # Prepend starting statement, when found # noqa
        for key2 in bool_dict:
                reg_term = "^" + key2 + "\s"
                if re.match(reg_term, key):
                        category = convert_dict[re.search("\w*$", key).group(0)]
                        for x in range(len(Category_dict[key])):
                                part = "\"%" + Category_dict[key][x] + "%\""
                                query_where += bool_dict[key2][0] + category + bool_dict[key2][1] + part




print("Content-type: text/json\n\n")
cursor, connection = connect_db()

results = getGeneNames(query_where)

print(json.dumps(results))
# print results

# disconnect from db
disconnect_db(cursor, connection)
