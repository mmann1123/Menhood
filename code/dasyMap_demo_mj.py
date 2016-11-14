
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

# retrieve directory where the shapefiles used in tabulate intersection exist
inputSpace = raw_input("Please paste the working directory which store the intermidate files and results:")

# set working directory to directory user provides
arcpy.env.workspace = inputSpace


outPutFile = "TabulateIntersectionResult.dbf"
arcpy.env.outputMFlag = "Enable"
####################################################################################################################################
#%%
#Part 1: perform the tabulate intersection that slices the year a census tracts by year b 

# Part 1 slices the year a census tracts by year b,. This determines how census tracts
# have changed over time and how we will apply year a values to year b geometries.
# ArcPy's tabulate intersection tool does just this, taking the year b 'slicer' layer
# in as the 'zone_features' parameter, and the year a 'sliced' layer as 'class_features'.

# this outputs a dbf where each row represents a polygon created when year a is sliced by
# year b. In Part 2 we'll manipulate this so that we handle all ways in which census
# tracts change from a to b

# in addition to the zone & class feature parameters, we also need to provide zone & class
# field parameters - fields from both zone and class shapefiles. First, both parameters
# have to include their matching census tract ids, the 'GEO_ID' fields. Then, class_fields
# parameter should also include the attributes of interest since our goal is to fit these
# year a fields to the year b census tracts in Part 3.

# lastly there is the out_table parameter, simply the file name and path to which we
# want to save the output

# zone_features, the year b shapefile
zone_features = "DC_Census2010_.shp"

# zone_fields, field in zone_features defining geo_id. this also exists in class field
zone_fields = ["GEO_ID"]#The attribute field or fields used to define classe

# class_features, the year a shapefile
class_features = "dec2000_5.shp"

# class_fields, field in class_fields defining geo_id plus attributes we want to apply to
# year b
class_fields = ["GEO_ID", 'dec_ma',
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

# where we save the file
out_table = os.path.join(inputSpace, outPutFile)


# quick error handling to make sure the out_table made in 147 exists
try:

    os.remove(out_table)

except OSError:

    pass

# run tabulate intersection
arcpy.TabulateIntersection_analysis (zone_features, 
                               zone_fields, class_features, out_table, class_fields)
                              
print "complete"
################################################################################################################################################
#%%
#Part 2: this function convert the tabulate intersection result into csv       

# here in part 2 we create a function to covert a dbf to csv and pass the out_table 
# made from the tabulate intersection tool in Part 1 through it, this allows us 
# to use the output in pandas in Part 3, which we need to do!
                   
def dbf_to_csv(out_table):

	# Make from .csv to be made from .dbf. at this point the .csv hasn't any contents
    csv_fn = out_table[:-4]+ ".csv" 
    
    # error handling to make sure it worked
    try:
        os.remove(csv_fn)
        
    except OSError:
        pass
    
    # Create a csv file and write contents from dbf
    
    # open the empty .csv file, with ability to write in it
    with open(csv_fn,'wb') as csvfile: 
    
    	# read in dbf created with tabulate intersection
        in_db = dbf.Dbf(out_table)
        
        # set the empty, open csv to variable we will write contents of dbf to
        out_csv = csv.writer(csvfile)
        
        # create empty list that will hold column names of dbf that we'll give to our csv
        names = []
        
        # Iterate over the column names from the dbf and add them to names list
        for field in in_db.header.fields: 
            names.append(field.name)
            
        # write the column names in names to the csv as row header names
        out_csv.writerow(names)
        
        # iterate over records in the dbf and write them to the csv
        for rec in in_db:
            out_csv.writerow(rec.fieldData)
        
        # close the dbf. We are done converting the dbf to a csv! 
        in_db.close()

# Run the dbf_to_csv function, passing through out_table from Part 1 to make our csv
# for Part 2!
dbf_to_csv(out_table)

####################################################################################################################################
#%%  Part 3: Split out_table into a table to aggregate and to split 

# two dataframes are created here to handle different scenarios regarding how census
# tracts have been split from the two years of interest, referred as year a and b.

# the first scenario is where multiple tracts in year a was combined together in year b
# in this scenario, for dasymetric mapping we want the same values in the year a tracts
# to exist in the year b tracts, so we 'aggregate them', hence being combined in agg_df

# the second scenario is when a year a census tract is split into multiple year b tracts.
# here we want to take the year a value to all those split them amongst year b, 
# hence split. 

# we start from the 1st row in the intrsct, the df we made by reading in out_csv created 
# in part 1 and search down for all consecutive rows where year a tract ids, here in 
# column 'GEO_ID', are the same. we save this to a list. We then take the length of that 
# list to count down from the same row we started to make it and count down the same 
# length, only this time grabbing a list of year b ids, here the column 'GEO_ID_1'.

# next we use an if statement to see if the length of GEO_ID_1 is greater than 1
# if it, then we consider it a split and take from out_csv all columns and row of same
# index as those taken to make the lists above and add it to the split_df variable

# if our if statement returns false, that there is only 1 tract in year b with same 
# id as multiple tracts in year a, then it is an aggregate and we add it to the split_df

# last depending on if we have a split or aggregate scenario, subset intrsct to be all
# rows with index 1 greater than the length of split or aggregate and then continue on 
# until all tracts in year a have been assigned to either df_agg or df_split, which 
# when the while loop in which we iterate this process, which checks to see if the length
# of rows in intrsct is greater than 0, breakss

intrsct = pd.read_csv(out_table)

# create split_df and agg_df with only columns, no rows yet.
split_df = pd.DataFrame(columns=[intrsct.columns.values])
agg_df = pd.DataFrame(columns=[intrsct.columns.values])

# while loop to iterate separating to agg_df and split_df until all rows are agg or split
while len(intrsct) > 0:


	# create geoid and geoid1 dataframes used later to compare
	geoid = intrsct[['GEO_ID']]
	geoid1 = intrsct[['GEO_ID_1']]

	# get 1st value in geoid, and save to list called geoid1st to use with .isin() 
	# to select all rows in geoid with value matching geoid1st
	# note, some hardcode ~ coersion is used to get just geoid. should be fixed
	geoid1st = [geoid.iloc[0].to_string()[10:len(geoid.iloc[0].to_string())]]

	# subset geoid to rows with geoid1st value
	geoid1st_all = geoid[geoid["GEO_ID"].isin(geoid1st)]

    if len(geoid1_geoid1st_all) > 1:

        # add to agg_df
        agg_df = agg_df.append(intrsct[:len(geoid1st_all)])

    # subset intrsct so it starts at one after row after geoid1st_all's last row

    intrsct = intrsct[len(geoid1st_all):]

    # see if geoid1_geoid1st_all is greater than 1, if so add to split_df
	if len(geoid1_geoid1st_all) = 1:
	
		# add to agg_df 	
		split_df = split_df.append(intrsct[:len(geoid1st_all)])
	
		# subset intrsct so it starts at one after row after geoid1st_all's last row
		intrsct = intrsct[len(geoid1st_all):]
	
	# see if geoid_geoid1st_all is equal to one, if so, then add to split_df


########################################################################################################################
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

########################################################################################################################
#%% Part 4: Separate Normalized and Count Variables

# In this section we will separate the variables depending on if they represent normalized values or count values as
# both need to be handled differently when being applied to the year b census tract. Also split and aggregate scenarios
# necessitate specific handling.

# With aggregate scenarios we average normalized values and sum count values
# With split scenarios we make normalized values the same from the year a tract to cut up year b tracts. When count,
# we apply the area weighted value of the larger year a to the sliced year b values.

# to make this happen we will apply a forloop over the agg_df and split_df where nested operations do the following.

# create two lists for normal and


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
## Part 5: join the table into shapefile fields
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
