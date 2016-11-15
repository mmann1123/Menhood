
# coding: utf-8

# In[1]:

import pandas as pd
import arcpy
arcpy.env.overwriteOutput = True
import os
import time


# In[2]:

TotalList = []; ReferList = []; R_ReferList = []; iterator = 0; i = 0
def get_imme_subF(a_dir):    #Given a path, eturn a list of all immediate sub-directory's list
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
def go_deep(level, RootPath):  #Given a root path, go deep a given level of directory, and return a list of all immediate sub-directory's list
    for i in range(level):
        RootPath = os.path.join(RootPath, get_imme_subF(RootPath)[0])
    return get_imme_subF(RootPath)
def split_check(String1, String2, check_location):
    list1 = String1.split(".")
    list2 = String2.split(".")
    S1part = list1[0].split("_")[check_location-1]
    S2part = list2[0].split("_")[check_location-1]
    return S1part == S2part


# In[3]:

CSV_FilePath_SS = str(raw_input("Please provide the immediate parent file path to your ACS & DEC csv files:" + 
"\n\n" + "For example: G:\Share\GEOG6307\Grossman, this path has two folders: ACS and DEC"+"\n\n"
+ "This is the most important path required in this program, be very careful" + "\n\n>>>"))# CSV_FilePath_Single_Slash
print "Changing current working directory to the path where tables located"
os.chdir(CSV_FilePath_SS)
CSV_FilePath = os.getcwd()
RootPath = CSV_FilePath
VariableCategoryList = go_deep(2, CSV_FilePath)
# print back file path to user
print "\n" + "File Path:" + "\n" + CSV_FilePath


# In[4]:

print "Which data category interests you?" + "\n"
for i in range(len(VariableCategoryList)):
    print "Type %s for "%(str(i+1)) + VariableCategoryList[i] + "\n"
CategoryDecision = str(raw_input("enter here, only numbers>>>>>>>"))
Category = VariableCategoryList[int(CategoryDecision)-1]


# In[5]:

VariableCategory = VariableCategoryList[int(CategoryDecision)-1]
Dataset = str(raw_input(
    "Which data set interests you?" + "\n\n"
    "Type ACS for American Community Survey" + "\n"
    "Type DEC for Decennial Census" + "\n\n> "))
CSV_FilePath = os.path.join(CSV_FilePath, Dataset)


# In[6]:

print "Which %s year interests you?"%(Dataset)
YearList = get_imme_subF(CSV_FilePath)
for y in YearList:
    print "Type %s for 20%s"%(y, y)
YearDecision = raw_input("enter here, only numbers>>>>>>>")
CSV_FilePath = os.path.join(CSV_FilePath, YearDecision)
CSV_FilePath = os.path.join(CSV_FilePath, Category)# This is the path stored the requested csv
print "Grabing CSV from  " + CSV_FilePath
os.chdir(CSV_FilePath)


# In[7]:

Namelist = sorted(os.listdir(CSV_FilePath))
for Index, NamePart in enumerate(Namelist):
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


# In[8]:

print "finished grabing the csv" + "\n" + "Here is all the data avaible with explanation:"
for pair in TotalList:# Each pair represent a pair of csv
    Ann_R = pair[0]# Ann_R as Ann really used
    Identifier = Ann_R.split(".")[0].split("_")[3]
    G_I_Dict = pair[1]
    for key, val in G_I_Dict.items():
        iterator += 1
        print str(iterator) + ": " + Identifier + "_" + key + "------" + val + "\n"
        ReferList.append([iterator, Ann_R, key, val])
while True:
    ReferNum = raw_input("Please type in the number of interest>>")
    OwnName = raw_input("\n" + "Please type in your name for this variable, no more than 10 characters" + "\n"+
                       "If you want to keep the original name, type 0 >>>")
    if len(OwnName) > 10:
        print "Your name is more than 10 characters, this program automatically truncated the extra characters"
        OwnName = OwnName[0:10]
    SelectedComb = ReferList[int(ReferNum)-1]
    SelectedComb.append(OwnName)
    R_ReferList.append(SelectedComb)
    finished = raw_input("***************************************" + "\n\n" +
        "Would you Like to select more variables?\nType 1 for Yes\nType 2 for No\n> ")
    if finished == "1":
        continue      
    if finished == "2":
        break
#print R_ReferList


# In[9]:

Joined_Pd = pd.DataFrame()
i = 0
for R_list in R_ReferList:
    Ann_RR = R_list[1]
    Ann_ID = R_list[2]
    OwnName_2 = R_list[4]
    Ann_Pd = pd.read_csv(Ann_RR)
    Ann_Pd = Ann_Pd.loc[1:, ["GEO.id", Ann_ID]]
    if OwnName_2 != "0":
        Ann_Pd.columns = ["GEO.id", OwnName_2]
    if i == 0:
        Joined_Pd = Ann_Pd
        i += 1
    else:
        Joined_Pd = Joined_Pd.merge(Ann_Pd, on="GEO.id")
        i += 1
#Joined_Pd


# In[10]:

DC_Shp = RootPath + "\\ShapeFiles" + "\\DC_Census.shp"
Output_name = raw_input("Please type in the name of the folder where store the joined shp and description of variables")
hms = time.strftime("%H:%M:%S")
dmy = time.strftime("%d/%m/%Y")
hms_list = hms.split(":")
dmy_list = dmy.split("/")
Folder_Path=RootPath+"\\Output"+"\\"+Output_name+"_"+hms_list[0]+"H"+hms_list[1]+"M"+hms_list[2]+"S"+dmy_list[0]+"D"+dmy_list[1]+"M"+dmy_list[2]+"Y"
os.mkdir(Folder_Path)
D_txt = open(Folder_Path+"\\Variable_Description.txt", "w")
for R_list_2 in R_ReferList:
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


# In[11]:

Joined_Pd.to_csv(Folder_Path+"\\Joined_variables.csv")
CensusLyr = arcpy.MakeFeatureLayer_management(DC_Shp, Folder_Path+"\\censusLayer.lyr")
arcpy.TableToTable_conversion(Folder_Path+"\\Joined_variables.csv", Folder_Path, "Joined_variables.dbf")
CensusLyr = arcpy.JoinField_management (CensusLyr,"GEO_ID", Folder_Path + "\\Joined_variables.dbf", "GEO_id")
Shp_name = raw_input("Last request: please type in the desired shapefile name, don't include .shp, no character as:" + 
                    "\\ or / or : or * or ? or \" or < or > or |" + "\n>>>>>>>>>>>>>>>>")
arcpy.CopyFeatures_management(CensusLyr, Folder_Path + "\\" + Shp_name + ".shp")


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



