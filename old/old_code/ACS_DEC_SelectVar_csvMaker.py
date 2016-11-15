# Coder: Max Grossman
# Code: ACS_DEC_SelectVar_csvMaker
# Purposee: Grab select variables from ACS/DEC csv given to make new sub-csv  

# numbers corresponding with the csv we want to grab from 
count = 0 
ACS_DEC_selectdict = ACS_DEC_dictList[count]

# List of csvs to select from that we will pick our subset of GEO.ids from 
ACS_DEC_csvList = ["ACS_10_5YR_DP05_metadata","DEC_00_SF1_DP1_metadata"]

# The list of GEOid's we will go after that we got from the ACS_DEC_selectdict

ACS_DEC_selectGEOID_List = ACS_DEC_selectdict.keys()

df.to_csv(dfuser + "_"+ ACS_DEC_csvList[count] + "_sub"+".csv")
df = df[["GEO.id",ACS_DEC_dictList[count]]]
