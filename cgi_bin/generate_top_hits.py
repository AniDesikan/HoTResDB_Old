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


def insert_gene(cursor,gene):
        cursor.execute("""
        INSERT INTO top_hits (gene_name,search_count)
        VALUES (%s, 1);
        """, (gene,))

def increment_count(cursor,gene):
        cursor.execute("""
        UPDATE top_hits
        SET search_count = search_count + 1
        WHERE gene_name LIKE %s;
        """, (gene,))

def gene_check(cursor, gene, connection):
        cursor.execute("""
        SELECT *
        FROM top_hits
        WHERE gene_name LIKE %s;
        """, (gene,))
        result = cursor.fetchall()
        if result:
                increment_count(cursor,gene)
        else:
                insert_gene(cursor,gene)
                connection.commit()


def disconnect_db(cursor, connection):
        #close cursor and connection
        cursor.close()
        connection.close()

##----MAIN FUNCTION----##
def main(gene_array):

        #connect to db
        cursor, connection = connect_db()

        for gene in gene_array:
                #capitalize all genes in array
                gene.upper()
                gene_check(cursor,gene,connection)

        #disconnect from db
        disconnect_db(cursor,connection)


