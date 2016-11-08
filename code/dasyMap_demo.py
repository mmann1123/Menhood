
"""
This scritp was created for dasymatric mapping
which can process both normalized and counted data based on one area of two time-point

@author: Shiyan, Qi
"""

import arcpy
import os
import csv
from dbfpy import dbf
import pandas as pd

#set up the environment and other things
inputSpace = raw_input("Please paste the working directory which store the intermidate files and results:")
arcpy.env.workspace = inputSpace
outPutFile = "TabulateIntersectionResult.dbf"
arcpy.env.outputMFlag = "Enable"
####################################################################################################################################
#%%
##part1: perform the tabulate intersection to get the tranformed percentage of census tracts
in_zone_features = "dc_dec2000.shp"#this is the pre-changed shp
zone_fields = ["GEO_ID",'dec00_vari',
       'dec00_va_1', 'dec00_va_2', 'dec00_va_3', 'dec00_va_4',
       'dec00_va_5', 'dec00_va_6', 'dec00_va_7', 'dec00_va_8',
       'dec00_va_9', 'dec00_va10', 'dec00_va11', 'dec00_va12',
       'dec00_va13', 'dec00_va14', 'dec00_va15', 'dec00_va16',
       'dec00_va17', 'dec00_va18', 'dec00_va19', 'dec00_va20',
       'dec00_va21', 'dec00_va22', 'dec00_va23', 'dec00_va24',
       'dec00_va25', 'dec00_va26', 'dec00_va27', 'dec00_va28',
       'dec00_va29', 'dec00_va30', 'dec00_va31', 'dec00_va32',
       'dec00_va33', 'dec00_va34', 'dec00_va35', 'dec00_va36',
       'dec00_va37', 'dec00_va38', 'dec00_va39', 'dec00_va40',
       'dec00_va41', 'dec00_va42', 'dec00_va43', 'dec00_va44',
       'dec00_va45', 'dec00_va46', 'dec00_va47', 'dec00_va48',
       'dec00_va49', 'dec00_va50', 'dec00_va51', 'dec00_va52',
       'dec00_va53', 'dec00_va54', 'dec00_va55', 'dec00_va56',
       'dec00_va57', 'dec00_va58', 'dec00_va59', 'dec00_va60',
       'dec00_va61', 'dec00_va62', 'dec00_va63', 'dec00_va64',
       'dec00_va65', 'dec00_va66', 'dec00_va67', 'dec00_va68',
       'dec00_va69', 'dec00_va70', 'dec00_va71', 'dec00_va72',
       'dec00_va73', 'dec00_va74', 'dec00_va75', 'dec00_va76',
       'dec00_va77', 'dec00_va78', 'dec00_va79', 'dec00_va80',
       'dec00_va81', 'dec00_va82', 'dec00_va83', 'dec00_va84',
       'dec00_va85', 'dec00_va86', 'dec00_va87', 'dec00_va88',
       'dec00_va89', 'dec00_va90', 'dec00_va91', 'dec00_va92',
       'dec00_va93', 'dec00_va94']
       #The attribute field or fields that will be used to define zones
                                                              # Fields could be more than those above. In this demo, we need those four fields
in_class_features = "DC_Census2010.shp"#this is after-changed shp
out_table = os.path.join(inputSpace, outPutFile)
class_fields = ["GEO_ID"]#The attribute field or fields used to define classes
try:
    os.remove(out_table)
except OSError:
    pass
arcpy.TabulateIntersection_analysis (in_zone_features, 
                               zone_fields, in_class_features, out_table, class_fields)
                              
print "complete"
################################################################################################################################################
#%%
#Part 2: this function convert the tabulate intersection result into csv                          
def dbf_to_csv(out_table):
    csv_fn = out_table[:-4]+ ".csv" #Set the table as .csv format
    try:
        os.remove(csv_fn)
    except OSError:
        pass
    with open(csv_fn,'wb') as csvfile: #Create a csv file and write contents from dbf
        in_db = dbf.Dbf(out_table)
        out_csv = csv.writer(csvfile)
        names = []
        for field in in_db.header.fields: #Write headers
            names.append(field.name)
        out_csv.writerow(names)
        for rec in in_db: #Write records
            out_csv.writerow(rec.fieldData)
        in_db.close()
dbf_to_csv(out_table)
####################################################################################################################################
#%%
#Remove the file we don't need (in case the name overlap)
csv_input = os.path.join(inputSpace, outPutFile[:-4]+ ".csv")
csv_output = os.path.join(inputSpace, outPutFile[:-4]+ "_10" + ".csv")
dbf_output = os.path.join(inputSpace, outPutFile[:-4]+ "_10" + ".dbf")
dbf_xml = dbf_output + ".xml"
try:
    os.remove(csv_output)
    os.remove(dbf_output)
    os.remove(dbf_xml)
except OSError:
    pass

##Part 3: Read the csv file and edite it
Table00 = pd.read_csv(csv_input)
#Declare lists and make sure to empty them, we will use these list to edit fields in next steps
#The fields which need to be edited are seperated into normalized or counted
#So normal -- normalized, count -- counted, and subsequently fields iteration will also based on the two types
normalField = []
del normalField[:]
normalValue = []
del normalValue[:]
normalValueAfter = []
del normalValueAfter[:]
countField = []
del countField[:]
countValue = []
del countValue[:]
countValueAfter = []
del countValueAfter[:]
TotalList2 = []
del TotalList2[:]
TotalList = list(Table00)#Make the table of 2000 year into a list
# Iteration of normalized and counted fields
i = 0
for fields in TotalList:
    TotalList2.append([i, fields]) # Create a dictionary 
    i += 1
print "Now we are going to choose whcih fields are normalized data, whcih fields are count-based data:"
print TotalList2
nonesense = raw_input("hit enter")
print "start from normalized field, please type in the corresponding number of each field:"
while True:#two while loop will record the numbers
    try:
        normal = raw_input("please enter the number here, only integer:  ")
        if normal == "end":
            print "finish recording"
            #return normalField
            break
        int(normal)
        normalField.append(normal)
        print "Thanks for typing, if there's no further number needed to be entered, please enter 'end'"
    except ValueError:
        print "Please only enter integers or 'end', let's try again, from the beginning"
        del normalField[:]
print "Now is count data field, please type in the corresponding number of each field:"
while True:
    try:
        count = raw_input("please enter the number here, only integer:  ")
        if count == "end":
            print "finish recording"
            #return countField
            break
        int(count)
        countField.append(count)
        print "Thanks for typing, if there's no further number needed to be entered, please enter 'end'"
    except ValueError:
        print "Please only enter integers or 'end', let's try again, from the beginning"
        del countField[:]
for normalKey in normalField:#use 'value' list to record the corresponding field name of the recorded number
    normalValue.append(TotalList2[int(normalKey)][1])# normalKey will show you 
for countKey in countField:
    countValue.append(TotalList2[int(countKey)][1])
for nv in normalValue: # nv -- normalized value
    Table00['B_'+nv[0:8]] = Table00[nv] #perfrom the calculation of change using pandas
    normalValueAfter.append('B_'+nv[0:8])#make a new list contain the new name of the hanged field
for cv in countValue: # counted value
    Table00['B_'+cv[0:8]] = Table00[cv] * Table00.PERCENTAGE * 0.01 #perfrom the calculation of change using pandas
    countValueAfter.append('B_'+cv[0:8])
    # B_ -- boundary 2010 

# We create dictionary because Aggregation function in Pandas will calculate data in this way
# for example: table.groupby[field].agg({'field1' : 'sum', 'field2' : 'mean'}), the part follow .agg are dictionaries
# that is why we need to write our data into this format and go to calculation step
normalDic = countDic = FidDic = {}
normalDic.clear()
countDic.clear()
FidDic.clear()
FidDic = {'FID_' : 'mean'}
normalDic = {nv:'sum' for nv in normalValueAfter}
countDic = {cv:'mean' for cv in countValueAfter}
normalDic.update(countDic)
normalDic.update(FidDic)
# Groupby the result by the sensus tract of year2010, sum the population, and average the income
Table10 = Table00.groupby(['NAME10'], as_index=False).agg(normalDic) # for example: table.groupby[field].agg({'field1' : 'sum', 'field2' : 'mean'})
#Table10.index.names = ['FID']    nv in normalValueAfter : 'sum', 'FID_' : 'mean', cv in countValue : 'mean'
Table10.to_csv(csv_output) # write the new table into csv
print "done"
####################################################################################################################################
#%%
## Part 4: join the table into shapefile fields
arcpy.env.workspace = inputSpace
inData = "demo10.shp"
inField = "NAME10"
joinTable = dbf_output#csv_output
joinField = "NAME10"
fieldList = list(Table10)
# change the csv into dbf and then join back to the shapefile
arcpy.CopyRows_management(csv_output, dbf_output)
arcpy.JoinField_management(inData, inField, joinTable, joinField, fieldList)

print("finished")
