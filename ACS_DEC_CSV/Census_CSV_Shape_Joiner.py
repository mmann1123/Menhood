# Coder: Max Grossman
# Code: ACS_DE_joiner.py
# Purpose: Grab user defined columns from ACS/DE and 
#          join to census tract shapefile.

#%% import libaries 

import pandas as pd
import arcpy
import json
arcpy.env.overwriteOutput=True
#%% Lists Needed to direct to selected CSVs

# List of categories that defines the variable cateogries to choose from   
VariableCategoryList = ["Demographics","Education"] 

# Lists of ACS and DEC csvs for each respective varaible type
# Both lists sequenced metadata csv followed by variable csv for each year
# For ACS variables, the [0-1] items are '09, [2-3] are '10, [4-5] are '11
# [6-7] are '12, and [8-9] '13 

# For DEC variables, the sequence is simply [0] metadata, [1] variable 

ACS_Demographics = ["ACS_09_5YR_DP5YR5_metadata.csv","ACS_10_5YR_DP05_metadata.csv", 
                    "ACS_10_5YR_DP05_with_ann.csv", "ACS_11_5YR_DP05_metadata.csv", 
                    "ACS_11_5YR_DP05_with_ann.csv","ACS_12_5YR_DP05_metadata.csv", 
                    "ACS_12_5YR_DP05_with_ann.csv","ACS_13_5YR_DP05_metadata.csv", 
                    "ACS_13_5YR_DP05_with_ann.csv"]
DEC_Demographics = ["DEC_00_SF1_DP1_metadata.csv", "DEC_00_SF1_DP1_with_ann.csv"]

ACS_Education = ["ACS_09_5YR_S1501_metadata.csv","ACS_09_5YR_S1501_with_ann.csv",
                 "ACS_10_5YR_S1501_metadata.csv","ACS_10_5YR_S1501_with_ann.csv",
                 "ACS_11_5YR_S1501_metadata.csv","ACS_11_5YR_S1501_with_ann.csv",
                 "ACS_12_5YR_S1501_metadata.csv","ACS_12_5YR_S1501_with_ann.csv",
                 "ACS_13_5YR_S1501_metadata.csv","ACS_13_5YR_S1501_with_ann.csv"]
DEC_Education = ["DEC_00_SF3_QTP20_metadata.csv","DEC_00_SF3_QTP20_with_ann.csv"]

ACS_Employment = ["ACS_09_5YR_DP5YR3_metadata.csv","ACS_09_5YR_DP5YR3_with_ann.csv",
                  "ACS_10_5YR_DP5YR3_metadata.csv","ACS_10_5YR_DP5YR3_with_ann.csv",
                  "ACS_11_5YR_DP5YR3_metadata.csv","ACS_11_5YR_DP5YR3_with_ann.csv",
                  "ACS_12_5YR_DP5YR3_metadata.csv","ACS_12_5YR_DP5YR3_with_ann.csv",
                  "ACS_11_5YR_DP5YR3_metadata.csv","ACS_11_5YR_DP5YR3_with_ann.csv"]
DEC_Employment = ["DEC_00_SF3_DP3_metadata.csv","DEC_00_SF3_DP3_with_ann.csv"]

ACS_HouseValue = ["ACS_09_5YR_B25075_metadata.csv","ACS_09_5YR_B25075_with_ann.csv",
                  "ACS_10_5YR_B25075_metadata.csv","ACS_10_5YR_B25075_with_ann.csv",
                  "ACS_11_5YR_B25075_metadata.csv","ACS_11_5YR_B25075_with_ann.csv",
                  "ACS_12_5YR_B25075_metadata.csv","ACS_12_5YR_B25075_with_ann.csv",
                  "ACS_13_5YR_B25075_metadata.csv","ACS_13_5YR_B25075_with_ann.csv"]
DEC_HouseValue = ["DEC_00_SF3_H074_metadata.csv","DEC_00_SF3_H074_with_ann.csv"]

ACS_MedianIncome = ["DEC_00_SF3_P053_metadata.csv","DEC_00_SF3_P053_with_ann.csv"]
DEC_MedianIncome = ["ACS_09_5YR_B19013_metadata.csv","ACS_09_5YR_B19013_with_ann.csv",
                    "ACS_10_5YR_B19013_metadata.csv","ACS_10_5YR_B19013_with_ann.csv",
                    "ACS_11_5YR_B19013_metadata.csv","ACS_11_5YR_B19013_with_ann.csv",
                    "ACS_12_5YR_B19013_metadata.csv","ACS_12_5YR_B19013_with_ann.csv",
                    "ACS_13_5YR_B19013_metadata.csv","ACS_13_5YR_B19013_with_ann.csv"]

ACS_MedianRent = ["DEC_00_SF3_H070_metadata.csv","DEC_00_SF3_H070_with_ann.csv"]
DEC_MedianRent = ["ACS_09_5YR_B25064_metadata.csv","ACS_09_5YR_B25064_with_ann.csv",
                  "ACS_10_5YR_B25064_metadata.csv","ACS_10_5YR_B25064_with_ann.csv",
                  "ACS_11_5YR_B25064_metadata.csv","ACS_11_5YR_B25064_with_ann.csv",
                  "ACS_12_5YR_B25064_metadata.csv","ACS_12_5YR_B25064_with_ann.csv",
                  "ACS_13_5YR_B25064_metadata.csv","ACS_13_5YR_B25064_with_ann.csv"]

    
# List of csvs follows same order as ACS_DEC_CategoryList categories, which is: 
# Demographics, Education...
# List follows sequence of ACS_VarCategory, DEC_VariableCategory for all 
# relevant variable types

ACS_DEC_csvList = [ACS_Demographics,DEC_Demographics,
                   ACS_Education,DEC_Education,
                   ACS_Employment,DEC_Employment,
                   ACS_HouseValue,DEC_HouseValue,
                   ACS_MedianIncome,DEC_MedianIncome] # list of cvs

ACS_DEC_dictList = [] # list of dictionaries with GEO.id and id inside


#%% CSV Selector Function

# intializing global variables
VariableCategory = " "; Dataset = " "; YearDecision = " "; CSV_FilePath = ""
Year = " "

# CSV_Selector will allow user to make either a list for ACS, DE, or both
def CSV_Selector(VariableCategory, Dataset, YearDecision,Year,CSV_FilePath):
    
    # User Provides the file path to their variables
    CSV_FilePath = str(raw_input(
    "Please provide the file path to your ACS & DEC csv files:" + "\n\n>"))
    
    # print back file path to user
    print "\n" + "File Path:" + "\n\n" + CSV_FilePath
    
  
    # Decision to choose the data category of interest
    CategoryDecision = str(raw_input(
    "Which data category interests you?" + "\n\n"
    "Type 1 for " + VariableCategoryList[0] + "\n"
    "Type 2 for " + VariableCategoryList[1] + "\n\n> "))
    
    # CategoryDecision is set to variable category user chose
    if CategoryDecision == "1":
        VariableCategory = VariableCategoryList[0]
    if CategoryDecision == "2":
        VariableCategory = VariableCategoryList[1]
    
    # Decision to choose between ACS or DEC dataset
    DatasetDecision = str(raw_input(
    "Which data set interests you?" + "\n\n"
    "Type 1 for ACS" + "\n"
    "Type 2 for DEC" + "\n\n> "))
    
    if DatasetDecision == "1":
        
        # Dataset, a returned val is set to ACS 
        Dataset = "ACS"
        
        # When ACS, a year must be defined as there are multiple years
        YearDecision = str(raw_input(
        "Which ACS year interests you?" + "\n\n"
        "Type 1 for '09" + "\n"
        "Type 2 for '10" + "\n"
        "Type 3 for '11" + "\n"
        "Type 4 for '12" + "\n"
        "Type 5 for '13" + "\n\n> "))
        
        if YearDecision == "1":
            Year = "09"
        if YearDecision == "2":
            Year = "10"
        if YearDecision == "3":
            Year = "11"
        if YearDecision == "4":
            Year = "12"
        if YearDecision == "5":
            Year = "13"
            
        
    if DatasetDecision == "2":

        Dataset = "DEC"
        
        #arbitrary returend value because year is not important for DEC
        
        YearDecision = " "
        Year = "00"
    
    return VariableCategory, Dataset, YearDecision, Year, CSV_FilePath

#%% Run CSV Selector

VariableCategory,Dataset,YearDecision,Year,CSV_FilePath = CSV_Selector(VariableCategory,Dataset,YearDecision,Year,CSV_FilePath)

print "\n" + "Variable Type: " +  VariableCategory + "\n" + "Dataset: " + Dataset + "\n" + "Year: " + "20" + Year
raw_input(">")

#%% function that uses values returned from CSV_Selector make dict from metadata CSV

# initialize global dictionary

GEOid_id_Dict = {}
ACS_DEC_df = " "

def VariableDictionary_Maker(VariableCategory,Dataset,YearDecision,GEOid_id_Dict,ACS_DEC_df,CSV_FilePath):
    
    VariableCategory = VariableCategory
    Dataset = Dataset    
    YeaDecision = YearDecision
    
    if VariableCategory == VariableCategoryList[0] and Dataset == "DEC":
    
        # read in csv as dataframe

        ACS_DEC_df_meta = pd.read_csv(CSV_FilePath + "\\" + DEC_Demographics[0])
        ACS_DEC_df = pd.read_csv(CSV_FilePath + "\\" + DEC_Demographics[1])

        # Make GEO.id list and ID list and combine into dictionary

        # Set lists to tolist() function on the GEO.id and Id columns in csv
        
        GEOid_List = ACS_DEC_df_meta["GEO.id"].tolist()
        id_List = ACS_DEC_df_meta["Id"].tolist()
    
    
        # Create Dictionary with map, zip, and dict functions

        GEOid_id_Dict = dict(zip(GEOid_List,id_List))
                    
        return GEOid_id_Dict,ACS_DEC_df
        
    if VariableCategory == VariableCategoryList[0] and Dataset == "ACS" and YeaDecision == "1":   
        
        # read in csv as dataframe

        ACS_DEC_df_meta = pd.read_csv(CSV_FilePath + "\\" + ACS_Demographics[0])
        ACS_DEC_df = pd.read_csv(CSV_FilePath + "\\" + ACS_Demographics[1])
        # Make GEO.id list and ID list and combine into dictionary

        # Set lists to tolist() function on the GEO.id and Id columns in csv
        GEOid_List = ACS_DEC_df_meta["GEO.id"].tolist()
        id_List = ACS_DEC_df_meta["Id"].tolist()
    
        # Create Dictionary with map, zip, and dict functions

        GEOid_id_Dict = dict(zip(GEOid_List,id_List))
    
    
        # Trim off unneeded margin of error variables
    
        for key, val in GEOid_id_Dict.items():
            if val.startswith('Percent; Margin of Error') :
                del GEOid_id_Dict[key]
            if val.startswith('Number; Margin of Error') :
                del GEOid_id_Dict[key]    
    
        return GEOid_id_Dict,ACS_DEC_df
    
    if VariableCategory == VariableCategoryList[0] and Dataset == "ACS" and YeaDecision == "2":   
        
        # read in csv as dataframe

        ACS_DEC_df_meta = pd.read_csv(CSV_FilePath + "\\" + ACS_Demographics[2])
        ACS_DEC_df = pd.read_csv(CSV_FilePath + "\\" + ACS_Demographics[3])
        # Make GEO.id list and ID list and combine into dictionary

        # Set lists to tolist() function on the GEO.id and Id columns in csv
        GEOid_List = ACS_DEC_df_meta["GEO.id"].tolist()
        id_List = ACS_DEC_df_meta["Id"].tolist()
    
        # Create Dictionary with map, zip, and dict functions

        GEOid_id_Dict = dict(zip(GEOid_List,id_List))
    
    
        # Trim off unneeded margin of error variables
    
        for key, val in GEOid_id_Dict.items():
            if val.startswith('Percent Margin of Error') :
                del GEOid_id_Dict[key]
            if val.startswith('Estimate Margin of Error') :
                del GEOid_id_Dict[key]    
            if val.startswith('Margin of Error'):
                del GEOid_id_Dict[key]
                
        return GEOid_id_Dict,ACS_DEC_df
    
    if VariableCategory == VariableCategoryList[0] and Dataset == "ACS" and YeaDecision == "3":   
        
        # read in csv as dataframe

        ACS_DEC_df_meta = pd.read_csv(CSV_FilePath + "\\" +ACS_Demographics[4])
        ACS_DEC_df = pd.read_csv(CSV_FilePath + "\\" + ACS_Demographics[5])
        
        # Make GEO.id list and ID list and combine into dictionary

        # Set lists to tolist() function on the GEO.id and Id columns in csv
        GEOid_List = ACS_DEC_df_meta["GEO.id"].tolist()
        id_List = ACS_DEC_df_meta["Id"].tolist()
    
        # Create Dictionary with map, zip, and dict functions

        GEOid_id_Dict = dict(zip(GEOid_List,id_List))
    
    
        # Trim off unneeded margin of error variables
    
        for key, val in GEOid_id_Dict.items():
            if val.startswith('Percent Margin of Error') :
                del GEOid_id_Dict[key]
            if val.startswith('Estimate Margin of Error') :
                del GEOid_id_Dict[key]    
            if val.startswith('Margin of Error'):
                del GEOid_id_Dict[key]
    
        return GEOid_id_Dict,ACS_DEC_df
        
    if VariableCategory == VariableCategoryList[0] and Dataset == "ACS" and YeaDecision == "4":   
        
        # read in csv as dataframe

        ACS_DEC_df_meta = pd.read_csv(CSV_FilePath + "\\" + ACS_Demographics[6])
        ACS_DEC_df = pd.read_csv(CSV_FilePath + "\\" + ACS_Demographics[7])
        
        # Make GEO.id list and ID list and combine into dictionary

        # Set lists to tolist() function on the GEO.id and Id columns in csv
        GEOid_List = ACS_DEC_df_meta["GEO.id"].tolist()
        id_List = ACS_DEC_df_meta["Id"].tolist()
    
        # Create Dictionary with map, zip, and dict functions

        GEOid_id_Dict = dict(zip(GEOid_List,id_List))
    
    
        # Trim off unneeded margin of error variables
    
        for key, val in GEOid_id_Dict.items():
            if val.startswith('Percent Margin of Error') :
                del GEOid_id_Dict[key]
            if val.startswith('Estimate Margin of Error') :
                del GEOid_id_Dict[key]    
            if val.startswith('Margin of Error'):
                del GEOid_id_Dict[key]
    
        return GEOid_id_Dict,ACS_DEC_df
    
    if VariableCategory == VariableCategoryList[0] and Dataset == "ACS" and YeaDecision == "5":   
        
        # read in csv as dataframe

        ACS_DEC_df_meta = pd.read_csv(CSV_FilePath + "\\" + ACS_Demographics[8])
        ACS_DEC_df = pd.read_csv(CSV_FilePath + "\\" + ACS_Demographics[9])

        # Make GEO.id list and ID list and combine into dictionary

        # Set lists to tolist() function on the GEO.id and Id columns in csv
        GEOid_List = ACS_DEC_df_meta["GEO.id"].tolist()
        id_List = ACS_DEC_df_meta["Id"].tolist()
    
        # Create Dictionary with map, zip, and dict functions

        GEOid_id_Dict = dict(zip(GEOid_List,id_List))
    
    
        # Trim off unneeded margin of error variables
    
        for key, val in GEOid_id_Dict.items():
            if val.startswith('Percent Margin of Error') :
                del GEOid_id_Dict[key]
            if val.startswith('Estimate Margin of Error') :
                del GEOid_id_Dict[key]    
            if val.startswith('Margin of Error'):
                del GEOid_id_Dict[key]
    
        return GEOid_id_Dict,ACS_DEC_df
    
#%% Run VariableDictionary_Maker
    
GEOid_id_Dict,ACS_DEC_df = VariableDictionary_Maker(VariableCategory,Dataset,YearDecision,GEOid_id_Dict,ACS_DEC_df,CSV_FilePath)    


#%% Allow User to select variables of interest with VariableSelector function
UsrSelVarLst = []   
GEOid_id_Dict_UsrSel = {}
GEOid_id_List_UsrSel = []
    
def VariableSelector(GEOid_id_Dict,UsrSelVarLst,GEOid_id_Dict_UsrSel,GEOid_id_List_UsrSel,VariableCategory,CSV_FilePath):
    
    # Initialize GEOid_id_Dict,UsrSelVarLst
    GEOid_id_Dict = GEOid_id_Dict
    UsrSelVarLst = UsrSelVarLst    
    GEOid_id_Dict_UsrSel = GEOid_id_Dict_UsrSel
    GEOid_id_List_UsrSel = GEOid_id_List_UsrSel

    #print variables user can select from.    
    for value in GEOid_id_Dict:
        print GEOid_id_Dict[value]
    
    # Use While loop to alow user to select variables of interest
    while True:
        SelectVar = raw_input("Please type a variable of interest.\n>")
        UsrSelVarLst.append(SelectVar)
        finished = raw_input(
        "Would you Like to select more variables?\nType 1 for Yes\nType 2 for No\n> ")
        if finished == "1":
            for value in GEOid_id_Dict:
                print GEOid_id_Dict[value]
        if finished == "2":
            break
    
    # iterate over values in GEOid_id_Dict. If UsrSelVarLst item is
    # the same as GEOid_id_Dict[value], append to new select dictionary
    for value in GEOid_id_Dict:
        if  GEOid_id_Dict[value] in UsrSelVarLst:
            GEOid_id_Dict_UsrSel.update({value : GEOid_id_Dict[value]})
            
    # write GEOid_id_Dict to text File kept in directory
            
    json.dump(GEOid_id_Dict_UsrSel, open(CSV_FilePath + "\\" + VariableCategory + ".txt",'w'))
    
    # iterate over keys and values in GEOid_id_Dict_UsrSel
    # append keys to GEOid_id_List. This is needed to make subset CSV
    for key,val in GEOid_id_Dict_UsrSel.items():
        GEOid_id_List_UsrSel.append(key)    
    
    # Unique id columns not added to lists are lost in ablove functions
    # that need to be added to GEOid_id_List_UsrSel to make subset csv. 
    CensusTractColumns = ["GEO.id","GEO.id2","GEO.display-label"]
    
    # extend GEOid_id_List_UsrSel with CensusTractColumns

    GEOid_id_List_UsrSel.extend(CensusTractColumns)

    return GEOid_id_Dict_UsrSel, GEOid_id_List_UsrSel

    
#%% Set GEOid_id_Dict_UsrSel,GEOid_id_List_UsrSel to  VariableSelector 
    
GEOid_id_Dict_UsrSel,GEOid_id_List_UsrSel = VariableSelector(GEOid_id_Dict,UsrSelVarLst,GEOid_id_Dict_UsrSel,GEOid_id_List_UsrSel,VariableCategory)

# print the variables the user selected
print "Your Variable GEO.ids are:" + "\n"
for GEOid in GEOid_id_List_UsrSel:
    if GEOid.startswith("H"):
        print GEOid
#%% CSVCopier will use selections to make copy csv with only the select variables included

# initialize the UserVariableCSV needed for the function
UserVariablesDf = " "


def CSVCopier(GEOid_id_List_UsrSel,UserVariablesDf,ACS_DEC_df):
    UserVariablesDf = UserVariablesDf
    UserVariablesDf = ACS_DEC_df[GEOid_id_List_UsrSel]
    print "Below is a peak at your variables:" + "\n"
    print UserVariablesDf.head()
    return  UserVariablesDf

#%% Set UserVariablesCSV to CSVCopier 

UserVariablesDf = CSVCopier(GEOid_id_List_UsrSel,UserVariablesDf,ACS_DEC_df)


#%% Make UserVariablesCSV into dfb file to join to shapefile

UserShapefile = " "
UserVariablesCSV = " "
CensusLyr = " "

#def NewCensusShpMaker(UserVariablesCSV, UserVariablesDf, CensusLyr, UserShapefile, Year, Dataset, VariableCategory):

# Create UniqueID for lyr,csv,dbf,shp    
    
UniqueId = "DC_" + Dataset + Year + VariableCategory     

# User provides file path to shapefile    
UserShapefile = str(raw_input("Please Provide the file path that includes the shapefile to join your selected variables to:" "\n\n" + ">"))    
    
# User provides file path for new shapefile
NewUsrShapefile = str(raw_input("Please provide the file path to send your new shapefile to:" + "\n\n" + ">" )) 
LyrFilePath = NewUsrShapefile + "\\" + UniqueId + ".lyr"

    
# Make New Layer from the DC Census Tract Shapefile   
 
CensusLyr = arcpy.MakeFeatureLayer_management(UserShapefile, LyrFilePath)
    
# List we will use to find all rows in UserVaribalesCSV NOT in Census Lyr    
   
NotIncluded_GEO_IDList = []

# List of sorted GEO_ID in the UserVariablesCSV

UsrVarGEO_IDList = UserVariablesDf['GEO.id'].tolist()
UsrVarGEO_IDList.pop(0)
UsrVarGEO_IDList = sorted(UsrVarGEO_IDList)
for GEO_ID in UsrVarGEO_IDList:
    GEO_ID = str(GEO_ID)
    
# Search through CensusLyr to make list of all GEO_Ids in Census Lyr
    
with arcpy.da.SearchCursor(CensusLyr, ['GEO_ID']) as Cursor:
    LyrGEO_IdList = sorted(({str(row[0]) for row in Cursor}))
    
# Iterate through each item in csvGEO_IDList to see if in LyrGEO_IDList
    
for GEO_ID in LyrGEO_IdList:
    if GEO_ID not in UsrVarGEO_IDList:
        print GEO_ID
        NotIncluded_GEO_IDList.append(GEO_ID)
    
# Use the NotInlcuded List to make UserVariablesCSV only include those
# Rows with GEO_ID in the Shapefile it will be joined to.

UserVariablesDf = UserVariablesDf['GEO.id' != [NotIncluded_GEO_IDList]]
CSVName = CSV_FilePath+"\\"+UniqueId+".csv"
UserVariablesDf.to_csv(CSVName)

# converts UserVariablesCSV to dbf
    
DBF_Output = UniqueId + "UserVarDBF.dbf"
arcpy.TableToTable_conversion(CSVName,NewUsrShapefile,DBF_Output)
UserVariablesDBF = NewUsrShapefile + "\\" + UniqueId + "UserVarDBF.dbf"
    
# Get rid off all fields we do not need before join.
    
fields = arcpy.ListFields(UserVariablesDBF)
    
# Create list of field names, then add the GEO.id and variables to second
# List
    
fieldsList = []

for field in fields:
    fieldsList.append(field.name)
        
fieldsListsub = []
    
for f in fieldsList:
    if f.startswith('H'):
        fieldsListsub.append(f)
    if f.startswith('GEO_id'):
        fieldsListsub.append(f)
   
# Join DBF to Layer and save it to Lyr
   
CensusLyr = arcpy.JoinField_management (CensusLyr,"GEO_ID", UserVariablesDBF ,"GEO_id", fieldsListsub)
    
# CensusLyr = arcpy.AddJoin_management (CensusLyr, "GEO_ID", UserVariablesDBF ,"GEO_id")

# List the fields. Pick those that start with H
# Make that into a list 
# Do JoinField.


CensusLyr = arcpy.CopyFeatures_management(CensusLyr,NewUsrShapefile+"\\"+UniqueId+".shp")
CensusLyrPath = NewUsrShapefile+"\\"+UniqueId+".shp"

# Lastly, make field alias for each fo the census fields
    
# Make List of long id names. these will become alias
VariableAliasList = UserVariablesDf.loc[0].tolist()

for Var in VariableAliasList:
    if Var.startswith("G"):
        VariableAliasList.pop()

    
#Make List of fields in new layer
#fieldList = arcpy.ListFields(CensusLyr)

#fields_List = []

#for field in fields:
    fields_List.append(field.name)
    
#for f in fields_List:
    if f.startswith("G"):
        fields_List.pop()

#for alias in VariableAliasList:
    for field in fieldList:
         if alias == field.name:
             arcpy.AlterField_management(CensusLyr,field.name,"#",alias)
        
   # return CensusLyr

#%% Set CensusLyr to NewCensusShpMaker

# CensusLyr = NewCensusShpMaker(UserVariablesCSV, UserVariablesDf, CensusLyr, UserShapefile, Year, Dataset, VariableCategory)