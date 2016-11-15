
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
in_zone_features = "dec2000_5.shp"#this is the pre-changed shp
zone_fields = ["GEO_ID", 'dec_ma',
 'dec_tp',
 'dec_mp',
 'dec_mpp',
 'dec_fp',
 'dec_fpp',
 'dec_aap',
 'dec_aapp',
 'dec_lf',
 'dec_lfp',
 'dec_em',
 'dec_emp',
 'dec_ue',
 'dec_uep',
 'dec_nlf',
 'decnlfp',
 'dec_flf',
 'dec_flfp',
 'd_e1824',
 'd_e24lm',
 'd_e24lf',
 'd_nh24l',
 'd_nh24lm',
 'd_nh24lf',
 'd_hs24l',
 'd_hs24lm',
 'd_hs24lm.1',
 'd_as24l',
 'd_as24lm',
 'd_as24lf',
 'd_ba24l',
 'd_ba24lm',
 'd_ba24lf',
 'd_hs24l.1',
 'd_hs34lm',
 'd_hs34lf',
 'd_ba34l',
 'd_ba34lm',
 'd_ba34lf',
 'd_hs44l',
 'd_hs44lm',
 'd_hs44lf',
 'dec_10kl',
 'dec_1015',
 'dec_1519',
 'dec_2025',
 'dec_2530',
 'dec_3035',
 'dec_3540',
 'dec_4050',
 'dec_5059',
 'dec_6069',
 'dec_7079',
 'dec_8089',
 'dec_9099',
 'dec_1124',
 'dec_12549',
 'dec_15074',
 'dec_17599',
 'dec_20049',
 'dec_25099',
 'dec_30099',
 'dec_40099',
 'dec_500749',
 'dec_750999',
 'dec_1000',
 'DEC_MGRp',
 'DEC_MOC',
 'DEC_FOC',
 'DEC_MRC',
 'DEC_FRC',
 'DEC_MO',
 'DEC_FO',
 'DEC_MR',
 'DEC_FR',
 'DEC_OO',
 'DEC_RO',
 'DEC_SSM',
 'DEC_SSMF',
 'DEC_SSF',
 'DEC_SSO',
 'DEC_BPL',
 'DEC_BPLp',
 'DEC_BPLM',
 'DEC_BPLF',
 'DEC_BPLMp',
 'DEC_BPLFp',
 'DEC_MI']
       #The attribute field or fields that will be used to define zones
                                                              # Fields could be more than those above. In this demo, we need those four fields
in_class_features = "DC_Census2010_.shp"#this is after-changed shp
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
        normalField.append(int(normal))
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
        countField.append(int(count))
        print "Thanks for typing, if there's no further number needed to be entered, please enter 'end'"
    except ValueError:
        print "Please only enter integers or 'end', let's try again, from the beginning"
        del countField[:]
for normalKey in normalField:#use 'value' list to record the corresponding field name of the recorded number
    normalValue.append(TotalList2[normalKey][1])# normalKey will show you 
for countKey in countField:
    countValue.append(TotalList2[countKey][1])
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
FidDic = {'GEO_ID' : 'mean'}
normalDic = {nv:'sum' for nv in normalValueAfter}
countDic = {cv:'mean' for cv in countValueAfter}
normalDic.update(countDic)
#normalDic.update(FidDic)
# Groupby the result by the sensus tract of year2010, sum the population, and average the income
Table10 = Table00.groupby(['GEO_ID_1'], as_index=False).agg(normalDic) # for example: table.groupby[field].agg({'field1' : 'sum', 'field2' : 'mean'})
#Table10.index.names = ['FID']    nv in normalValueAfter : 'sum', 'FID_' : 'mean', cv in countValue : 'mean'
Table10.to_csv(csv_output) # write the new table into csv
print "done"
####################################################################################################################################
#%%
## Part 4: join the table into shapefile fields
#arcpy.env.workspace = inputSpace
#inData = "DC_Census2010_.shp"
#inField = "GEO_ID"
#joinTable = dbf_output#csv_output
#joinField = "GEO_ID"
#fieldList = list(Table10)
# change the csv into dbf and then join back to the shapefile
#arcpy.CopyRows_management(csv_output, dbf_output)
#arcpy.JoinField_management(inData, inField, joinTable, joinField, fieldList)

#print("finished")
