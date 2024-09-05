#!/usr/bin/env python3
import cgi

#the next two lines are useful for debugging
#they cause errors during execution to be sent back to the browser
import cgitb
cgitb.enable()

#the next line gives us a convenient way to insert values into strings
from string import Template

import pymysql
import sys
import json
import math

### IMPORT HEATMAP CLUSTER BREAKS BIOED, PROBABLY IMPORTS THE OTHER PY FILE
# import heatmap_cluster
import copy
from operator import itemgetter

def connect_db():
        # PURPOSE: connect to database
        connection = pymysql.connect()
        cursor = connection.cursor()

        return cursor, connection


def disconnect_db(cursor, connection):
        # PURPOSE: close cursor and connection
        cursor.close()
        connection.close()

def getGID(genelist, not_in_db):
        """
        # PURPOSE: Get unique integer GIDs for each gene in genelist
        #
        # INPUTS:
        # genelist      - list of gene symbols or ensembl ids. Can be mixed
        # not_in_db - running total of things not found in the database
        #
        # OUTPUT:
        # geneDict      - Dictionary of gene symbols where {gid: ensembl or symbol}
        """
        geneDict = {}
        #loop through list of genes and get gid for each
        for gene in genelist:
                cursor.execute("""
                SELECT GID
                FROM GENES
                WHERE ensembl_human LIKE %s OR ensembl_MMU LIKE %s OR WikiGene_Name_human LIKE %s OR WikiGene_Name_MMU LIKE %s;
                """, (gene, gene, gene, gene))
                rows = cursor.fetchall()
                if rows:
                        for row in rows:
                                # make gid key and gene name value
                                # {gid : ensembl or symbol}
                                geneDict[row[0]] = gene
                else:
                        not_in_db.append([gene, " Gene not in database"])
        return geneDict

def gene_summ(geneDict):
        """
        # PURPOSE: To create the results table with Ensembl Human ID or Wikigene Symbol.
        #                  Other columns are appended on javascript side
        #
        # INPUTS:
        # geneDict       - Dictionary of gene symbols where {gid: ensembl or symbol}
        #
        # OUTPUT:
        # gene_table - 5-column table with GID, the gene symbol and the ensembl id for both human and macaque
        """
        gene_table = []

        #Get the gene id for each
        for gid in geneDict:
                cursor.execute("""
                        SELECT GID, ensembl_human, WikiGene_Name_human, ensembl_MMU, WikiGene_Name_MMU
                        FROM GENES
                        WHERE GID = %s;
                """, [gid])
                rows = cursor.fetchone()
                if rows:
                        gene_table.append(rows)

        return gene_table


def getStrain(samples):
        """
        # PURPOSE: Data tables in user-side results requires DPI appended based on studies searched.
        #         They don't all have the same DPI, so this will check for the maximum DPI value and
        #                 create an array to be appended to the table on HTML side
        #
        # INPUTS:
        # samples - list of dataset names
        #
        # OUTPUTS:
        # strains - list of distinct strains
        """
        strains = []
        for skey in samples:
                sample = samples[skey]
                samplename = skey
                cursor.execute("""
                SELECT DISTINCT STRAIN
                FROM EXPERIMENT
                WHERE STUDY_NAME = %s;
                """, [sample])
                for row in cursor:
                        strains.append(row)
        straintemp = set(strains)
        strains = list(straintemp)
        return strains


def getDatatypes(samples):
        #PURPOSE: Data tables in user-side results requires DPI appended based on studies searched. They don't all have the same DPI, so this will check for the maximum DPI value and create an array to be appended to the table on HTML side
        #INPUTS:
        datatypes = []
        # log("datatypes and studies")
        for skey in samples:
                # log("\t" + str(skey) + "\n", buffer=False)
                sample = samples[skey]
                samplename = skey
                cursor.execute("""
                SELECT DISTINCT SEQUENCING_TYPE
                FROM EXPERIMENT
                WHERE STUDY_NAME = %s;
                """, [samplename])
                for row in cursor:
                        # log("\t\t" + str(row[0]) + "\n", buffer=False)
                        datatypes.append(row[0])
        datatypes = list(set(datatypes))
        return datatypes


def createSampledict(samplelist, not_in_db):
        # TODO: Figure out if it's useful
        # PURPOSE:
        # INPUTS:
        # samplelist - list of studies we'll be looking at
        # not_in_db - list of search terms not in the database.
        #                        This passes through this function and any additional genes not found are appended into this list.
        #                        These may be genes in the converter but not the database.
        sampledict = {}
        row_check = True
        for sample in samplelist:
                cursor.execute("""
                SELECT DISTINCT STUDY_NAME
                FROM EXPERIMENT
                WHERE STUDY_NAME LIKE %s AND EID in (SELECT DISTINCT EID FROM PATIENT);
                """, [sample])
                rows = cursor.fetchall()


                if rows:
                        for row in rows:
                                samplesample = row[0]
                                key = sample
                                if key not in sampledict:
                                        sampledict[key] = []
                                sampledict[key].append(samplesample)

                else:
                        not_in_db.append([sample, ' Study not found'])

        return sampledict


def getMaxDPI(samples, s_status):
        #PURPOSE: Data tables in user-side results requires DPI appended based on studies searched. They don't all have the same DPI, so this will check for the maximum DPI value and create an array to be appended to the table on HTML side
        #INPUTS:
        maxDPI = 0
        for samplename in samples:
                # survival = "" if s_status else "AND survival LIKE \"died\""
                if s_status:
                        cursor.execute("""
                        SELECT max(DPI)
                        FROM PATIENT JOIN SAMPLE using (PID) JOIN EXPERIMENT using(EID)
                        WHERE STUDY_NAME = %s;
                        """, [samplename])
                else:
                        cursor.execute("""
                        SELECT max(DPI)
                        FROM PATIENT JOIN SAMPLE using (PID) JOIN EXPERIMENT using(EID)
                        WHERE STUDY_NAME = %s AND survival LIKE \"died\";
                        """, [samplename])

                row = cursor.fetchone()
                if row[0] > maxDPI:
                        maxDPI = row[0]
        # DPI_list = [n for n in range(-8, maxDPI + 1)]
        DPI_list = [n for n in range(maxDPI + 1)]
        return DPI_list

# ##########################
# ## II. RNASEQ FUNCTIONS ##
# ##########################

def count_boxplot_virus(geneDict, DPI_list, studies, noresults, s_status):
        """
        # PURPOSE: To get the counts data for RNASeq studies in JSON and table formats for boxplots
        #
        # INPUTS:
        # geneDict      - Dictionary of gene symbols, {gid: ensembl or symbol}
        # DPI_list      - list of days you want to look at
        # studies       - list of studies you want to look at
        # noresults     - list of genes without data
        # s_status      - survival status, true = survive or delayed, false = died
        #
        # OUTPUTS:
        # results       - table for boxplots with dictionaries of gene, study info, log CPM adn DPI
        """
        seq_format = "RNAseq"
        results = []

        for key in geneDict:
                #initialize temporary dictionary with highcharts format
                gene = geneDict[key]
                gid = key
                for study in studies:
                        # survival = "" if s_status else "AND survival LIKE \"died\""
                        #FROM GENES g JOIN RNAseq on RNAseq.ensembl=g.ensembl_MMU JOIN SAMPLE USING (sid) JOIN PATIENT USING (pid) JOIN EXPERIMENT USING (EID)
                        if s_status:
                                cursor.execute("""
                                SELECT DPI, expression, virus
                                FROM GENES JOIN RNAseq r using(GID) JOIN SAMPLE USING (SID) JOIN PATIENT USING (pid) JOIN EXPERIMENT USING (EID)
                                WHERE gid = %s AND Study_Name LIKE %s  and DPI >= 0
                                UNION
                                SELECT DPI, expression, virus
                                FROM GENES JOIN RNAseq_bomv_tafv using(GID) JOIN SAMPLE USING (SID) JOIN PATIENT USING (PID) JOIN EXPERIMENT USING (EID)
                                WHERE gid = %s AND Study_Name LIKE %s  and DPI >= 0
                                ORDER BY DPI;""", [gid, "%" + seq_format + "%", "%" + study + "%",  gid, "%" + seq_format + "%", "%" + study + "%"])
                        else:
                                cursor.execute("""
                                SELECT DPI, expression, virus
                                FROM GENES JOIN RNAseq r using(GID) JOIN SAMPLE USING (SID) JOIN PATIENT USING (pid) JOIN EXPERIMENT USING (EID)
                                WHERE gid = %s AND Study_Name LIKE %s AND survival LIKE \"died\" and DPI >= 0
                                UNION
                                SELECT DPI, expression, virus
                                FROM GENES JOIN RNAseq_bomv_tafv using(GID) JOIN SAMPLE USING (SID) JOIN PATIENT USING (PID) JOIN EXPERIMENT USING (EID)
                                WHERE gid = %s AND Study_Name LIKE %s AND survival LIKE \"died\" and DPI >= 0
                                ORDER BY DPI;""", [gid, "%" + seq_format + "%", "%" + study + "%",  gid, "%" + seq_format + "%", "%" + study + "%"])

                        #get results
                        rows = cursor.fetchall()

                        if rows:
                                for row in rows:
                                        conv = float(row[1])
                                        if conv != 0:
                                                logconv = math.log(conv, 2)  # toggle this
                                        else:
                                                logconv = 0
                                        temp = {'gene': gene, 'study': study, 'data': logconv, 'DPI': row[0]}
                                        results.append(temp)
                        if not cursor.rowcount:
                                noName = gene + '_' + study
                                if noName not in noresults:
                                        noresults.append(noName)
        # Re-order results by DPI
        results = sorted(results, key=itemgetter('DPI'))
        return results


def countQuery_virus(geneDict, DPI_list, studies, noresults, s_status):
        """
        # PURPOSE: To get the counts data for RNASeq studies in JSON and table formats
        #
        # INPUTS:
        # geneDict      - Dictionary of gene symbols, {gid: ensembl or symbol}
        # DPI_list      - list of days you want to look at
        # studies       - list of studies you want to look at
        # noresults     - list of genes without data
        # s_status      - survival status, true = include survive or delayed, false = only died
        #
        # OUTPUTS:
        # results       - table for output visualization
        # table         - table for output
        # noresults     - list of things without data
        #
        #OVERVIEW of Steps:
        # - Query for:
        #               average expression level at each DPI
        #               standard deviation of that expression level at each DPI
        #               number of different expression levels for that DPI for later calculations based on study, sequencing type, and gid for each (survival if applicable) --- huh???
        # - Initialize DPI at 0 in order to place studies in standard format
        # - If there are results, start adding data (skipping DPI indexes where there is no data for that particular search)
        # - For error bars, calculate standard error based on the standard deviation and the square root of counts for each DPI. Refer to Google for standard error formula
        # - Perform LOG2 standardization on both the counts and the standard error. Log of 0 is undefined, but 0 values are given instead to show that tests were done at that DPI but no counts were obtained.
        # - append data to highcharts JSON object and table for each DPI found for highcharts visualization -- line charts
        """
        seq_format = "RNAseq"
        results = []
        table = []

        for key in geneDict:
                #initialize temporary dictionary with highcharts format
                gene = geneDict[key]
                gid = key
                for study in studies:
                        # survival = "" if s_status else "AND survival LIKE \"died\""
                        if s_status:
                                cursor.execute("""
                                SELECT DPI, avg(expression), virus, std(expression), count(expression), strain
                                FROM GENES JOIN RNAseq using(gid) JOIN SAMPLE USING (sid) JOIN PATIENT USING (pid) JOIN EXPERIMENT USING (EID)
                                WHERE gid = %s AND Study_Name LIKE %s and DPI >= 0
                                GROUP BY DPI, virus, strain
                                UNION
                                SELECT DPI, avg(expression), virus, std(expression), count(expression), strain
                                FROM GENES JOIN RNAseq_bomv_tafv using(gid) JOIN SAMPLE USING (sid) JOIN PATIENT USING (pid) JOIN EXPERIMENT USING (EID)
                                WHERE gid = %s AND Study_Name LIKE %s and DPI >= 0
                                GROUP BY DPI, virus, strain
                                ORDER BY DPI;""", [gid, "%" + study + "%", gid, "%" + study + "%"])
                        else:
                                cursor.execute("""
                                SELECT DPI, avg(expression), virus, std(expression), count(expression), strain
                                FROM GENES JOIN RNAseq using(gid) JOIN SAMPLE USING (sid) JOIN PATIENT USING (pid) JOIN EXPERIMENT USING (EID)
                                WHERE gid = %s AND Study_Name LIKE %s AND DPI >= 0 
                                GROUP BY DPI, virus, strain
                                UNION
                                SELECT DPI, avg(expression), virus, std(expression), count(expression), strain
                                FROM GENES JOIN RNAseq_bomv_tafv using(gid) JOIN SAMPLE USING (sid) JOIN PATIENT USING (pid) JOIN EXPERIMENT USING (EID)
                                WHERE gid = %s AND Study_Name LIKE %s  AND DPI >= 0 
                                GROUP BY DPI, virus, strain
                                ORDER BY DPI;""", [gid, "%" + study + "%", gid, "%" + study + "%"])
                        #get results
                        rows = cursor.fetchall()
                        #increment DPI in DPI list and add counts to JSON object
                        # DPI = -9
                        DPI = 0
                        counts = []
                        countserror = []

                        if rows:
                                for row in rows:
                                        # This loop accounts for missing data for each day,
                                        # simply moving onto the next day that does have data
                                        while DPI_list[DPI] != row[0]: # consider changing to just `DPI != row[0]`
                                                counts.append(None)
                                                countserror.append(None)
                                                DPI += 1
                                        conv = float(row[1])

                                        #GET SE
                                        sd = float(row[3])
                                        n = float(row[4])
                                        nsq = math.sqrt(n)
                                        logmin = 0
                                        logmax = 0
                                        if sd != 0:
                                                se = sd/nsq
                                                minimum = conv - se
                                                logmin = math.log(minimum,2)
                                                maximum = conv + se
                                                logmax = math.log(maximum,2)
                                        errorbar = []
                                        logconv = 0
                                        if conv != 0:
                                                logconv = math.log(conv, 2)
                                        counts.append(logconv)
                                        errorbar.append(logmin)
                                        errorbar.append(logmax)
                                        countserror.append(errorbar)

                                        DPI +=1
                                        virus = row[2]
                                        strain = row[5]

                                if len(counts) > 0:
                                        temp = {'name':gene + '_' + study + '_' + seq_format + ('_SURVIVORS' if s_status else ''),
                                                        'data':counts}
                                        results.append(temp)
                                        temperror = {'name':gene + '_' + study + '_' + seq_format + '_error'  + ('_SURVIVORS' if s_status else ''),
                                                                 'type':'errorbar',
                                                                 'data':countserror}
                                        results.append(temperror)
                                        tblrow = [gene, virus, seq_format, strain, study]
                                        tblrowfull = tblrow + counts
                                        table.append(tblrowfull)
                        if not cursor.rowcount:
                                noName = gene + '_' + study
                                if noName not in noresults:
                                        noresults.append(noName)

        return results, table, noresults


def FCQUERY_virus (geneDict, DPI_list, studies, s_status, hm_x_axis):
        """
        # PURPOSE: To get the fold change data for RNASeq studies in JSON and table formats
        # Note: There are different versions of MySQL query due to the differences in metadata table format between studies
        # OVERVIEW of Steps:
        # - Query for average expression level at each DPI, for later calculations based on study, sequencing type, and gid for each (survival if applicable)
        # - Initialize DPI at 0 in order to place studies in standard format
        # - Get and store the day 0 counts for each search in order to calculate fold change
        # - If there are results, calculate fold change by dividing at that DPI by day 0 and then getting log2 of fold change for standardization.
        # - start adding data (skipping DPI indexes where there is no data for that particular search)
        # - Store data in matrix format for heat map
        # - Create heat map X axis to be clustered in later functions
        # - append data to highcharts JSON object and table for each DPI found
        # PS: Refer to highcharts website for the format of error bars and line chart
        #
        # INPUTS:
        # geneDict - DICTIONARY of gene symbols, {gid: ensembl or symbol}
        # DPI_list - ARRAY of DPI from 0 to maxDPI of all studies in search
        # studies - ARRAY of all studies that match search parameters
        # s_status - BOOLEAN. True if user chose to view survivor data
        # hm_x_axis - ARRAY of study + DPI terms to be used in heat map x axis.
        #                         Since this function is RNAseq-specific, need to pass this
        #                         variable through each fold change function for each datatype
        #                         to get all study + DPI combinations
        #
        # OUTPUTS:
        # results - results formatted into JSON objects for HighCharts
        # table - results formatted in 2D-ARRAY format for data table
        # heat_map_sortedby_study -
        # heat_map_cats_sortedby_study - No idea why it is named cats... it's first value holds all the genes
        # hm_x_axis - the updated heat map x axis
        """
        results = []
        table = []
        seq_format = "RNAseq"

        #initialize heat map data
        #initialize temporary dictionary with highcharts format
        heat_map_sortedby_study = []
        heat_map_cats_sortedby_study = []
        DPI_heat_map_cats = []
        heatmap_y = 0
        for key in geneDict:
                gene = geneDict[key]
                #add category to heat map data and initialize list for specific row
                #it is made unique at the end
                DPI_heat_map_cats.append(gene)

        for study in studies:
                #reinitialize DPI heat map data per study
                DPI_heat_map = []
                DPI_heat_map_survivors = [] #for data structure organization
                hmlogic = False
                s_options = [" AND survival LIKE \"died\""]
                if s_status:
                        s_options.append(" AND (survival LIKE \"survived\" OR survival LIKE \"delayed\")")
                for survival in s_options:
                        for key in geneDict:
                                gene = geneDict[key]
                                gid = key
                                DPI_heat_map_row = []
                                DPI_heat_map_survivors_row = []
                                if survival == " AND survival LIKE \"died\"":
                                        cursor.execute("""
                                                SELECT DPI, avg(expression), virus, strain
                                                FROM GENES JOIN RNAseq using(gid) JOIN SAMPLE USING (sid) JOIN PATIENT USING (pid) JOIN EXPERIMENT USING (EID)
                                                WHERE gid = %s AND Study_Name LIKE %s and DPI >= 0 AND survival LIKE \"died\"
                                                GROUP BY DPI,virus, strain
                                                UNION
                                                SELECT DPI, avg(expression), virus, strain
                                                FROM GENES JOIN RNAseq_bomv_tafv using(gid) JOIN SAMPLE USING (sid) JOIN PATIENT USING (pid) JOIN EXPERIMENT USING (EID)
                                                WHERE gid = %s AND Study_Name LIKE %s and DPI >= 0 AND survival LIKE \"died\"
                                                GROUP BY DPI, virus, strain
                                                ORDER BY DPI;""", [gid, "%" + study + "%", gid, "%" + study + "%",])
                                else:
                                        cursor.execute("""
                                                SELECT DPI, avg(expression), virus, strain
                                                FROM GENES JOIN RNAseq using(gid) JOIN SAMPLE USING (sid) JOIN PATIENT USING (pid) JOIN EXPERIMENT USING (EID)
                                                WHERE gid = %s AND Study_Name LIKE %s and DPI >= 0 AND (survival LIKE \"survived\" OR survival LIKE \"delayed\")
                                                GROUP BY DPI,virus, strain
                                                UNION
                                                SELECT DPI, avg(expression), virus, strain
                                                FROM GENES JOIN RNAseq_bomv_tafv using(gid) JOIN SAMPLE USING (sid) JOIN PATIENT USING (pid) JOIN EXPERIMENT USING (EID)
                                                WHERE gid = %s AND Study_Name LIKE %s and DPI >= 0 AND (survival LIKE \"survived\" OR survival LIKE \"delayed\")
                                                GROUP BY DPI, virus, strain
                                                ORDER BY DPI;""", [gid, "%" + study + "%", gid, "%" + study + "%"])
                                #get results
                                FCs = []
                                DPI = 0
                                heatmap_x = 0
                                day_zero_exp = 0
                                found_day_zero = False

                                rows = cursor.fetchall()
                                for row in rows:
                                        if row[0] < 0:
                                                continue
                                        if row[0] == 0:
                                                day_zero_exp = float(row[1])
                                                heatmap_y += 1
                                                found_day_zero = True
                                        elif not found_day_zero:
                                                while DPI_list[DPI] != row[0]:
                                                        FCs.append(None)
                                                        DPI += 1
                                                if DPI_list[DPI] == row[0]:
                                                        day_zero_exp = float(row[1])
                                                        heatmap_y += 1
                                                        found_day_zero = True
                                        while DPI_list[DPI] != row[0]:
                                                FCs.append(None)
                                                DPI+=1
                                        current_exp = float(row[1])
                                        loggedFC = 0
                                        if current_exp != 0 and day_zero_exp != 0:
                                                FC = current_exp/day_zero_exp
                                                loggedFC = math.log(FC,2)
                                        FCs.append(loggedFC)
                                        study_plus_dpi = study + ('_survivors_' if (survival != s_options[0]) else "") + "_day_" + str(DPI)
                                        temp2 = [heatmap_x,heatmap_y,loggedFC, study_plus_dpi, gene]
                                        if survival == s_options[0]:
                                                DPI_heat_map_row.append(temp2)
                                        else:
                                                DPI_heat_map_survivors_row.append(temp2)
                                        if study_plus_dpi not in hm_x_axis:
                                                hm_x_axis.append(study_plus_dpi)
                                        heatmap_x += 1
                                        DPI += 1
                                        virus = row[2]
                                        strain = row[3]
                                        hmlogic = True  # There were genes, so append to heat map. Remains false if no genes

                                if len(FCs) > 0:
                                        temp = {'name':gene + '_' + study, 'data':FCs}
                                        results.append(temp)
                                        tblrow = [gene, virus, seq_format, strain, study]
                                        tblrowfull = tblrow + FCs
                                        table.append(tblrowfull)
                                if DPI_heat_map_row:
                                        DPI_heat_map += DPI_heat_map_row
                                if DPI_heat_map_survivors_row:
                                        DPI_heat_map_survivors += DPI_heat_map_survivors_row


                        #increment y for heatmap
                        heatmap_y+=1
                if hmlogic is True:
                        heat_map_sortedby_study.append(DPI_heat_map)
                        heat_map_sortedby_study.append(DPI_heat_map_survivors)

        heat_map_cats_sortedby_study.append(DPI_heat_map_cats)

        return results, table, heat_map_sortedby_study, heat_map_cats_sortedby_study, hm_x_axis

# ###############################
# ## III. MICROARRAY FUNCTIONS ##
# ###############################

def count_boxplot_microarray_virus(geneDict, noresults): # studies
        """
        # PURPOSE: To get the counts data for Microarray studies in JSON and table formats for boxplots
        #
        # INPUTS:
        # geneDict      - Dictionary of gene symbols, {gid: ensembl or symbol}
        # DPI_list      - list of days you want to look at
        # studies       - list of studies you want to look at
        # noresults     - list of genes without data
        # s_status      - survival status, true = survive or delayed, false = died
        #
        # OUTPUTS:
        # results       - table for boxplots with dictionaries of gene, study info, log CPM adn DPI
        """
        seq_format = "Microarray"
        results = []

        for gid in geneDict:
                #initialize temporary dictionary with highcharts format
                gene = geneDict[gid]

                cursor.execute("""
                SELECT DPI, expression, STUDY_NAME
                from GENE2PROBE JOIN MICROARRAY USING (probe_id) join SAMPLE USING (SID) JOIN PATIENT USING (PID) JOIN EXPERIMENT USING (EID)
                where gid = %s AND Sequencing_type LIKE "%s" and DPI >= 0
                ORDER BY DPI;"""%(gid, seq_format))
                # cursor.execute("""
                # SELECT DPI, expression, STUDY_NAME
                # from GENE2PROBE JOIN MICROARRAY USING (probe_id) join SAMPLE USING (SID) JOIN PATIENT USING (PID) JOIN EXPERIMENT USING (EID)
                # where gid = %s AND Sequencing_type LIKE "%s" and DPI >= 0
                # ORDER BY DPI;""", [gid, seq_format])

                #get results
                rows = cursor.fetchall()
                if rows:
                        for row in rows:
                                if row[1]:
                                        conv = float(row[1])
                                        temp = {'gene': gene, 'study': row[2], 'data': conv, 'DPI': row[0]}
                                        results.append(temp)
        # Re-order results by DPI
        results = sorted(results, key=itemgetter('DPI'))
        return results


def get_Probe_IDs(geneDict, not_in_db):
        """
        # PURPOSE: Microarray data organized by probe ID. Need to get the Probes for each MMU ID for later searches to minimize JOINs
        #
        # INPUT
        # geneDict  - DICTIONARY of gene symbols, {gid: ensembl or symbol}
        # not_in_db - Running total of gids not found in the database
        #
        # OUTPUT
        # ProbeDict - DICTIONARY of probes, {gid: [probe_id1, probe_id2, probe_id3, ...]}
        """
        ProbeDict = {}
        for gid in geneDict:
                #go through gene list and find the probes for each gene
                cursor.execute("""
                SELECT Probe_ID
                FROM GENES JOIN GENE2PROBE using (GID)
                WHERE GID = %s;
                """ % (gid))
                # cursor.execute("""
                # SELECT Probe_ID
                # FROM GENES JOIN GENE2PROBE using (GID)
                # WHERE GID = %s;
                # """ , [gid])

                rows = cursor.fetchall()
                # make a dict where {gid: [probe names]}
                if rows:
                        for row in rows:
                                probe = row[0]
                                if gid not in ProbeDict:
                                        ProbeDict[gid] = []
                                ProbeDict[gid].append(probe)
                else:
                        not_in_db.append([geneDict[gid], " Probes not in database."])

        return ProbeDict


def microarray_countQuery_virus (ProbeDict, geneDict, DPI_list, studies, noresults, s_status):
        """
        # PURPOSE: Microarray counts data
        # INPUT
        # ProbeDict - DICTIONARY of probes, {gid: [probe_id1, probe_id2, probe_id3, ...]}
        # DPI_list      - list of days you want to look at
        # studies       - list of studies you want to look at
        # noresults     - list of genes without data
        # s_status      - survival status, true = include survive or delayed, false = only died
        # OUTPUT
        # results - counts
        # table   - counts, but with error bars
        # Note: refer to previous RNASeq pipeline for specific steps
        # Main difference: Need to average across probes for each GID. Units are in normalized flourescence intensity
        """
        seq_format = "Microarray"
        results = []
        table = []
        for gid in ProbeDict:
                probes = ProbeDict[gid]
                probe_string = ', '.join("'" + probe + "'" for probe in probes)
                gene = geneDict[gid]
                for study in studies:
                        # survival = "" if s_status else "AND survival LIKE \"died\""
                        survival = "" if s_status else "AND survival LIKE \"died\""
                        # sql = """SELECT DPI, avg(expression), virus, std(expression),count(expression), strain
                        #                 FROM MICROARRAY JOIN SAMPLE using (SID) JOIN PATIENT using (PID) JOIN EXPERIMENT using (EID)
                        #                 WHERE probe_id IN (%s) AND STUDY_NAME LIKE "%s" %s and DPI >= 0
                        #                 GROUP BY DPI, virus, strain
                        #                 ORDER BY DPI;"""
                        # sql = sql % (probe_string,"%" + study + "%", survival)
                        # cursor.execute(sql)
                        cursor.execute("""
                                        SELECT DPI, avg(expression), virus,std(expression),count(expression), strain
                                        FROM MICROARRAY JOIN SAMPLE USING (SID) JOIN PATIENT USING (PID) JOIN EXPERIMENT USING (EID)
                                        WHERE probe_id in (%s) AND STUDY_NAME LIKE "%s" %s and DPI >= 0
                                        GROUP BY DPI, virus, strain
                                        ORDER BY DPI;"""%(probe_string, "%" + study + "%", survival))
                        
                        #get results
                        rows = cursor.fetchall()

                        #increment DPI in DPI list and add counts to JSON object
                        DPI = 0
                        counts = []
                        countserror = []

                        if rows:
                                for row in rows:
                                        # This loop accounts for missing data for each day,
                                        # simply moving onto the next day that does have data
                                        if row[0] >= 0:
                                                while DPI_list[DPI] != row[0]: # consider changing to just `DPI != row[0]`
                                                        counts.append(None)
                                                        countserror.append(None)
                                                        DPI += 1
                                                conv = float(row[1])
                                                #GET SE
                                                sd = float(row[3])
                                                n = float(row[4])
                                                nsq = math.sqrt(n)
                                                logmin = 0
                                                logmax = 0
                                                if sd != 0:
                                                        se = sd/nsq
                                                        # microarray is already log transformed... or at least contains -values for what should be counts
                                                        #minimum = conv - se
                                                        #logmin = math.log(minimum,2)
                                                        #maximum = conv + se
                                                        #logmax = math.log(maximum,2)
                                                        logmin = conv - se
                                                        logmax = conv + se
                                                errorbar = []
                                                logconv = 0
                                                if conv != 0:
                                                        logconv = conv # math.log(conv, 2)
                                                counts.append(logconv)
                                                errorbar.append(logmin)
                                                errorbar.append(logmax)
                                                countserror.append(errorbar)

                                                DPI +=1
                                                virus = row[2]
                                                strain = row[5]

                                if len(counts) > 0:
                                        temp = {'name':gene + '_' + study + '_' + seq_format + ('_SURVIVORS' if s_status else ''),
                                                        'data':counts}
                                        results.append(temp)
                                        temperror = {'name':gene + '_' + study + '_' + seq_format + '_error' + ('_SURVIVORS' if s_status else ''),
                                                                 'type':'errorbar',
                                                                 'data':countserror}
                                        results.append(temperror)
                                        tblrow = [gene, virus, seq_format, strain, study]
                                        tblrowfull = tblrow + counts
                                        table.append(tblrowfull)
                        if not cursor.rowcount:
                                noName = gene + '_' + study
                                if noName not in noresults:
                                        noresults.append(noName)

        return results, table, noresults


def microarray_FCQuery_virus (probeDict, geneDict, DPI_list, studies, s_status, hm_x_axis):
        """
        #PURPOSE: Microarray fold change data
        #Note: refer to previous RNASeq pipeline for specific steps
        #Main difference: Need to average across probes for each MMU ID. Units are in normalized flourescence intensity
        #initialize variables
        """
        results = []
        table = []
        seq_format = "Microarray"

        #initialize heat map data
        #initialize temporary dictionary with highcharts format
        heat_map_sortedby_study = []
        heat_map_cats_sortedby_study = []
        DPI_heat_map_cats = []
        heatmap_y = 0

        for key in geneDict:
                gene = geneDict[key]
                #add category to heat map data and initialize list for specific row
                #it is made unique at the end
                DPI_heat_map_cats.append(gene)

        for study in studies:
                #reinitialize DPI heat map data per study
                DPI_heat_map = []
                DPI_heat_map_survivors = [] #for data structure organization
                hmlogic = False
                s_options = [" AND survival LIKE \"died\""]
                if s_status:
                        s_options.append(" AND (survival LIKE \"survived\" OR survival LIKE \"delayed\")")
                for survival in s_options:
                        for gid in probeDict:
                                probes = probeDict[gid]
                                probe_string = ', '.join("'" + probe + "'" for probe in probes)
                                gene = geneDict[gid]
                                DPI_heat_map_row = []
                                DPI_heat_map_survivors_row = []
                                cursor.execute("""
                                        SELECT DPI, avg(expression), virus, strain
                                        FROM MICROARRAY JOIN SAMPLE USING (SID) JOIN PATIENT USING (PID) JOIN EXPERIMENT USING (EID)
                                        WHERE probe_id in (%s) AND STUDY_NAME LIKE "%s" %s and DPI >= 0
                                        GROUP BY DPI, virus, strain
                                        ORDER BY DPI;"""%(probe_string, "%" + study + "%", survival))
                                # if survival == "AND survival LIKE \"died\"":
                                #         cursor.execute("""
                                #                 SELECT DPI, avg(expression), virus, strain
                                #                 FROM MICROARRAY JOIN SAMPLE USING (SID) JOIN PATIENT USING (PID) JOIN EXPERIMENT USING (EID)
                                #                 WHERE probe_id in (%s) AND STUDY_NAME LIKE %s and DPI >= 0 AND survival LIKE \"died\"
                                #                 GROUP BY DPI, virus, strain
                                #                 ORDER BY DPI;""", [probe_string, "%" + study + "%"])
                                # else:
                                #         cursor.execute("""
                                #                 SELECT DPI, avg(expression), virus, strain
                                #                 FROM MICROARRAY JOIN SAMPLE USING (SID) JOIN PATIENT USING (PID) JOIN EXPERIMENT USING (EID)
                                #                 WHERE probe_id in (%s) AND STUDY_NAME LIKE %s and DPI >= 0 AND (survival LIKE \"survived\" OR survival LIKE \"delayed\")
                                #                 GROUP BY DPI, virus, strain
                                #                 ORDER BY DPI;""", [probe_string, "%" + study + "%"])
                                #get results
                                FCs = []
                                DPI = 0
                                heatmap_x = 0
                                day_zero_exp = 0

                                rows = cursor.fetchall()
                                for row in rows:
                                        if row[0] < 0:
                                                continue
                                        if row[0] == 0:
                                                day_zero_exp = float(row[1])
                                                heatmap_y += 1
                                        while DPI_list[DPI] != row[0]:
                                                FCs.append(None)
                                                DPI+=1
                                        current_exp = float(row[1])
                                        loggedFC = 0
                                        if current_exp != 0 and day_zero_exp != 0:
                                                loggedFC = current_exp - day_zero_exp
                                        FCs.append(loggedFC)
                                        study_plus_dpi = study + ('_survivors_' if (survival != s_options[0]) else "") + "_day_" + str(DPI)
                                        temp2 = [heatmap_x,heatmap_y,loggedFC, study_plus_dpi, gene]
                                        if survival == s_options[0]:
                                                DPI_heat_map_row.append(temp2)
                                        else:
                                                DPI_heat_map_survivors_row.append(temp2)
                                        if study_plus_dpi not in hm_x_axis:
                                                hm_x_axis.append(study_plus_dpi)
                                        heatmap_x += 1
                                        DPI += 1
                                        virus = row[2]
                                        strain = row[3]
                                        hmlogic = True #There were genes, so append to heat map. Remains false if no genes

                                if len(FCs) > 0:
                                        temp = {'name':gene + '_' + study, 'data':FCs}
                                        results.append(temp)
                                        tblrow = [gene, virus, seq_format, strain, study]
                                        tblrowfull = tblrow + FCs
                                        table.append(tblrowfull)
                                if DPI_heat_map_row:
                                        DPI_heat_map += DPI_heat_map_row
                                if DPI_heat_map_survivors_row:
                                        DPI_heat_map_survivors += DPI_heat_map_survivors_row

                        #increment y for heatmap
                        heatmap_y+=1
                if hmlogic is True:
                        heat_map_sortedby_study.append(DPI_heat_map)
                        heat_map_sortedby_study.append(DPI_heat_map_survivors)

        heat_map_cats_sortedby_study.append(DPI_heat_map_cats)

        return results, table, heat_map_sortedby_study, heat_map_cats_sortedby_study, hm_x_axis

##################
## V. MAIN CODE ##
##################

# Get data from client in next section
form = cgi.FieldStorage()

# We had trouble passing booleans, so this is how we're doing the checkbox
s_status = True if form.getvalue("include_survivors") == "on" else False

import time
# log(time.asctime( time.localtime(time.time())), "\nJeff v3")

# initialize list of genes that don't have results
noresults = []

# TODO: use re.split to use multiple types of delimeters
# initialize list of genes entered
genelist = []
genes = form.getvalue("genes")
if genes:
        genelist = genes.split()

samplelist = []
samples = form.getvalue("samples")
if samples:
        samplelist = samples.split()

# get username
login = form.getvalue("username")


# get the headers
print("Content-type: text/json")
print()
print()


# log("got past the forms")

#connect to db
cursor, connection = connect_db()

orig_genelist = genelist

#initialize list of genes not in database
not_in_db = []
sampleDict = createSampledict(samplelist, not_in_db)

strain = getStrain(sampleDict)

datatypes = getDatatypes(sampleDict)

# Dictionary of gene symbols where {gid: ensembl or symbol}
geneDict = getGID(genelist, not_in_db)

#get summary information for first table
gene_table = gene_summ(geneDict)

#get max DPI and return list of DPIs
DPI_list = getMaxDPI(sampleDict, s_status)

# get list of study names
study_names = [key for key in sampleDict]

##############
#   RNASEQ   #
##############

count_results = []
count_table = []
noresults = []
boxplot_data = []
FC_results = []
FC_table = []
heat_map_cats_sortedby_study= []
heat_map_sortedby_study = []
hm_x_axis = []

# If RNAseq is selected
if "RNAseq" in datatypes:
        # log("RNAseq")
        # log(DPI_list)
        count_results, count_table, noresults = countQuery_virus(geneDict, DPI_list, study_names, noresults, s_status)
        #boxplot_data = count_boxplot_virus(geneDict, DPI_list, study_names, noresults, s_status)

        #get FC results for RNAseq
        FC_results, FC_table, heat_map_sortedby_study, heat_map_cats_sortedby_study, hm_x_axis = FCQUERY_virus(geneDict, DPI_list, study_names, s_status, hm_x_axis)


##############
# MICROARRAY #
##############

microarray_boxplot_results = []
microarray_count_results = []
# if microarray is selected
if "Microarray" in datatypes:
        # log("microarray\n")
        microarray_DPI = []
        microarray_count_table = []
        microarray_FC_results = []
        microarray_FC_table = []
        MAheat_map_sortedby_study = []
        MAheat_map_cats_sortedby_study = []

        # get probes for each gid and store into dictionary
        ProbeDict = get_Probe_IDs(geneDict, not_in_db)

        # call function to get microarray counts
        microarray_count_results, microarray_count_table, noresults = microarray_countQuery_virus(ProbeDict, geneDict, DPI_list, study_names, noresults, s_status)
        microarray_boxplot_results = count_boxplot_microarray_virus(geneDict, noresults)

        # call function to get microarray FC data
        microarray_FC_results, microarray_FC_table, MAheat_map_sortedby_study, MAheat_map_cats_sortedby_study, hm_x_axis = microarray_FCQuery_virus(ProbeDict, geneDict, DPI_list, study_names, s_status, hm_x_axis)

        #append tables and FC results but not count results
        count_results = count_results + microarray_count_results
        count_table = count_table + microarray_count_table
        FC_results = FC_results + microarray_FC_results
        FC_table = FC_table + microarray_FC_table
        heat_map_cats_sortedby_study = heat_map_cats_sortedby_study + MAheat_map_cats_sortedby_study
        heat_map_sortedby_study = heat_map_sortedby_study + MAheat_map_sortedby_study

###############
# RETURN DATA #
###############

all_results = []
all_results.append(gene_table)#                                         0
all_results.append(count_results)###################1
all_results.append(FC_results)#                                         2
all_results.append(DPI_list)########################3
all_results.append(count_table)#                                        4
all_results.append(FC_table)########################5
all_results.append(hm_x_axis)#                                          6
all_results.append(study_names)#####################7
all_results.append(genelist)#                                           8 genelist
all_results.append(not_in_db)#######################9
# all_results.append(["test", "10"])
all_results.append(heat_map_cats_sortedby_study)#       10       
# all_results.append(["test", "12"])
all_results.append(heat_map_sortedby_study)#########11
all_results.append(microarray_count_results)#           12

# DEBUG RESULTS. REMOVE WHEN FINISHED DEBUGGING
all_results.append(genelist)#                                           16 genelist
all_results.append(geneDict)########################17 geneDict
all_results.append("")#                                                         18 MMUDict
all_results.append(strain)##########################19
all_results.append(orig_genelist)#                                      20
all_results.append(login)###########################21
all_results.append([])#                                                         22 test_data

# MORE IMORTANT RESULTS
all_results.append(boxplot_data)####################23
all_results.append(microarray_boxplot_results)#         24


#results will be a list of dictionaries (for each output type)
print(json.dumps(all_results))


#disconnect from db
disconnect_db(cursor,connection)
