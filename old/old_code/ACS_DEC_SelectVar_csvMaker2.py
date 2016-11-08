# Coder: Max Grossman
# Code: ACS_DEC_SelectVar_csvMaker
# Purposee: Grab select variables from ACS/DEC csv given to make new sub-csv  

#%% Use for-loop to print all values from list 
    
#for value in GEOid_id_Dict:
#    print GEOid_id_Dict[value]
    
# have user input the variable name of interest with while&for loop

# List of variables user will select

SelectVariableList = []

# Variable while statement will evaluate true or not true

MoreVarSelect = True

# Use While loop to allow user to select variables of interest

while MoreVarSelect == True:
    SelectVar = raw_input("Please type a variable of interest.\n>")
    SelectVariableList.append(SelectVar)
    finished = str(raw_input(
    "Would you Like to select more variables?\nType 1 for Yes\nType 2 for no\n> "))
    if finished == "1":
        MoreValSelect = False
    if finished == "2":
        MoreVarSelect = True
        
# Use if

if 
    
        
        
    
    