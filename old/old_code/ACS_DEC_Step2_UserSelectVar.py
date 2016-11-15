# Coder: Max Grossman
# Code: ACS_DEC_SelectVar_csvMaker
# Purposee: Grab select variables from ACS/DEC csv given to make new sub-csv  

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
    "Would you Like to select more variables?\nType 1 for Yes\nType 2 for no\n> ")
    if finished == "2":
        break
        
#%% Take User selections and create new copy dictionary of those selected

    
# Use for loop and if statement to create new dictionary

GEOid_id_dict_UsrSel = {}

for value in GEOid_id_dict:
    if  GEOid_id_dict[value] in UsrSelVarLst:
        GEOid_id_dict_Usr_Sel.update({value : GEOid_id_dict[value]})
     
#%% Use This User Selected List to make copy of census CSV
     

    