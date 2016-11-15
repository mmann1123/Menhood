# Coder: Max
# Code: ACS_DEC_Step1_DictMaker.py
# Purpose: Code that creates Dict of GEO.Id and Id for ACS and DE cvs

#%% Libraries to Import 

import pandas as pd
#import arcpy

#%% Create Dictionary with GEO.id key and id values

# Lists of ACS and DEC csvs for each respective varaible type
# Both lists sequenced metadata csv followed by variable csv for each year
# For ACS variables, the [0-1] items are '09, [2-3] are '10, [4-5] are '11
# [6-7] are '12, and [8-9] '13 
# For DEC variables, the sequence is simply [0] metadata, [1] variable 
ACS_Demographics = ["ACS_09_5YR_DP05_metadata.csv", "ACS_09_5YR_DP05_with_ann.csv", "ACS_10_5YR_DP05_metadata.csv", "ACS_10_5YR_DP05_with_ann.csv", "ACS_11_5YR_DP05_metadata.csv", "ACS_11_5YR_DP05_with_ann.csv","ACS_12_5YR_DP05_metadata.csv", "ACS_12_5YR_DP05_with_ann.csv","ACS_13_5YR_DP05_metadata.csv", "ACS_13_5YR_DP05_with_ann.csv"]
DEC_Demographics = ["DEC_00_SF1_DP1_metadata.csv", "DEC_00_SF1_DP1_with_ann.csv"]
# List of csvs follows same order as ACS_DEC_CategoryList categories, which is: 
# Demographics, Education...
# List follows sequence of ACS_VarCategory, DEC_VariableCategory for all 
# relevant variable types
ACS_DEC_csvList = [ACS_Demographics,DEC_Demographics] # list of cvs
ACS_DEC_dictList = [] # list of dictionaries with GEO.id and id inside

for csv in ACS_DEC_csvList: 

    # read in csv as dataframe

    ACS_DEC_df_meta = pd.read_csv("/Users/maxgrossman/Desktop/ACS_DEC_CSV/" + csv + ".csv")

    # Make GEO.id list and ID list and combine into dictionary

    # Set lists to tolist() function on the GEO.id and Id columns in csv
    GEOid_List = ACS_DEC_df_meta["GEO.id"].tolist()
    id_List = ACS_DEC_df_meta["Id"].tolist()
    
    
    # Create Dictionary with map, zip, and dict functions

    GEOid_id_Dict = dict(zip(GEOid_List,id_List))
    
    
    
    # If handling an ACS csv, trim off margin of error nonsense.  
    
    if csv.startswith("ACS"):
        
        for key, val in GEOid_id_Dict.items():
            if val.startswith('Percent Margin') :
                del GEOid_id_Dict[key]
            if val.startswith('Estimate Margin') :
                del GEOid_id_Dict[key]
       

print GEOid_id_Dict

ACS_DEC_dictList.append(GEOid_id_Dict)
        
#%% Allow Users to select variables
    
for value in GEOid_id_Dict:
    print GEOid_id_Dict[value]
    
# have user input the variable name of interest with while&for loop

# List of variables user will select

UsrSelVarLst = []

# Use While loop to allow user to select variables of interest

while True:
    SelectVar = raw_input("Please type a variable of interest.\n>")
    UsrSelVarLst.append(SelectVar)
    finished = raw_input(
    "Would you Like to select more variables?\nType 1 for Yes\nType 2 for No\n> ")
    if finished == "2":
        break
        
#%% Take User selections and create new copy dictionary of those selected

# Empty Dictionary to copy selected values to
GEOid_id_Dict_UsrSel = {}

# Empty Dictionary to make copy of dict keys. This is used for making subset
# csv 

GEOid_id_List_UsrSel = []
    
# Use for loop and if statement to create new dictionary

for value in GEOid_id_Dict:
    if  GEOid_id_Dict[value] in UsrSelVarLst:
        GEOid_id_Dict_UsrSel.update({value : GEOid_id_Dict[value]})

# Use for loop to make list of keys, in new dict. We do this because
# these keys are the column heads in the census csv files.

for key,val in GEOid_id_Dict_UsrSel.items():
    GEOid_id_List_UsrSel.append(key)

# This is a list of some column heads that were taken from the 
# metadata file. I then extend the GEOid_id_List_UsrSel with this list

NeededColumns = ["GEO.id","GEO.id2","GEO.display-label"]

GEOid_id_List_UsrSel.extend(NeededColumns)

print GEOid_id_List_UsrSel


#%% Use selections to make copy csv with only the select variables included


ACS_DEC_df = pd.read_csv("/Users/maxgrossman/Desktop/ACS_DEC_CSV/DEC_00_SF1_DP1_with_ann.csv")

UserVariablesCSV = ACS_DEC_df[GEOid_id_List_UsrSel]

print UserVariablesCSV.head()

#%% Make Feature Layer of DC Census shape to add new CSV columns to.

arcpy.MakeFeatureLayer_management()