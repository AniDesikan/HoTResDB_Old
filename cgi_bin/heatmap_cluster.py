#!/usr/bin/python

import cgitb
import json
import math
import numpy
import scipy
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster, leaves_list
from scipy.spatial.distance import pdist, squareform
import matplotlib
matplotlib.use('Agg')  # Disables Matplotlib GUI, which was giving errors on hotres-development. No idea why
import matplotlib.pyplot as plt
# import inchlib_clust
import random
import re
import pylab
import copy



cgitb.enable()

# Debug Data
# gene = ['STAT1', 'stat2']
# DPI = [[[0, 0, -0.3536539937165816, 'EBOV_PBMC_aersol_RNASeq_1', 'STAT1'], [1, 0, 0.03299137809929163, 'EBOV_PBMC_aersol_RNASeq_3', 'STAT1'], [2, 0, 2.1874513356194094, 'EBOV_PBMC_aersol_RNASeq_6', 'STAT1'], [3, 0, 2.906101176811325, 'EBOV_PBMC_aersol_RNASeq_8', 'STAT1'], [0, 1, 0.2990508506759951, 'EBOV_PBMC_aersol_RNASeq_1', 'stat2'], [1, 1, 0.34284165051621085, 'EBOV_PBMC_aersol_RNASeq_3', 'stat2'], [2, 1, 2.337712600670566, 'EBOV_PBMC_aersol_RNASeq_6', 'stat2'], [3, 1, 3.2234330087397223, 'EBOV_PBMC_aersol_RNASeq_8', 'stat2']], [], [[0, 0, 2.961462450592886, 'EBOV_PBMC_Drug_Microarray_3', 'STAT1'], [1, 0, 1.9962635869565224, 'EBOV_PBMC_Drug_Microarray_6', 'STAT1']]]
# gene = ['stat1', 'STAT2', 'isg15', 'CXCL10']
# DPI = [[[0, 0, -0.3536539937165816, 'EBOV_PBMC_aersol_RNASeq_1', 'stat1'], [1, 0, 0.03299137809929163, 'EBOV_PBMC_aersol_RNASeq_3', 'stat1'], [2, 0, 2.1874513356194094, 'EBOV_PBMC_aersol_RNASeq_6', 'stat1'], [3, 0, 2.906101176811325, 'EBOV_PBMC_aersol_RNASeq_8', 'stat1'], [0, 1, 0.2990508506759951, 'EBOV_PBMC_aersol_RNASeq_1', 'STAT2'], [1, 1, 0.34284165051621085, 'EBOV_PBMC_aersol_RNASeq_3', 'STAT2'], [2, 1, 2.337712600670566, 'EBOV_PBMC_aersol_RNASeq_6', 'STAT2'], [3, 1, 3.2234330087397223, 'EBOV_PBMC_aersol_RNASeq_8', 'STAT2'], [0, 2, -2.1110900720340777, 'EBOV_PBMC_aersol_RNASeq_1', 'isg15'], [1, 2, -2.1051743410634067, 'EBOV_PBMC_aersol_RNASeq_3', 'isg15'], [2, 2, 5.517074932744375, 'EBOV_PBMC_aersol_RNASeq_6', 'isg15'], [3, 2, 7.032984799896681, 'EBOV_PBMC_aersol_RNASeq_8', 'isg15'], [0, 3, 0.16114811084408656, 'EBOV_PBMC_aersol_RNASeq_1', 'CXCL10'], [1, 3, 1.062171431151846, 'EBOV_PBMC_aersol_RNASeq_3', 'CXCL10'], [2, 3, 6.738235445688717, 'EBOV_PBMC_aersol_RNASeq_6', 'CXCL10'], [3, 3, 10.909261750345133, 'EBOV_PBMC_aersol_RNASeq_8', 'CXCL10']], [], [[0, 0, 3.125838926174497, 'EBOV_PBMC_Drug_Microarray_3', 'CXCL10'], [1, 0, 3.0100671140939594, 'EBOV_PBMC_Drug_Microarray_6', 'CXCL10'], [0, 1, 0.5086484312148032, 'EBOV_PBMC_Drug_Microarray_3', 'isg15'], [1, 1, 0.5160398230088493, 'EBOV_PBMC_Drug_Microarray_6', 'isg15'], [0, 2, 2.961462450592886, 'EBOV_PBMC_Drug_Microarray_3', 'stat1'], [1, 2, 1.9962635869565224, 'EBOV_PBMC_Drug_Microarray_6', 'stat1']]]
# isg15
# isg20
# ifit1
# mmp8
# tgfbi
# eomes


# #----MAIN CODE----# #
def madhat(data, heatmap_version):  # Initial parse of data
    # Get data from python script
    DPI = copy.deepcopy(data)  # Copies data, does not refer to object

    # Initialize variables
    heatmap_temp = []
    heatmap_temp_comp = []
    initial_temp = False
    highest_count = 0  # Amount to add to X value of array to shift current array correct amount right
    highest_val = 0  # Highest value in the dataset, sets legend limits as this
    curr_count = 0  # Current X within the array
    Ymatrix = {}  # Stores Y value of genes
    highest_x = 0  # Stores length of longest row of studies

    for i in range(len(DPI)):  # Goes through study by study (i = number of studies)
        # studylen = len(DPI[i])/len(gene)  # Number of days per study
        # arraylen = len(DPI[i])  # Number of days in all studies total
        # Remove exact duplicate arrays from DPI
        if initial_temp is False:
            heatmap_temp_comp += [copy.deepcopy(DPI[i])]  # Add current array(i) to existing heatmap array
            # heatmap_temp += copy.deepcopy(DPI[i])
            initial_temp = True
        else:
            DPI_exists = False
            for k in range(len(heatmap_temp_comp)):  # Check if exact copy of array already exists in heatmap temp
                # if heatmap_temp[k] != copy.deepcopy(DPI[i]):
                #     DPI_exists = False
                # print heatmap_temp_comp[k], DPI[i], "<br>"
                if heatmap_temp_comp[k] == copy.deepcopy(DPI[i]):  # If a single array in heatmap_temp is the same, DPI[i[ will not be appended # noqa
                    DPI_exists = True
                    # print "Match Found, Did not Append <br>"
                # else:
                    # print "Match Not Found, Appended <br>"
            if DPI_exists is False:
                heatmap_temp_comp += [copy.deepcopy(DPI[i])]
                # heatmap_temp += copy.deepcopy(DPI[i])  # Add current array(i) to existing heatmap array
                # for y in range(len(heatmap_temp)):
                #     print heatmap_temp[y], "<br>"

    for i in range(len(heatmap_temp_comp)):
        # studylen = len(heatmap_temp_comp[i])/len(gene)  # Number of days per study
        arraylen = len(heatmap_temp_comp[i])  # Number of days in all studies total
        for j in range(arraylen):  # X values, Goes through studies day by day (j = number of days-study)
            heatmap_temp_comp[i][j][0] += highest_count
            curr_count = heatmap_temp_comp[i][j][0]
            if highest_val < heatmap_temp_comp[i][j][2]:
                highest_val = heatmap_temp_comp[i][j][2]
            if i == 0 and heatmap_temp_comp[i][j][4] not in Ymatrix:  # Create dictionary to list Y value associated with gene from initial RNAseq data (set as baseline) # noqa
                Ymatrix[heatmap_temp_comp[i][j][4]] = heatmap_temp_comp[i][j][1]
            if i != 0 and heatmap_temp_comp[i][j][1] != Ymatrix[heatmap_temp_comp[i][j][4]]:  # Set y value for the gene equal to established y value # noqa
                heatmap_temp_comp[i][j][1] = Ymatrix[heatmap_temp_comp[i][j][4]]
            highest_x = heatmap_temp_comp[i][j][0]
        highest_count = curr_count + 1
        heatmap_temp += heatmap_temp_comp[i]  # Add current array(i) to existing heatmap array
    highest_val = math.ceil(highest_val)

    # Reorder by day
    if heatmap_version == "day":
        def getKey(item):
            day = re.search('[0-9]*$', item[3])
            return int(day.group(0))
        heatmap_by_day = sorted(heatmap_temp, key=getKey)  # Sort by day, last value of study-name

        # Initialize values
        curr_study = ""
        curr_x = 0

        # Set x value as position in re-ordered list
        for x in range(len(heatmap_by_day)):
            if curr_study == "":
                curr_study = heatmap_by_day[x][3]  # If current study hasn't been set yet, set as current study
                heatmap_by_day[x][0] = curr_x
            elif heatmap_by_day[x][3] == curr_study:  # If the current study is equal to the previous study, don't change x value # noqa
                heatmap_by_day[x][0] = curr_x  # set x value as current x
                curr_study = heatmap_by_day[x][3]
            else:
                curr_study = heatmap_by_day[x][3]
                curr_x += 1
                heatmap_by_day[x][0] = curr_x
        heatmap_temp = heatmap_by_day

    return heatmap_temp, highest_val, highest_x


def cluster(dataMatrix, fullMatrix, geneMatrix):
    # get your data into a 2d numpy array where rows are genes, and columns are conditions
    arr_2d = numpy.array(dataMatrix)
    row_2d = numpy.array(fullMatrix)
    gene_2d = numpy.array(geneMatrix)

    # Create random array for debugging
    # x = scipy.rand(40)
    # arr_2d = row_2d = scipy.zeros([40, 40])
    # for i in range(40):
    #     for j in range(40):
    #         arr_2d[i, j] = abs(x[i] - x[j])

    # calculate a distance matrix
    distMatrix = pdist(arr_2d)

    # convert the distance matrix to square form. The distance matrix
    # calculated above contains no redundancies, you want a square form
    # matrix where the data is mirrored across the diagonal.
    # distSquareMatrix = squareform(distMatrix)

    # calculate the linkage matrix
    linkageMatrix = linkage(distMatrix, method='single')
    # Y = linkage(arr_2d, method='single')  # Debug

    # create a dendrogram by using the dendrogram class
    dendro = dendrogram(linkageMatrix, orientation="right")
    # Z2 = dendrogram(Y)  # Debug data

    # Get order of leaves in dendrogram
    # leaves = leaves_list(linkageMatrix)

    # get the order of rows according to the dendrogram
    leaves = dendro['leaves']
    # idx2 = Z2['leaves']  # Debug Data

    # reorder the original data according to the order of the
    # dendrogram. Note that this slice notation is numpy specific.
    # It just means for every row specified in the 'leaves' array,
    # get all the columns. So it effectively remakes the data matrix
    # using the order from the 'leaves' array.
    # transformedData = arr_2d[leaves, :]
    # transformedData = transformedData[:, idx2]  # Debug Data
    transformedRows = row_2d[leaves, :]
    transformedGenes = gene_2d[leaves]


    # Debug Data, Write reordered data to image file
    # fig = pylab.figure(figsize=(8, 8))
    # ax1 = fig.add_axes([0.09, 0.1, 0.2, 0.6])
    # ax1.set_xticks([])
    # ax1.set_yticks([])
    # axmatrix = fig.add_axes([0.3, 0.1, 0.6, 0.6])
    # im = axmatrix.matshow(transformedData, aspect='auto', origin='lower', cmap=pylab.cm.YlGnBu)
    # axmatrix.set_xticks([])
    # axmatrix.set_yticks([])
    # axcolor = fig.add_axes([0.91, 0.1, 0.02, 0.6])
    # pylab.colorbar(im, cax=axcolor)
    # fig.show()
    # test = "/home/dezhang/heatmaps/dendrogram" + str(random.randint(100,999)) + ".png"
    # fig.savefig(test)

    return transformedRows, transformedGenes


def main(gene, DPI, heatmap_version):
    # Create copies of data to prevent weird global variable interactions
    DPI = copy.deepcopy(DPI)

    long_list = madhat(DPI, heatmap_version)
    long_list = copy.deepcopy(long_list)

    # Parse Response
    exprs = long_list[0]
    highest_val = long_list[1]
    highest_x = long_list[2]  # gives length of longest row to base matrix off of
    ngene = gene

    # Initialize 2D matrices to store data
    genereorder = []
    # matrix = [[None for g in range(len(exprs)/len(ngene))] for k in range(len(ngene))]
    matrix = [[None for g in range(highest_x+1)] for k in range(len(ngene))]  # stores expression values
    genematrix = []  # stores gene names
    # partialmatrix = [[None for g in range(len(exprs) / len(ngene))] for k in range(len(ngene))]
    partialmatrix = [[None for g in range(highest_x+1)] for k in range(len(ngene))]
    # studymatrix = [str() for g in range(len(exprs)/len(ngene))]
    studymatrix = [str() for g in range(highest_x+1)]  # stores study names
    # TODO Nested List Comprehension

    # Assign value to each coordinate on the matrix
    for i in range(len(exprs)):
        col = exprs[i][0]
        row = exprs[i][1]
        x_value = exprs[i][2]
        x_label = exprs[i][3]
        gene = exprs[i][4]
        matrix[row][col] = x_value
        partialmatrix[row][col] = (col, row, x_value)  # Data formatted for Highcharts
        if row == 0:
            studymatrix[col] = x_label
        if col == 0:
            genematrix.append(gene)

    # Cluster rows using matplotlib
    if len(genematrix) > 1:
        tempclust = cluster(matrix, partialmatrix, genematrix)
        genereorder = tempclust[1].tolist()
        matclust = tempclust[0].tolist()
        # Rewrite Y values based on clustering repositioning
        for z in range(len(matclust)):
            for h in range(len(matclust[z])):
                if matclust[z][h] is not None:
                    matclust[z][h] = list(matclust[z][h])
                    matclust[z][h][1] = z  # set y value as current Y
                else:
                    matclust[z][h] = (h, z, None)
    elif len(genematrix) <= 1:
        matclust = partialmatrix
        genereorder = genematrix

    matclust = [j for i in matclust for j in i]  # Flatten List

    # format as JSON object
    jedi = (matclust, studymatrix, genereorder, highest_val)

    # Return data to function
    return jedi

# main(gene, DPI, "day")  # Debug Function
