#!/usr/bin/python


###################################
#  RECLUSTER FC ACROSS DATATYPES  #
###################################

###INPUTS###
#1. Unclustered RNAseq data
#2. Unclustered Microarray data

###STEPS###
#1. Receive data
#2. Concatenate strings in proper format
#3. Cluster with heatmap_cluster.main


import cgi
import cgitb
import sys
import json
import heatmap_cluster


cgitb.enable()

##----FUNCTIONS----##


##----MAIN FUNCTION----##

#get the headers
print("Content-type: text/json")
print()
print()

result = ["EBOV_PBMC_aersol_RNASeq_1","EBOV_PBMC_aersol_RNASeq_3","EBOV_PBMC_aersol_RNASeq_6","EBOV_PBMC_aersol_RNASeq_8"],[[[0,0,0.8872380885715585,"EBOV_PBMC_aersol_RNASeq_1","EMC2"],[1,0,0.7984437567047001,"EBOV_PBMC_aersol_RNASeq_3","EMC2"],[2,0,1.3769743644972616,"EBOV_PBMC_aersol_RNASeq_6","EMC2"],[3,0,1.859063591072143,"EBOV_PBMC_aersol_RNASeq_8","EMC2"]]],[[[0,0,0,"EBOV_PBMC_Drug_Microarray_0","EMC2"],[1,0,0.4582795844931766,"EBOV_PBMC_Drug_Microarray_3","EMC2"],[2,0,0.5758028379387602,"EBOV_PBMC_Drug_Microarray_6","EMC2"]]]

data = sys.stdin.read()
myjson = json.loads(data)

print(json.dumps(result))
