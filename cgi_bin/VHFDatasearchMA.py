#!/usr/bin/python


############################
# Microarray Data Pipeline #
############################


import pymysql
import cgi
import cgitb
import sys
import json
import math

cgitb.enable()

##----FUNCTIONS----##


def connect_db():
        # connect to database
        connection = pymysql.connect()
        # get cursor
        cursor = connection.cursor()

        return cursor, connection


def getGID(MMUdict):

        # initialize gene dictionary
        geneDict = {}
        # loop through list of genes and get gid for each
        for gene in MMUdict:
                MMUlist = MMUdict[gene]
                for MMU in MMUlist:
                        #query databse for gid of genes
                        cursor.execute("""
                                SELECT gid
                                FROM gene2
                                WHERE gene_id LIKE "%s";
                        """%(MMU))
                        #get the only the gid
                        rows = cursor.fetchall()
                        if rows:
                                for row in rows:
                                        if row[0] not in geneDict:
                                                #make gid key and gene name value
                                                geneDict[row[0]] = gene
        return geneDict


def ensembl2GID(enslist):
        # initialize list
        genelist = []
        # iterate through list
        for id in enslist:
                # check if ensembl is an MMU ID
                if "MMU" in id or "mmu" in id:
                        cursor.execute("""
                        SELECT WikiGene_Name_human, Ensembl_Gene_ID_human
                        FROM Converter02
                        WHERE Ensembl_Gene_ID_MMU LIKE "%s"
                        """ % ("%" + id + "%"))
                        name = cursor.fetchone()
                elif "ENSG" in id or "ensg" in id:
                        cursor.execute("""
                        SELECT WikiGene_Name_human, Ensembl_Gene_ID_MMU
                        FROM Converter02
                        WHERE Ensembl_Gene_ID_human LIKE "%s"
                        """ % ("%" + id + "%"))
                        name = cursor.fetchone()
                if name:
                        if name[0] not in genelist:
                                #get WikiGene_Name
                                genelist.append(name[0])
                        ##genelist.append(name[1])
        return genelist


def gene_summ(genes):
        #create the gene summary table
        gene_table = []
        for gene in genes:
                gname = genes[gene]
                item = []
                cursor.execute("""
                SELECT Ensembl_Gene_ID_human
                FROM Converter02
                WHERE WikiGene_Name_human LIKE "%s";
                """%(gname))
                row = cursor.fetchone()
                if row :
                        item = [row[0],gname]
                        gene_table.append(item)
                else:
                        item = ['N/A', gname]
                        gene_table.append(item)
        return gene_table


def checkAlt(genelist):
        more_genes = []
        #check for alternate formats
        for gene in genelist:
                #check if WG_MMU
                cursor.execute("""
                SELECT WikiGene_Name_human
                FROM Converter02
                WHERE WikiGene_Name_MMU LIKE "%s";
                """%(gene))
                rows = cursor.fetchall()
                if rows:
                        for row in rows:
                                name = row[0].strip()
                                if row[0] != '' and name not in genelist:
                                        more_genes.append(name)
                                        #remove the found gene from the list
                                        while gene in genelist:
                                                genelist.remove(gene)

                #check if UniprotHuman
                cursor.execute("""
                SELECT WikiGene_Name_human
                FROM Converter02
                WHERE UniProt_Name_human LIKE "%s";
                """%(gene))
                rows = cursor.fetchall()
                if rows:
                        for row in rows:
                                name = row[0].strip()
                                if row[0] != '' and name not in genelist:
                                        more_genes.append(name)
                                        #remove the found gene from the list
                                        while gene in genelist:
                                                genelist.remove(gene)

                #check if UniprotMMU
                cursor.execute("""
                SELECT WikiGene_Name_human
                FROM Converter02
                WHERE UniProt_Name_MMU LIKE "%s";
                """%(gene))
                rows = cursor.fetchall()
                if rows:
                        for row in rows:
                                name = row[0].strip()
                                if row[0] != '' and name not in genelist:
                                        more_genes.append(name)
                                        #remove the found gene from the list
                                        while gene in genelist:
                                                genelist.remove(gene)
        genelist = genelist + more_genes
        return genelist


def createMMUdict (genelist, not_in_db, ENS2GI):
        MMUdict = {}

        for gene in genelist:
                #go through gene list and find each MMU for each gene
                cursor.execute("""
                SELECT Ensembl_Gene_ID_MMU
                FROM Converter02
                WHERE WikiGene_Name_human LIKE "%s"
                GROUP BY Ensembl_Gene_ID_MMU;
                """%(gene))
                rows = cursor.fetchall()
                #if rows, make gene name key and MMU names values
                if rows:
                        for row in rows:
                                MMU = row[0]
                                key = gene
                                if key not in MMUdict:
                                        MMUdict[key] = []
                                MMUdict[key].append(MMU)
                                if MMU not in ENS2GI:
                                        ENS2GI[MMU] = gene
                else:
                        not_in_db.append(gene)
        return MMUdict, not_in_db, ENS2GI


def getMaxDPI (genes, strains, datatypes, s_status):

        #initialize current max
        maxDPI = 0

        for type in datatypes:
                for strain in strains:
                        for key in genes:
                                gene = genes[key]
                                gid = key

                                if type == "RNAseq":
                                        if strain == "Kikwit":
                                                if s_status == True:
                                                        cursor.execute("""
                                                        SELECT max(DPI)
                                                        FROM gene_expression2 JOIN metadata USING (sid)
                                                        WHERE gid = %s AND strain LIKE "%s" AND Sequencing_type LIKE "%s"
                                                        ORDER BY DPI DESC;
                                                        """%(gid, strain,"%" + type + "%"))
                                                        row = cursor.fetchone()
                                                else:
                                                        cursor.execute("""
                                                        SELECT max(DPI)
                                                        FROM gene_expression2 JOIN metadata USING (sid)
                                                        WHERE gid = %s AND strain LIKE "%s" AND Sequencing_type LIKE "%s" AND survival LIKE "died"
                                                        ORDER BY DPI DESC;
                                                        """%(gid, strain,"%" + type + "%"))
                                                        row = cursor.fetchone()
                                        else:
                                                cursor.execute("""
                                                SELECT max(DPI)
                                                FROM gene_expression2 JOIN metadata USING (sid)
                                                WHERE gid = %s AND strain LIKE "%s" AND Sequencing_type LIKE "%s"
                                                ORDER BY DPI DESC;
                                                """%(gid, strain,"%" + type + "%"))
                                                row = cursor.fetchone()
                                else:
                                        cursor.execute("""
                                        SELECT max(DPI)
                                        FROM gene_expression2 JOIN metadata USING (sid)
                                        WHERE gid = %s AND Sequencing_type LIKE "%s"
                                        ORDER BY DPI DESC;
                                        """%(gid,"%" + type + "%"))
                                        row = cursor.fetchone()

                                if row:
                                        loc_max = row[0]
                                else:
                                        loc_max = 0

                                if loc_max > maxDPI:
                                        maxDPI = loc_max

        #make a list for incrementing DPI
        DPI_list = []
        for n in range(0,maxDPI + 1):
                DPI_list.append(n)

        return DPI_list


def get_Probe_IDs(MMUdict, not_in_db):
        ProbeDict = {}

        for gene in MMUdict:
                MMUlist = MMUdict[gene]
                for MMU in MMUlist:
                        #go through gene list and find each MMU for each gene
                        cursor.execute("""
                        SELECT Probe_ID
                        FROM Ensembl2GI2Probe LEFT JOIN Converter02 ON Ensembl_ID_Human = Ensembl_Gene_ID_human
                        WHERE Ensembl_Gene_ID_MMU LIKE "%s";
                        """%(MMU))
                        rows = cursor.fetchall()
                        #if rows, make gene name key and MMU names values
                        if rows:
                                for row in rows:
                                        probe = row[0]
                                        key = MMU
                                        if key not in ProbeDict:
                                                ProbeDict[key] = []
                                        ProbeDict[key].append(probe)
                        else:
                                not_in_db.append(gene)

        return ProbeDict, not_in_db


def microarray_countQuery_virus (ProbeDict, ENS2GI):
        test_list = []
        results = []
        table = []
        study = ''
        for gene in ProbeDict:
                probes = ProbeDict[gene]
                sql = """SELECT DPI, avg(expression_level), std(expression_level),count(expression_level), Study_Name
                                FROM microarray_expression02
                                JOIN metadata USING (sample_id)
                                WHERE probe_id IN (%s)
                                GROUP BY DPI ORDER BY DPI;"""
                in_p = ', '.join(map(lambda x: '%s', probes))
                sql = sql % in_p
                cursor.execute(sql, probes)
                #get results
                rows = cursor.fetchall()

                #increment DPI in DPI list and add counts to JSON object
                DPI = 0
                counts = []
                countserror = []

                if rows:
                        for row in rows:
                                if row[0] >= 0:
                                        while DPI != row[0]:
                                                counts.append(None)
                                                countserror.append(None)
                                                DPI += 1
                                        conv = float(row[1])
                                        test_list.append(conv)
                                        #GET SE
                                        sd = float(row[2])
                                        n = float(row[3])
                                        nsq = math.sqrt(n)
                                        if sd != 0:
                                                se = sd/nsq
                                                min = conv - se
                                                logmin = min #temporary
                                                #logmin = math.log(min,2)
                                                max = conv + se
                                                logmax = max #temporary
                                                #logmax = math.log(max,2)
                                        else:
                                                logmin = 0
                                                logmax = 0
                                        errorbar = []
                                        if conv != 0:
                                                logconv = conv #temporary
                                                #logconv = math.log(conv, 2) #toggle this
                                        else:
                                                logconv = 0
                                        counts.append(logconv)
                                        errorbar.append(logmin)
                                        errorbar.append(logmax)
                                        countserror.append(errorbar)

                                        DPI +=1
                                        study = row[4].strip()
                        if len(counts) > 0:
                                gene_id = ''
                                for key in ENS2GI:
                                        if key == gene:
                                                gene_id = ENS2GI[key]
                                temp = {'name':gene_id + '_' + study + '_microarray', 'data':counts}
                                results.append(temp)
                                temperror = {'name':gene_id + '_' + study + '-' + '_error', 'type':'errorbar', 'data':countserror}
                                results.append(temperror)
                                tblrow = [gene_id, 'ebola', 'Microarray', "Mayinga", study]
                                tblrowfull = tblrow + counts
                                table.append(tblrowfull)
                # if not cursor.rowcount:
                        # noName = gene + '_' + study + '-' + strain
                        # if noName not in noresults:
                                # noresults.append(noName)
        return results, table


def microarray_FCQuery_virus (ProbeDict, ENS2GI, heat_map_sortedby_study):
        #initialize variables
        test_list = []
        results = []
        table = []
        study = ''
        heat_map_sortedby_study = []
        y = 0


        for gene in ProbeDict:
                #get probes attributed to gene in dictionary
                probes = ProbeDict[gene]

                #initialize DPI heatmap row
                DPI_heat_map_row = []
                x = 0

                sql = """SELECT DPI, avg(expression_level),Study_Name FROM microarray_expression02 JOIN metadata USING (sample_id) WHERE probe_id IN (%s) GROUP BY DPI ORDER BY DPI;"""
                in_p = ', '.join(map(lambda x: '%s', probes))
                sql = sql % in_p
                cursor.execute(sql, probes)
                #get results
                rows = cursor.fetchall()

                FCs = []
                DPI = 0
                n = 0

                for row in rows:
                        #negative DPI not included
                        if row[0] > 0:
                                while DPI != row[0]:
                                        FCs.append(None)
                                        DPI+=1

                        #if DPI positive and matches current position
                        if row[0] >= 0 and DPI == row[0]:
                                #if DPI is zero...
                                if row[0] == 0:
                                        DPI_zero = row[1]
                                        day_zero_exp = float(DPI_zero)
                                        loggedFC = 0
                                        FCs.append(loggedFC)
                                # while DPI != row[0]:
                                        # FCs.append(None)
                                        # DPI+=1

                                #if DPI is greater than zero...
                                if row[0] > 0:
                                # else:
                                        current_exp = float(row[1])
                                        if current_exp != 0 and day_zero_exp !=0:
                                                FC = current_exp/day_zero_exp
                                                #loggedFC = math.log(FC,2)
                                                loggedFC = FC
                                        else:
                                                loggedFC = 0
                                        FCs.append(loggedFC)
                                #get study name from query
                                study = row[2].strip()

                                ###Get necessary data and append to heatmap row, then increment x
                                gene_id = ''
                                for key in ENS2GI:
                                        if key == gene:
                                                gene_id = ENS2GI[key]
                                study_plus_dpi = study + '_' + str(DPI)
                                temp2 = [x,y,loggedFC, study_plus_dpi, gene_id]
                                DPI_heat_map_row.append(temp2)
                                DPI += 1
                                x+=1


                if len(FCs) > 0:
                        gene_id = ''
                        for key in ENS2GI:
                                if key == gene:
                                        gene_id = ENS2GI[key]
                        temp = {'name':gene_id + '_' + study  + '-Mayinga', 'data':FCs}
                        results.append(temp)
                        tblrow = [gene_id, 'ebola', 'Microarray', "Mayinga", study]
                        tblrowfull = tblrow + FCs
                        table.append(tblrowfull)

                #increment y for next gene and append info to heat map
                y+=1
                heat_map_sortedby_study.append(DPI_heat_map_row)
        return results, table, heat_map_sortedby_study


def disconnect_db(cursor, connection):
        #close cursor and connection
        cursor.close()
        connection.close()

# #----MAIN CODE----# #

# get data from client
form = cgi.FieldStorage()

# ####VIRUS RESULTS#### #
evirus = form.getvalue("evirus")
mvirus = form.getvalue("mvirus")
lvirus = form.getvalue("lvirus")
#######################

# ####DATA TYPE RESULTS#### #
# get datatypes and append to list
datatype = []
datatype1 = form.getvalue("type1")
datatype2 = form.getvalue("type2")
datatype3 = form.getvalue("type3")


if datatype1:
        datatype.append(datatype1)

if datatype2:
        datatype.append(datatype2)

if datatype3:
        datatype.append(datatype3)
############################

# ####STRAIN RESULTS#### #

# get strains
strain = []
estrain1 = form.getvalue("estrain1")
estrain2 = form.getvalue("estrain2")
estrain3 = form.getvalue("estrain3")
lstrain = form.getvalue("lstrain")
mstrain = form.getvalue("mstrain")

if estrain1:
        strain.append(estrain1)
if estrain2:
        strain.append(estrain2)
if estrain3:
        strain.append(estrain3)
if lstrain:
        strain.append(lstrain)
if mstrain:
        strain.append(mstrain)

# ####With no survivors?#### #
survivors = form.getvalue("survivors")
if survivors == "Yes":
        s_status = True
else:
        s_status = False


############################

# initialize list of genes that don't have results
noresults = []

# initialize list of genes entered
genelist = []
genes = form.getvalue("genes")
if genes:
        # split genes into a list
        genelist = genes.split()


# check for ensemblIDs entered
ensIDs = form.getvalue("ensemblID")
# if ensIDs:
        # split ensIDs into list
        # enslist = ensIDs.split()

# get username
login = form.getvalue("username")

# get the headers
print("Content-type: text/json")
print()
print()

# connect to db
cursor, connection = connect_db()

# initialize dictionary of ensmmu->wikigeneID
ENS2GI = {}


# get wikigene names from converter
if ensIDs:
        # split ensIDs into list
        enslist = ensIDs.split()
        ensGenes = ensembl2GID(enslist)
        if genes:
                # append all gene symbols together into one big list
                genelist = genelist + ensGenes
        else:
                genelist = ensGenes

# check to see if genes are in another format
genelist = checkAlt(genelist)

# initialize list of genes not in database
not_in_db = []

# get each ensembl MMU id for each gene in genelist
MMUdict, not_in_db, ENS2GI = createMMUdict(genelist, not_in_db, ENS2GI)


# get gIDs of results
geneDict = getGID(MMUdict)


# get summary information for first table
gene_table = gene_summ(geneDict)


# get max DPI and return list of DPIs
DPI_list = getMaxDPI(geneDict, strain, datatype, s_status)


# get list of study names
# study_names = getStudyNames (geneDict, strain, datatype, login)


# process genelist to eliminate duplicates
unique_list = []
for word in genelist:
        for i in range(len(unique_list)):
                if unique_list[i].lower() == word.lower():
                        unique_list[i] = min(word, unique_list[i])
                        break
                else:
                        unique_list.append(word)


# #######----------------MICROARRAY PIPELINE----------########### #

microarray_DPI = []
microarray_count_results = []
microarray_count_table = []
microarray_FC_results = []
microarray_FC_table = []
heat_map_sortedby_study = []
ProbeDict = {}

# if microarray is selected
if datatype2:
        # get probes for each MMU and store into dictionary
        ProbeDict, not_in_db = get_Probe_IDs(MMUdict, not_in_db)

        # call function to get microarray counts
        # microarray_count_results, microarray_count_table
        microarray_count_results, microarray_count_table = microarray_countQuery_virus(ProbeDict, ENS2GI)

        # call function to get microarray FC data
        microarray_FC_results, microarray_FC_table, heat_map_sortedby_study = microarray_FCQuery_virus(ProbeDict, ENS2GI, heat_map_sortedby_study)

        # study_names = getStudyNames(ProbeDict, ENS2GI)


all_results = []
all_results.append(microarray_count_results)
all_results.append(microarray_FC_results)
all_results.append(microarray_count_table)
all_results.append(microarray_FC_table)
all_results.append(heat_map_sortedby_study)
all_results.append(DPI_list)
# all_results.append(study_names)

# results will be a list of dictionaries (for each output type)

print(json.dumps(all_results))


# disconnect from db
disconnect_db(cursor,connection)
