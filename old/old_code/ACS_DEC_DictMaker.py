# Coder: Max
# Code: ACS_DEC_DictMaker.py
# Purpose: Code that creates Dict of GEO.Id and Id for ACS and DE cvs

#%% Libraries to Import 

import pandas as pd

#%% 

# Lists of csvs to make lists from
ACS_DEC_csvList = ["ACS_10_5YR_DP05_metadata"] # list of cvs
ACS_DEC_dictList = [] # list of dictionaries with GEO.id and id inside

for csv in ACS_DEC_csvList: 

    # read in csv as dataframe

    ACS_DEC_df = pd.read_csv("/Users/maxgrossman/Desktop/ACS_DEC_CSV/" + csv + ".csv")

    # Make GEO.id list and ID list and combine into dictionary

    # Set lists to tolist() function on the GEO.id and Id columns in csv
    GEOid_List = ACS_DEC_df["GEO.id"].tolist()
    id_List = ACS_DEC_df["Id"].tolist()

    # trim off undeeded items in list

    GEOid_List.pop(0)
    GEOid_List.pop(0)
    id_List.pop(0)
    id_List.pop(0)

    # Create Dictionary with map, zip, and dict functions

    GEOid_id_Dict = dict(zip(GEOid_List,id_List))
    ACS_DEC_dictList.append(GEOid_id_Dict)
    print ACS_DEC_dictList
    


