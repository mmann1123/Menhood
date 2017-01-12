
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
import numpy as np

# arcpy error hanlding
arcpy.env.outputMFlag = "Enable"


# Here we create a function to covert a dbf to csv. We pass the out_table
# made from the tabulate intersection tool in Part 1 through it, this allows us
# to use the output in pandas in Part 3, which we need to do!

def dbf_to_csv(out_table):
    # string of .csv
    csv_fn = out_table[:-4] + ".csv"

    # error handling to make sure it worked
    try:
        os.remove(csv_fn)

    except OSError:
        pass

    # Create a csv file and write contents from dbf

    # generate empty .csv file from csv_fn, open and allow to write in it
    with open(csv_fn, 'wb') as csvfile:

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


####################################################################################################################################
#%%
#Part 1: perform the tabulate intersection that slices the year a census tracts by year b 

# Part 1 slices the year a census tracts by year b. This determines how census tracts
# have changed over time and how we will apply year a values to year b geometries.
# ArcPy's tabulate intersection tool does just this, taking the year b 'slicer' layer
# as the 'zone_features' parameter, and the year a 'sliced' layer as 'class_features'.

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

# retrieve directory where the shapefiles used in tabulate intersection exist
inputSpace = raw_input("Please paste directory to save shapefiles:")

# set working directory to directory user provides
arcpy.env.workspace = inputSpace

# zone_features, the year b shapefile
zone_features = raw_input("Provide full path to zone shapefile:")

# zone_fields, field in zone_features defining geo_id. this also exists in class field
zone_fields = ["GEO_ID"]

#The attribute field or fields used to define classe

# class_features, the year a shapefile
class_features = raw_input("Provide full path to class shapefile:")

class_dbf = class_features[:-4] + ".dbf"

# class_fields, field in class_fields defining geo_id plus attributes we want to apply to
# year b
class_fields = list(pd.read_csv(class_dbf[:-4]+".csv"))

# name of output file
outPutFile = os.path.join(inputSpace, "TabulateIntersectionResult.dbf")

# final tabulated csv file
final_csv = outPutFile[:-4] + "_fin" + ".csv"


# quick error handling to make sure the out_table exists
try:

    os.remove(out_table)

except OSError:

    pass



# run tabulate intersection
arcpy.TabulateIntersection_analysis (zone_features,
                               zone_fields, class_features, outPutFile, class_fields)

print "complete"
################################################################################################################################################
#%%
#Part 2: this function convert the tabulate intersection result into a csv


# Run the dbf_to_csv function, passing through out_table from Part 1 to make our csv
# for Part 2!
dbf_to_csv(out_table)

####################################################################################################################################
#%%  Part 3: Split out_table into a table to aggregate and to split 

# two dataframes are created here to handle different scenarios regarding how census
# tracts have been split from the two years of interest, referred as year a and b.

# the first scenario is where multiple tracts in year a were combined together in year b.
# in this scenario, we want the same values in the year a tracts
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
# if yes, then we consider it a split and take from out_csv all columns and row of same
# index as those taken to make the lists above and add it to the split_df variable

# if our if statement returns false, that there is only 1 tract in year b with same 
# id as multiple tracts in year a, then it is an aggregate and we add it to the split_df

# last depending on if we have a split or aggregate scenario, subset intrsct to be all
# rows with index 1 greater than the length of split or aggregate and then continue on 
# until all tracts in year a have been assigned to either df_agg or df_split, which 
# when the while loop in which we iterate this process, which checks to see if the length
# of rows in intrsct is greater than 0, breakss

intrsct = pd.read_csv(out_table)

# replace strings and #div/0 with na

intrsct = intrsct.replace("#DIV/0!", np.nan)
intrsct = intrsct.replace("(X)",np.nan)

# add area_list 'AREA' as 'Perc_GEO_ID_1_AREA to intrsct

intrsct = intrsct.sort("GEO_ID")

# create split_df and agg_df with only columns, no rows yet.
split_df = pd.DataFrame(columns=[intrsct.columns.values])
agg_df = pd.DataFrame(columns=[intrsct.columns.values])

# while loop to iterate separating to agg_df and split_df until all rows are agg or split
while len(intrsct) > 0:

	# get 1st value in geoid, and save to list called geoid1st to use with .isin()
	# to select all rows in geoid with value matching geoid1st
	# note, some hardcode ~ coersion is used to get just geoid. should be fixed
	geoid_1st = [intrsct.sort("GEO_ID").iloc[0]["GEO_ID"]][0]

    geoid_geoid1st_all = intrsct.loc[intrsct.GEO_ID == geoid_1st]["GEO_ID_1"].tolist()

    if len(geoid_geoid1st_all) > 1:

        # add to agg_df
        agg_df = agg_df.append(intrsct[:len(geoid_geoid1st_all)])

    # subset intrsct so it starts at one after row after geoid1st_all's last row

    intrsct = intrsct[len(geoid_geoid1st_all):]

    # see if geoid1_geoid1st_all is greater than 1, if so add to split_df
	if len(geoid_geoid1st_all) == 1:

		# add to agg_df
		split_df = split_df.append(intrsct[:len(geoid_geoid1st_all)])

		# subset intrsct so it starts at one after row after geoid1st_all's last row
		intrsct = intrsct[len(geoid_geoid1st_all):]

########################################################################################################################
#%% Part 4: Separate Normalized and Count Variables

# In this section we will separate the variables depending on if they represent normalized values or count values as
# both need to be handled differently when being applied to the year b census tract. Also split and aggregate scenarios
# necessitate specific handling.

# With aggregate scenarios we average normalized values and sum weighted count values
# With split scenarios we make normalized values the same from the year a tract to cut up year b tracts. When count,
# we apply the area weighted value of the larger year a to the sliced year b values.

# to make this happen we will apply a forloop over the agg_df and split_df where nested operations do the following.

    # create two lists for normalized and count variables
    # apply the correct 'mapping' (averaging, weighted sum)

# create list with agg and split dfs

agg_split_dict = {'agg_df':agg_df,'split_df':split_df}

for i in agg_split_dict:

    # create list of variables

    var_list = list(agg_df)

    # create list of variables that we'll use select as either normalized or count

    var_sel_list = []

    # add vars in var_list to var_sel_list to make them 'selectable'

    for field in var_list:

        var_sel_list.append([var_list.index(field), field])

    if i == 'agg_df':

        # if no variables index, pass it!

        if len(agg_split_dict[i]) > 0:

            # list holding selected count fields

            agg_normalField = []

            # list holding selected count fields

            agg_countField = []

            # two while loops, the first selecting the normal fields, the second selecting the count fields

            print "Now we are going to choose which fields are normalized data, which fields are count-based data:"

            raw_input("hit enter")

            print "start from normalized field, please type in the corresponding number of each field:"

            print var_sel_list

            while True:

                try:

                    # input records key of list element holding variable of interest

                    normal = raw_input("please enter the number here, only integer:  ")

                    # when end is entered, break the while look

                    if normal == "end":

                        print "finish recording"

                        # return normalField
                        break

                    # add variable name to agg_normalField

                    agg_normalField.append(var_sel_list[int(normal)][1])

                    print "Thanks for typing, if there's no further number needed to be entered, please enter 'end'"

                except ValueError:

                    print "Please only enter integers or 'end', let's try again, from the beginning"

                    del agg_normalField[:]

            print "\n Now is count data field, please type in the corresponding number of each field: \n"

            print var_sel_list

            # same while for counts

            while True:

                try:

                    count = raw_input("please enter the number here, only integer:  ")

                    if count == "end":
                        print "finish recording"

                        # return countField
                        break

                    agg_countField.append(var_sel_list[int(count)][1])

                    print "Thanks for typing, if there's no further number needed to be entered, please enter 'end'"

                except ValueError:

                    print "Please only enter integers or 'end', let's try again, from the beginning"

                    del countField[:]

            # agg normalFields_list holds dataframe of 'mapped' normal variables

            agg_normalFields_list = []

            # for each normal field do the following:
                # calculate mean for each "GEO_ID_1" group
                # append calculation to agg_normal_Field_list
                # append dataframe holding each calculation to agg_normalFields_list
                # inner join dataframe in agg_normalFields_list, saving as agg_normal_df

            if len(agg_normalField) > 0:

                for normalField in agg_normalField:


                    agg_normalField_list = []

                    for i in agg_df.GEO_ID.unique():

                        field_avg = pd.DataFrame(

                                        {
                                            "GEO_ID":i,
                                            normalField:agg_df[agg_df.GEO_ID == i][normalField].replace(0.00, np.nan).astype(float).mean()

                                        },
                                        index = [0]
                                    )

                        agg_normalField_list.append(field_avg)

                    agg_normalFields_list.append(pd.concat(agg_normalField_list).set_index("GEO_ID"))

                    if len(agg_normalField) == 1 :

                        agg_normal_df = agg_normalFields_list[0]

                    if agg_normalField.index(normalField) > 0:

                        agg_normal_df = pd.concat(agg_normalFields_list,axis=1)


                # agg normalFields_list holds dataframe of 'mapped' normal variables

                agg_countFields_list = []

                # for each normal field do the following:
                    # calculate mean for each "GEO_ID_1" group
                    # append calculation to agg_normal_Field_list
                    # append dataframe holding each calculation to agg_normalFields_list
                    # inner join dataframe in agg_normalFields_list, saving as agg_normal_df

            if len(agg_countField) > 0:

                for countField in agg_countField:

                    agg_countField_list = []

                    for i in agg_df.GEO_ID.unique():

                        field_weightsum = pd.DataFrame(

                            {

                             "GEO_ID":i,
                             countField:(agg_df[agg_df.GEO_ID == i][countField] *
                                         agg_df[agg_df.GEO_ID == i]["PERCENTAGE"]).sum()

                            }, index =  [0]
                        )

                        agg_countField_list.append(field_weightsum)

                    agg_countFields_list.append(pd.concat(agg_countField_list).set_index("GEO_ID"))

                    if len(agg_countField) == 1 :

                        agg_count_df = agg_countFields_list[0]

                    if agg_countField.index(countField) > 0:

                        agg_count_df = pd.concat(agg_countFields_list,axis=1)


            # finally merge the agg_normal and agg_count dataframes back to agg_df

            if len(agg_normalField) > 0  & len(agg_countField) > 0 :

                agg_df = pd.concat([agg_normal_df, agg_count_df],axis=1)

            if len(agg_normalField) > 0  & len(agg_countField) == 0 :


                agg_df = pd.concat([agg_normal_df], axis=1)

            else:

                agg_df = pd.concat([agg_count_df], axis=1)

    # below includes same steps as agg, except mapping calculations for agg and split, which are different

    elif i == 'split_df':

        if len(agg_split_dict[i]) > 1:

            # list holding selected count fields

            split_Fields = split_df.columns.tolist()

            split_Fields_list = []

            # for each normal field do the following:
                # calculate mean for each "GEO_ID_1" group
                # append calculation to agg_normal_Field_list
                # append dataframe holding each calculation to agg_normalFields_list
                # inner join dataframe in agg_normalFields_list, saving as agg_normal_df

            for Field in split_Field:

                split_Field_list = []

                for i in split_df.GEO_ID.unique():

                    field_value = pd.DataFrame(

                        {
                            "GEO_ID": i,
                            normalField: split_df[split_df.GEO_ID == i][normalField].replace(0.00, np.nan)

                        },
                        index=[0]
                    )

                    split_Field_list.append(field_value)

                split_Fields_list.append(pd.concat(split_Field_list).set_index("GEO_ID"))

                if len(split_Field) == 1:

                    split_df = split_Fields_list[0]

                if split_Field.index(Field) > 0:
                    split_df = pd.concat(split_Fields_list, axis=1)

            df_list = [split_df,agg_df]

            final_df = pd.concat(df_list,axis=1)

            final_df.index.name = "GEO_ID"

            final_df.to_csv(final_csv)

agg_df.index.name = "GEO_ID"

agg_df.to_csv(final_csv)


####################################################################################################################################
#%%
## Part 5: join the table with year b shapefile

arcpy.env.workspace = inputSpace
inData = "DC_Census2010_.shp"
inField = "GEO_ID"
joinTable = final_csv
joinField = "GEO_ID"
fieldList = var_list
# change the csv into dbf and then join back to the shapefile
arcpy.CopyRows_management(final_csv, dbf_output)
arcpy.JoinField_management(inData, inField, joinTable, joinField, fieldList)

