#!/usr/bin/python


##----FUNCTIONS----##


def FILE2dict() :
    #intialize empty dictionary
    c = {}
    #open the file
    readFile = open('GI_2_Ensenble_human.txt', 'r')
    #iterate through file and store codon as key and aa as value
    for line in readFile:
        ln = line.split()
    for x in range(0,len(ln),2):
        key = ln[x]
        #check if key isn't in dictionary yet. If not, initialize new list in value position
        if key not in c:
            value = []
        value.append(ln[x+1].strip())
        c[key] = value
#gene numbers are keys, Ensembl IDs are values
    readFile.close()
    return c

def GENE2Ensembl(table, ID):

    #initialize output
    ID2 = []
    #iterate through table
    for key in table:

        #If a match, it will return the Ensembl ID, else return none
        if ID == key:
            #print key, table[key]
            ID2.append(table[key])

    print("Ensembl ID:", ID2)

def Ensembl2GENE(table, ID):

    #initialize output as list
    ID2 = []
    for key in table:

        for pos in table[key]:
            if ID == pos:
                ID2.append(key)

    print("Gene ID:", ID2)

##----MAIN CODE----##

G2Edict=FILE2dict()


ans = input("Which ID type are you entering? (1=Gene ID / 2=Ensembl ID):     ")

#ID = input("Enter the ID:       ")
#IDs are stored as strings in dictionary
#ID = str(ID)

if ans == 1:
    ID = input("Enter the ID:       ")
    ID = str(ID)
    GENE2Ensembl(G2Edict, ID)
if ans == 2:
    ID = input("Enter the ID:       ")
    ID = str(ID)
    Ensembl2GENE(G2Edict, ID)


##----END OF CODE----##
