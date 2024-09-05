#!/usr/bin/python

import hashlib
import pymysql
import sys
import cgi
import cgitb
import json
import csv
import os
import io

cgitb.enable()
####################
## FUNCTIONS ##
####################

######
# Function to connect to the localhost database
def connect_db():
        #connect to database
        connection = pymysql.connect()
        #get cursor
        cursor = connection.cursor()
        return cursor, connection

#######
# Function to disconnect from the localhost database
def disconnect_db(cursor, connection):
        #close cursor and connection
        cursor.close()
        connection.close()


#######
# Function to get the EID from a study name in the EXPERIMENT table

def get_EID(study):
        query = """
        SELECT EID
        FROM EXPERIMENT_TEST
        WHERE STUDY_NAME = %s
        """
        try:
                cursor.execute(query, (study,))
                result = cursor.fetchone()
                if result:
                        return result[0]
                else:
                        print(e,query)
        except pymysql.Error as e: 
                print(e, query)
                return None


#######
# Function to get the PubID from a paper name in the PAPERS table

def get_PUBID(title):
        query = """
        SELECT PUBID
        FROM PUBLICATION
        WHERE TITLE = %s
        """
        try:
                cursor.execute(query, (title,))
                result = cursor.fetchone()
                if result:
                        return result[0]
                else:
                        return None
        except pymysql.Error as e: 
                print(e, query)
                return None
######
# Function to check that this sample_id hasn't been entered before, and also to enter into database
def get_SID(sample_id):
        query = """
        SELECT SID
        FROM SAMPLE_TEST
        WHERE sample_id = %s
        """
        try:
                cursor.execute(query, (sample_id,))
                # cursor.execute(query)
                result = cursor.fetchone()
                if result:
                        return result[0]
                else:
                        return None
        except pymysql.Error as e: 
                print(e, query)
                return None

# Functions to get GID and ensembl_ID for entering RNA sequencing data into the database
def get_GID(gene_name):
        query = """
        SELECT GID
        FROM GENES
        WHERE WikiGene_Name_MMU = %s
        """
        try:
                cursor.execute(query, (gene_name,))
                result = cursor.fetchall()
                if result:
                        return result[0][0]  # Return the first element of the list
                else:
                        return None
        except pymysql.Error as e: 
                print(e, query)
                return None

def get_ensembl(gene_name):
        query = """
        SELECT ensembl_MMU
        FROM GENES
        WHERE WikiGene_Name_MMU = %s
        """
        try:
                cursor.execute(query, (gene_name,))
                result = cursor.fetchall()
                if result:
                        return result[0][0]  # Return the first element of the list
                else:
                        return None
        except pymysql.Error as e: 
                print(e, query)
                return None

#######
# Function to parse the rna csv to input the results into the 

def process_csv(input_csv_path, output_csv_path):
    df = pd.read_csv(input_csv_path, header=0, index_col=0)
    
    processed_rows = []

    for gene_name, row in df.iterrows():
        for sample_id, expression in row.items():
            # Get SID and GID from the database
            SID = get_SID(sample_id)
            GID = get_GID(gene_name)
            ensembl = get_ensembl(gene_name)
            
            if SID and (GID or ensembl):
                processed_row = {
                    'SID': SID,
                    'GID': GID,
                    'ensembl': ensembl,
                    'expression': expression
                }
                processed_rows.append(processed_row)

    # Write processed data to a new CSV file
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['SID', 'GID', 'ensembl', 'expression']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_rows)




###########################################

print("Content-type: text/html\n")

# This is where the form values get parsed and values are input into the database / retrieved from the database
form = cgi.FieldStorage()
if (form):
    cursor, connection = connect_db()
    results = []

    # This selector is what chooses which query is executed, chosen in the HTML file by which button is pressed
    selector = form.getvalue("selector", "")
    
    # This automatically loads each time you load the document
    # Loads the paper titles for the dropdown selection for enter_experiment pubID value

    if (selector == "papers"):
        query = """
        select TITLE
        from PUBLICATION
        order by PUBID asc
        """
        try:
            cursor.execute(query)    
        except pymysql.Error as e: 
            print(e,query)    

        results = cursor.fetchall()
        print(json.dumps(results))
    
    # This gets loaded twice, once for the enter RNA_Sequencing data dropdown, once for the Samples data dropdown
    # This fills in the experiment dropdown with the titles of the experiments in the experiment table
    # Currently takes in from the EXPERIMENT_TEST table, change to EXPERIMENT table once done with testing

    elif (selector == "experiment"):
        query = """
        select STUDY_NAME
        from EXPERIMENT_TEST
        order by STUDY_NAME asc
        """
        try:
            cursor.execute(query)    
        except pymysql.Error as e: 
            print(e,query)    

        results = cursor.fetchall()
        print(json.dumps(results))
    # This gets loaded whenever the experiment dropdown for the experiment stats button is changed
    # This returns all the information for each experiment in a json, so it can be put into the 
    # createSortableTables function in the html file

    elif selector == "experimentStats":
        experiment = get_EID(form.getvalue("experiment"))

        patient_query = """
        SELECT PID, PATIENT_NAME, PFU, survival, Vaccinated, EID, NHP_ID
        FROM PATIENT
        where EID = %s;
        """

        samples_query = """
        SELECT SID, sample_id, DPI, virus_count, Experimental_condition, PID, EID
        FROM SAMPLE_TEST
        where EID = %s;
        """

        rna_samples_genes_query = """
        SELECT count(distinct(r.SID)) as samples, count(distinct(r.GID)) as genes
        FROM RNAseq_TEST2 r join SAMPLE_TEST st using(SID)
        where EID = %s;
        """

        rna_missing_samples_query = """
        select sample_id as sample
        from SAMPLE_TEST
        where SID not in (select SID from RNAseq_TEST2 rt) and EID = %s;
        """

        try:
            cursor.execute(patient_query, (experiment,))
            patients_results = cursor.fetchall()
        except pymysql.Error as e:
            print(e, patient_query)

        try:
            cursor.execute(samples_query, (experiment,))
            samples_results = cursor.fetchall()
        except pymysql.Error as e:
            print(e, samples_query)

        try:
            cursor.execute(rna_samples_genes_query, (experiment,))
            seq_stats_results = cursor.fetchone()
        except pymysql.Error as e:
            print(e, rna_samples_genes_query)

        try:
            cursor.execute(rna_missing_samples_query, (experiment,))
            missing_samples_results = cursor.fetchall()
        except pymysql.Error as e:
            print(e, rna_missing_samples_query)

        response = {
                "patients": [],
                "samples": [],
                "seq_stats": []
                }

                # Convert seq_stats dictionary to an array of key-value pairs
        response["seq_stats"] = [
              {
        "Experiment ID": experiment,
        "Number of Samples": seq_stats_results[0] if seq_stats_results else 0,
        "Samples without Sequencing Data": "No missing samples" if not missing_samples_results else [row[0] for row in missing_samples_results],
        "Number of Genes": seq_stats_results[1] if seq_stats_results else 0,
              }
        ]
        # for key, value in seq_stats_dict.items():
        #         response["seq_stats"].append({key : value})

        # Add patients
        for row in patients_results:
                response["patients"].append({
                        "PID": row[0],
                        "PATIENT_NAME": row[1],
                        "PFU": row[2],
                        "survival": row[3],
                        "Vaccinated": row[4],
                        "EID": row[5],
                        "NHP_ID": row[6]
                })

        # Add samples
        for row in samples_results:
                response["samples"].append({
                        "SID": row[0],
                        "sample_id": row[1],
                        "DPI": row[2],
                        "virus_count": row[3],
                        "Experimental_condition": row[4],
                        "PID": row[5],
                        "EID": row[6]
                })
        print(json.dumps(response))

    # This is called whenever the "Enter Experiment" button is pressed
    # Takes in all of the data in the form for the experiment and inserts it into EXPERIMENT_TEST
    # Make sure to make this EXPERIMENT once you are sure that it works

    elif (selector == "enter_experiment"):

        study_name = form.getvalue("studyname")
        virus = form.getvalue("virus")
        strain = form.getvalue("strain")
        species = form.getvalue("species")
        tissue_type = form.getvalue("tissuetype")
        exposure_route = form.getvalue("exposureroute")
        papername = form.getvalue("paper")
        pubid = get_PUBID(papername)

        query = """
        INSERT INTO EXPERIMENT_TEST (study_name, virus, strain, species, tissue_type, exposure_route, pubid)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (study_name, virus, strain, species, tissue_type, exposure_route, pubid))
            connection.commit()
        except pymysql.Error as e: 
            print(e, query)
        
    # This is called whenever the "Enter Sample" button is pressed
    # Takes in all of the data in the form for the sample and inserts it into SAMPLE_TEST
    # Make sure to make this SAMPLE once you are sure that it works

    elif (selector == "enter_sample"):
        
        sample_id = form.getvalue("sample_id")
        DPI = form.getvalue("dpi")
        virus_count = form.getvalue("virus_count")
        Experimental_condition = form.getvalue("Experimental_condition")
        PID = form.getvalue("PID")
        EID = get_EID(form.getvalue("experiment"))

        if virus_count == "NULL":
                virus_count = None

        query = """
        INSERT INTO SAMPLE_TEST (sample_id, DPI, virus_count, Experimental_condition, PID, EID)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (sample_id, DPI, virus_count, Experimental_condition, PID, EID))
            connection.commit()
            print("Returned")
        except pymysql.Error as e: 
            print(e, query)
        
    # This is called whenever the "Enter RNA Sequencing Data" button is pressed
    # Takes in all of the data in the form for the RNA_Sequencing data and inserts it into RNAseq_TEST2
    # Make sure to make this RNAseq once you are sure that it works

    # Alright this is an incredibly janky solution. Basically I'm going to get the number of entries in the entire csv,
    # and then add each entry to a list until we've added all the entries in the dataframe. 

    # I couldn't get a selector in here because of the fact that it calls so many different objects, so what we're going to do 
    # is keep this as an else statement and then 
    else:
        rna_data = []
        data = form.getvalue("data")  # Get the list of objects
        data = json.loads(data)
        for obj in data:
                sample_id = obj['sampleID']
                gene_name = obj['gene_name']
                gene_name = gene_name.strip()
                SID = get_SID(sample_id)
                GID = get_GID(gene_name)
                ensembl = get_ensembl(gene_name)
                expression = obj['expression']
                # Add an if statement so that if GID and SID, then append, otherwise continue
                if SID and GID:
                        rna_data.append([SID, GID, ensembl, expression])
                elif SID and not GID:
                        # TODO: add gene to GENES table
                        continue
                else:
                        continue
        # Write the data to the CSV file and load it into the SQL database
        with open('/var/www/cgi-bin/rna_data.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rna_data)
                print("done")
        query = """
        LOAD DATA INFILE '/var/www/cgi-bin/rna_data.csv'
        INTO TABLE RNAseq_TEST2
        FIELDS TERMINATED BY ','
        """
        try:
                cursor.execute(query)
                connection.commit()
                print("Added RNA")
        except pymysql.Error as e:
                print(e, query)
        


    disconnect_db(cursor, connection)



else:
        

    print("No form data entered.")