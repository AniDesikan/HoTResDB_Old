#!/usr/bin/python

import pymysql
import cgi
import cgitb
import sys
import json
import math

cgitb.enable()

##----FUNCTIONS----##

def connect_db():
        #connect to database
        connection = pymysql.connect()
        #get cursor
        cursor = connection.cursor()

        return cursor, connection

def getGID(genelist):

        #initialize gene dictionary
        geneDict = {}

        #loop through list of genes and get gid for each
        for gene in genelist:

                #query databse for gid of genes
                cursor.execute("""
                    select GID
                    from GENES g
                    where WikiGene_Name_human LIKE %s
                """, (gene))

                #get the only the gid
                gid = cursor.fetchone()
                if gid:
                        #make gene name key and gid value
                        geneDict[gid[0]] = gene
        #for debugging####print json.dumps(geneDict)
        return geneDict

def ensembl2GID(enslist):
        #initialize list
        genelist = []
        #iterate through list
        for id in enslist:
                if "MMU" in id:
                        cursor.execute("""
                        SELECT WikiGene_Name, ensembl_human
                        FROM GENES
                        WHERE ensembl_MMU LIKE %s
                        """, (id))
                if "ENSG" in id:
                        cursor.execute("""
                        SELECT WikiGene_Name_MMU, ensembl_mmu
                        FROM GENES
                        WHERE ensembl_human LIKE %s
                        """, (id))
                name = cursor.fetchone()
                if name:
                        #get WikiGene_Name
                        genelist.append(name[0])
                        ##genelist.append(name[1])
        return genelist

def gene_summ(genes):
        gene_table = []
        for gene in genes:
                gname = genes[gene]
                item = []
                cursor.execute("""
                SELECT ensembl_human
                FROM GENES
                WHERE WikiGene_Name_human LIKE %s;
                """, (gname))
                row = cursor.fetchone()
                if row :
                        item = [row[0],gname]
                        gene_table.append(item)
                else:
                        item = ['N/A', gname]
                        gene_table.append(item)
        return gene_table

def getRange (geneDict,virus,strain,datatype):

        #This gets a list of the max DPI for each gene considering all factors. It will return a list of the range of values for DPI for CSV file
        maxlist = []
        for key in geneDict:
                gene = geneDict[key]
                gid = key
                cursor.execute("""
                SELECT max(DPI)
                FROM RNAseq JOIN SAMPLE ON SID=SID
                JOIN PATIENT using(PID)
                JOIN EXPERIMENT using(EID) 
                WHERE GID = %s AND VIRUS LIKE %s AND SEQUENCING_TYPE LIKE %s;
                """, (gid, virus, "%" + datatype + "%"))
                row = cursor.fetchone()
                if row:
                        #get maximum for particular gene
                        loc_max = row[0]
                        maxlist.append(loc_max)

        #get global maximum
        allmax = max(maxlist)
        print(json.dumps(allmax))

def countQuery_virus (geneDict,virus,strain,datatype):

        results = []

        for key in geneDict:

                #each row in the results will be an array
                gene = geneDict[key]
                gid = key
                cursor.execute("""
                SELECT DPI, avg(expression)
                FROM RNAseq JOIN SAMPLE ON SID=SID
                JOIN PATIENT using(PID)
                JOIN EXPERIMENT using(EID) 
                WHERE GID = %s AND VIRUS LIKE %s AND SEQUENCING_TYPE LIKE %s
                GROUP BY DPI
                ORDER BY DPI;""", (gid,virus,"%" + datatype + "%",))
                #get results
                rows = cursor.fetchall()

                temp = [gene, virus, strain, datatype]
                #exp_cond = rows[2]
                #add DPI and counts to JSON object
                DPI = []
                counts = []
                for row in rows:
                        DPI.append(row[0])
                        conv = int(row[1])
                        counts.append(conv)

                #add temporary array
                results.append(temp)


        #for debugging###print json.dumps(results)
        return results

def countQuery_strain (geneDict,strain,datatype):

        results = []

        #for key in geneDict:

                #initialize temporary dictionary with highcharts format
                #gene = geneDict[key]
                #gid = key
                #cursor.execute("""
                #SELECT DPI, avg(expression_level)
                #FROM gene_expression JOIN metadata ON sid=s_id
                #WHERE g_id = %s AND strain LIKE "%s"
                #GROUP BY DPI
                #ORDER BY DPI;"""%(gid,strain))
                #get results
                #rows = cursor.fetchall()

                #add DPI and counts to JSON object
                #DPI = []
                #counts = []
                #for row in rows:
                        #DPI.append(row[0])
                        #conv = int(row[1])
                        #counts.append(conv)


                #temp = {'name':gene, 'data':counts, 'DPI':DPI}
                #results.append(temp)


        #print json.dumps(geneDict)

def FCQUERY_virus (geneDict, virus, strain, datatype) :

        results = []

        for key in geneDict:

                gene = geneDict[key]
                gid = key
                cursor.execute("""
                SELECT DPI, avg(expression)
                FROM RNAseq JOIN SAMPLE ON SID=SID
                JOIN PATIENT using(PID)
                JOIN EXPERIMENT using(EID) 
                WHERE GID = %s AND VIRUS LIKE %s AND SEQUENCING_TYPE LIKE %s
                GROUP BY DPI
                ORDER BY DPI;
                """%(gid,virus,"%" + datatype + "%"))

                DPI_zero = cursor.fetchone()
                day_zero_exp = float(DPI_zero[1])

                #get experimental group
                #exp_cond = rows[2]

                rows = cursor.fetchall()
                FCs = []
                DPI = []
                for row in rows:
                        DPI.append(row[0])
                        current_exp = float(row[1])



                        FC = current_exp/day_zero_exp
                        #loggedFC = math.log(FC)/math.log(2)
                        loggedFC = str(FC)
                        FCs.append(loggedFC)

                temp = {'name':gene, 'data':FCs, 'DPI':DPI, 'type':virus}
                results.append(temp)

        #for debugging###print json.dumps(results)
        return results

def disconnect_db(cursor, connection):
        #close cursor and connection
        cursor.close()
        connection.close()

##----MAIN CODE----##

#get data from client
form = cgi.FieldStorage()
#first form result
evirus = form.getvalue("evirus")
mvirus = form.getvalue("mvirus")
lvirus = form.getvalue("lvirus")

datatype = form.getvalue("searchDataType")

estrain = form.getvalue("Estrain")
lstrain = form.getvalue("Lstrain")
mstrain = form.getvalue("Mstrain")

strain = ''
if estrain:
        strain = estrain
if mstrain:
        strain = mstrain
if mstrain:
        strain = mstrain

#study = form.getvalue("studytype")
genes = form.getvalue("genes")
if genes:
        #split genes into a list
        genelist = genes.split()


#check for ensemblIDs entered
ensIDs = form.getvalue("ensemblID")
if ensIDs:
        #split ensIDs into list
        enslist = ensIDs.split()


#get the headers
print("Content-type: text/json")
print()
print()





#connect to db
cursor, connection = connect_db()

#get wikigene names from converter
if ensIDs:
        ensGenes = ensembl2GID(enslist)
        #append all gene symbols together into one big list
        genelist = genelist + ensGenes


#get gIDs of results
geneDict = getGID(genelist)


#get summary information
gene_table = gene_summ(geneDict)

#get range of DPI
#getRange(geneDict, virus, strain, datatype)

#create table header


##count_results = []
#get counts of the queried genes if ebola
##if evirus:
        #if strain is specified
        #if strain:
        #       countQuery_strain(geneDict,estrain,datatype)
        #if strain not specified
        #else:
#       e_results = countQuery_virus(geneDict,evirus,strain,datatype)
        #add results to total count results
#       count_results.append(e_results)
#if marburg
##if mvirus:
#       m_results = countQuery_virus(geneDict,mvirus,strain,datatype)
        #add results to total count results
#       count_results.append(m_results)
#if lassa
##if lvirus:
#       l_results = countQuery_virus(geneDict,lvirus,strain,datatype)
        #add results to total count results
#       count_results.append(l_results)



##FC_results = []

#get fold changes of the queried genes for each virus type
##if evirus:
#       e_fc_results = FCQUERY_virus(geneDict,evirus,strain,datatype)
#       FC_results.append(e_fc_results)
##if mvirus:
#       m_fc_results = FCQUERY_virus(geneDict,mvirus,strain,datatype)
#       FC_results.append(m_fc_results)
#if lvirus:
        #l_fc_results = FCQUERY_virus(geneDict,lvirus,strain,datatype)
        #FC_results.append(l_fc_results)



###all_results = []
###all_results.append(gene_table)
###all_results.append(count_results)
###all_results.append(FC_results)

#results will be a list of dictionaries (for each output type)

#FINALPRINT#####print json.dumps(all_results)


#disconnect from db
disconnect_db(cursor,connection)
