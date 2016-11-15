
# coding: utf-8

# In[ ]:

import pandas as pd
import arcpy
arcpy.env.overwriteOutput = True
import os
import time
import csv
from dbfpy import dbf
import Tkinter as tk
import tkFileDialog


# In[ ]:

root = tk.Tk()
root.withdraw()
Joined_Pd = pd.DataFrame(); big_i = 0; RootPath = ""; Dyc_ReferList = [] #declare global variable
del Dyc_ReferList[:]
def get_imme_subF(a_dir):    #Given a path, return a list of all immediate sub-directory's list
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
def go_deep(level, RootPath):  #Given a root path, go deep a given level of directory, and return a list of all immediate sub-directory's list
    for i in range(level):
        RootPath = os.path.join(RootPath, get_imme_subF(RootPath)[0])
    return get_imme_subF(RootPath)
def split_check(String1, String2, check_location):#Check if a pair of string(filename)'s number X's element is equal or not
    list1 = String1.split(".")
    list2 = String2.split(".")
    S1part = list1[0].split("_")[check_location-1]
    S2part = list2[0].split("_")[check_location-1]
    return S1part == S2part
def dbf_to_csv(out_table):#Input a dbf, output a csv
    csv_fn = out_table[:-4]+ ".csv" #Set the table as .csv format
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


# In[ ]:

def Select_dyc():
    global Joined_Pd
    global big_i
    global RootPath
    global Dyc_ReferList
    while True:
        TotalList = []; ReferList = []; R_ReferList = []; iterator = 0; iii = 0
        del TotalList[:]
        del ReferList[:]
        del R_ReferList[:]
        Join_Pd = pd.DataFrame()
        print "Please choose the immediate parent directory to your ACS & DEC csv files:\n\n"
        print "For example: G:\Share\GEOG6307\Grossman, this path has two folders: ACS and DEC\n\n"
        print "This is the most important path required in this program, be very careful"
        nothing1 = raw_input("Type enter__")
        RP = tkFileDialog.askdirectory()
        CSV_FilePath_SS = str(RP)
        CSV_FilePath_SS = CSV_FilePath_SS.replace("/", "\\\\")
        print "Changing current working directory to the path where tables located"
        os.chdir(CSV_FilePath_SS)
        CSV_FilePath = os.getcwd()
        RootPath = CSV_FilePath
        VariableCategoryList = go_deep(2, CSV_FilePath)
        DatasetList = get_imme_subF(RootPath)
        # print back file path to user
        print "\n" + "File Path:" + "\n" + CSV_FilePath

        print "Which data category interests you?" + "\n"#Get category, by reference number
        for i in range(len(VariableCategoryList)):
            print "Type %s for "%(str(i+1)) + VariableCategoryList[i] + "\n"
        while True:
            try:
                CategoryDecision = str(raw_input("enter here, only numbers>>>>>>>"))
                Category = VariableCategoryList[int(CategoryDecision)-1]
                break
            except ValueError:
                print "That was not a valid number. Try again, please type in a number this time"

        print "Here is all the dataset available:"#Get dataset name by user typed, will restart to record if the dataset name is not right
        for i in range(len(DatasetList)):
            iplus = i + 1
            print "Dataset " + str(iplus) + ":  " + DatasetList[i]
        while True:
            Dataset = str(raw_input(
                "\nWhich data set interests you?" + "\n\n"
                "Type ACS for American Community Survey" + "\n"
                "Type DEC for Decennial Census" + "\n\n> "))
            TrF = Dataset in DatasetList
            if TrF == False:
                print "The dataset you entered is not a valid one, please enter again"
            else:
                break
        CSV_FilePath = os.path.join(CSV_FilePath, Dataset)

        print "Which %s year interests you?"%(Dataset)#Get year by user typed, if the year is not correct if will restart to record year
        YearList = get_imme_subF(CSV_FilePath)
        for y in YearList:
            print "Type %s for 20%s"%(y, y)
        while True:
            YearDecision = raw_input("enter here, only numbers>>>>>>>")
            TrF2 = YearDecision in YearList
            if TrF2 == False:
                print "The year you entered is not a valid one, please enter again, only two digit number"
            else:
                break
        CSV_FilePath = os.path.join(CSV_FilePath, YearDecision)
        CSV_FilePath = os.path.join(CSV_FilePath, Category)# This is the path stored the requested csv
        print "Grabing CSV from  " + CSV_FilePath
        os.chdir(CSV_FilePath)

        Namelist = sorted(os.listdir(CSV_FilePath))#Get the variable name and description, get rid of all the variable start with "margin
        for Index, NamePart in enumerate(Namelist):# of error"
            if Index + 1 == len(Namelist):
                    break
            else:
                Meta = NamePart
                Ann = Namelist[(Index + 1)]
                if split_check(Meta, Ann, 4) == False:
                    print "There is a mismatch between Meta and Ann csv, here is the Meta file name: "+"\n"+Meta
                    print "Skipping this pair of csv"
                    continue
                else:
                    MetaPd = pd.read_csv(Meta)
                    AnnPd = pd.read_csv(Ann)
                    GEOid_List = MetaPd["GEO.id"].tolist()[2:]
                    id_List = MetaPd["Id"].tolist()[2:]
                    GEOid_id_Dict = dict(zip(GEOid_List,id_List))
                    for key, val in GEOid_id_Dict.items():
                        if "Margin of Error" in val:
                            del GEOid_id_Dict[key]
                    TotalList.append([Ann, GEOid_id_Dict])

        print "finished grabing the csv" + "\n\nHere is all the data avaible with explanation:\n"
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++VARIABLES+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        for pair in TotalList:# Each pair represent a pair of csv
            Ann_R = pair[0]# Ann_R as Ann really used
            Identifier = Ann_R.split(".")[0].split("_")[3]
            G_I_Dict = pair[1]
            for key, val in G_I_Dict.items():
                iterator += 1
                print str(iterator) + ": " + Identifier + "_" + key + "------" + val + "\n"
                ReferList.append([iterator, Ann_R, key, val])
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++VARIABLES+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        while True:
            print "Choose a variable by the index number, for example:\n\n"
            print "7: DP03_HC01_VC127------Estimate; HEALTH INSURANCE COVERAGE - Civilian noninstitutionalized population\n"
            print "If you want to choose this variable, simply type in 7."
            print "Now please type in the number based on all the variable provided above."
            while True:
                try:
                    ReferNum = raw_input("Enter here>>>>>>>>>>>")#Get the variable by user typed number
                    SelectedComb = ReferList[int(ReferNum)-1]
                    break
                except ValueError:
                    print "That was not a valid number. Try again, please type in a number this time"
            OwnName = raw_input("\n" + "Please type in your name for this variable, no more than 10 characters" + "\n"+
                               "If you want to keep the original name, type 0 >>>")
            if len(OwnName) > 10:
                print "Your name is more than 10 characters, this program automatically truncated the extra characters"
                OwnName = OwnName[0:10]
            SelectedComb.append(OwnName)
            R_ReferList.append(SelectedComb)
            finished = raw_input("***************************************" + "\n\n" +
                "Would you Like to select more variables in this specific dataset-year-categories combination?\nType 1 for Yes\nType 2 for No\n> ")
            if finished == "1":
                continue      
            if finished == "2":
                break
        Dyc_ReferList.extend(R_ReferList) # Append the dyc combination list record to the global list, by each dyc combination
        for R_list in R_ReferList:
            Ann_RR = R_list[1]
            Ann_ID = R_list[2]
            OwnName_2 = R_list[4]
            Ann_Pd = pd.read_csv(Ann_RR)
            Ann_Pd = Ann_Pd.loc[1:, ["GEO.id", Ann_ID]]
            if OwnName_2 != "0":
                Ann_Pd.columns = ["GEO.id", OwnName_2]
            Ann_Pd.head()#
            if iii == 0:
                Join_Pd = Ann_Pd
                iii += 1
            else:
                Join_Pd = Join_Pd.merge(Ann_Pd, how = 'outer', on="GEO.id")
                iii += 1
        More_dyc = raw_input("Do you want to select more variable from different dataset-year-categories combination?\n\n"+
                            "Type 1 as you want to select more\nType anything else as you don't want to select more\n\n"+
                            "Enter here>>>>>>>>>")
        if More_dyc == "1":
            if big_i == 0:
                Joined_Pd = Join_Pd
                big_i += 1
                continue
            else:
                Joined_Pd = Joined_Pd.merge(Join_Pd, how = 'outer', on="GEO.id")
                big_i += 1
                continue     
        else:
            if big_i == 0:
                Joined_Pd = Join_Pd
                print "you choose not to select more variable"
                print "Finished slecting variable stage, now entering ouptput setting stage.\n"
                break
            else:
                Joined_Pd = Joined_Pd.merge(Join_Pd, how = 'outer', on="GEO.id")
                print "you choose not to select more variable"
                print "Finished slecting variable stage, now entering ouptput setting stage.\n"
                break
    print "Take a look at your final selection"


# In[ ]:

Select_dyc()
Joined_Pd.head()


# In[ ]:

print "\nOK, now let'select the original shapefile for DC metro area"
nothing2 = raw_input("type enter__")
file_path = tkFileDialog.askopenfilename()
DC_Shp = str(file_path)
DC_Shp = DC_Shp.replace("/", "\\\\")
print "This is your shapefile:\n" + DC_Shp
DC_Shp_dbf = DC_Shp[:-4] + ".dbf"
Output_name = raw_input("Please type in the name of the folder where store the joined shp and description of variables")#Get folder name
hms = time.strftime("%H:%M:%S")
dmy = time.strftime("%d/%m/%Y")#Get the current time and append it to folder name
hms_list = hms.split(":")
dmy_list = dmy.split("/")
Folder_Path=RootPath+"\\Other(Dont Type This)\\Output"+"\\"+Output_name+"_"+hms_list[0]+"H"+hms_list[1]+"M"+hms_list[2]+"S"+dmy_list[0]+"D"+dmy_list[1]+"M"+dmy_list[2]+"Y"
os.mkdir(Folder_Path)
D_txt = open(Folder_Path+"\\Variable_Description.txt", "w")#Creat a variable description txt in the output folder
for R_list_2 in Dyc_ReferList:
    Change_name = R_list_2[4]
    D_txt.write("The original variable number in CSV:   " + str(R_list_2[0])+"\n")
    D_txt.write("The associated CSV name:   " + R_list_2[1]+"\n")
    D_txt.write("The orignial variable name:   " + R_list_2[2]+"\n")
    if Change_name == "0":
        D_txt.write("The user-defined variable name:   None"+"\n")
    else:
        D_txt.write("The user-defined variable name:   " + Change_name+"\n")
    D_txt.write("The explanation of the variable:   " + R_list_2[3])
    D_txt.write("\n\n")
D_txt.close()


# In[ ]:

Shp_name = raw_input("Last request: please type in the desired shapefile name, don't include .shp, no character as:" + 
                    "\\ or / or : or * or ? or \" or < or > or |" + "\n>>>>>>>>>>>>>>>>")
arcpy.CopyFeatures_management(DC_Shp, Folder_Path+"\\"+Shp_name)#Copy a new shp to output folder from original one
Copied_Shp = Folder_Path+"\\"+Shp_name+".shp"
arcpy.TableToTable_conversion(DC_Shp_dbf, Folder_Path, "Shp_original.csv")#Grab the ori shp-dbf and covnert to csv(actually still dbf)
Shp_csv = Folder_Path + "\\Shp_original.csv"
Joined_shp_csv = Folder_Path + "\\Shp_Joined_variable.csv"
#.dbf_to_csv(Folder_Path+"\\Shp_original.dbf")#Use self-defined function to change dbf to csv
Shp_csv_pd = pd.read_csv(Shp_csv)#read csv as dataframe
Shp_pd_lj = Shp_csv_pd.merge(Joined_Pd, how="left", left_on="GEO_ID", right_on="GEO.id")#Left join the csv-dataframe with variable df
Shp_pd_lj = Shp_pd_lj.rename(columns = {"GEO_ID":"GEO_ID_2"})#rename the joined df column so that it won't have same name in the future
cols = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
Shp_pd_lj.drop(Shp_pd_lj.columns[cols],axis=1,inplace=True)#Drop uneeded columns, only leave Geoid, and variables
Shp_pd_lj.to_csv(Joined_shp_csv, index=False)
arcpy.TableToTable_conversion(Joined_shp_csv, Folder_Path, "Joined_variables.dbf")# Convert the joined-modified df to dbf
arcpy.JoinField_management(Copied_Shp,"GEO_ID", Folder_Path + "\\Joined_variables.dbf", "GEO_ID")#Join the dbf with new shp
print "Finished"


# In[ ]:

#arcpy.TableToTable_conversion(Folder_Path+"\\Joined_variables.csv", Folder_Path, "Joined_variables.dbf")
#CensusLyr = arcpy.JoinField_management(CensusLyr,"GEO_ID", Folder_Path + "\\Joined_variables.dbf", "GEO_id")
#DataYearCate = Dataset + YearDecision + Category
#del Shp_pd_lj["GEO.id"]
#CensusLyr = arcpy.MakeFeatureLayer_management(DC_Shp, Folder_Path+"\\censusLayer.lyr")
#arcpy.CopyFeatures_management(CensusLyr, Folder_Path + "\\" + Shp_name + ".shp")
#CensusLyr = arcpy.JoinField_management(CensusLyr,"GEO_ID", Folder_Path + "\\Joined_variables.dbf", "GEO_id")
#del Shp_pd_lj["GEO.id"]
#DC_Shp = RootPath + "\\Other(Dont Type This)\\ShapeFiles" + "\\DC_Census.shp"#This is the madatory way to grab original shp
#CSV_FilePath_SS = str(raw_input("Please choose the immediate parent directory to your ACS & DEC csv files:" + 
        #"\n\n" + "For example: G:\Share\GEOG6307\Grossman, this path has two folders: ACS and DEC"+"\n\n"
        #+ "This is the most important path required in this program, be very careful" + "\n\n>>>"))# GGG


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



