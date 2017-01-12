
"""
This scritp was created for joining multiple variables to one shp
@author: Shiyan, Qi
"""
import pandas as pd
#import arcpy
#arcpy.env.overwriteOutput = True
import os
import csv
from dbfpy import dbf
from Tkinter import *
import tkFileDialog         # Importing the Tkinter (tool box) library 
##
Joined_Pd = pd.DataFrame(); big_i = 0; Dyc_ReferList = [] #declare global variable
shppath = ""
folderpath = ""
Dyc_i_pd_List = [Dyc_ReferList, big_i, Joined_Pd, shppath, folderpath]
def get_imme_subF(a_dir):    #Given a path, return a list of all immediate sub-directory's list
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
def go_deep(level, RootPath):  #Given a root path, go deep a given level of directory, and return a list of all immediate sub-directory's list
    for i in range(level):
        RootPath = os.path.join(RootPath, get_imme_subF(RootPath)[0])
    return get_imme_subF(RootPath)
def split_check(String1, String2, check_location):#Check if a pair of string(filename)'s number X's element is equal or not, X is number, same as check_location parameter
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

def Format_the_path(path):
    path = str(path)
    path = path.replace("/", "\\")
    return path

def clickAbout():
    def moveDown():
        move_text = listbox.selection_get()
        curindex = int(listbox.curselection()[0])
        listbox.delete(curindex)
        listbox2.insert(END, move_text)
        Real_iterator = int(move_text.split(":")[0]) - 1##
        SelectedComb = ReferList[Real_iterator]##
        toplevel2 = Toplevel(toplevel)
        label1 = Label(toplevel2, text="type variable name if you want to rename it, leave it blank if you want to keep it unchanged", height=0, width=100)
        label1.pack()
        e = Entry(toplevel2)
        e.pack()
        def saveexit():
            OwnName = e.get()
            OwnName = OwnName[0:10]
            T2.insert(END, "You moved variable: "+move_text+"\nYou changed its name to: "+OwnName+"\n\n")
            SelectedComb.append(OwnName)##
            R_ReferList.append(SelectedComb)##
            toplevel2.destroy()
        saveexitBtn = Button(toplevel2, text="Save", command=saveexit)
        saveexitBtn.pack()

    def FinishExit():
        global Dyc_i_pd_List
        Dyc_ReferList = Dyc_i_pd_List[0]
        big_i = Dyc_i_pd_List[1]
        Joined_Pd = Dyc_i_pd_List[2]
        shppath = Dyc_i_pd_List[3]
        folderpath = Dyc_i_pd_List[4]
        Dyc_ReferList.extend(R_ReferList) # Append the dyc combination list record to the global list, by each dyc combination
        Join_Pd = pd.DataFrame()
        iii = 0
        for R_list in R_ReferList:
            Ann_RR = R_list[1]#the annotation csv file name
            Ann_ID = R_list[2]#the variable name
            OwnName_2 = R_list[4]
            Ann_Pd = pd.read_csv(str(Ann_RR))
            Ann_Pd = Ann_Pd.loc[1:, ["GEO.id", Ann_ID]]
            if OwnName_2 != '':
                Ann_Pd.rename(columns={"GEO.id": "GEO.id", Ann_ID: OwnName_2}, inplace=True)
            if iii == 0:
                Join_Pd = Ann_Pd
                iii += 1
            else:
                Join_Pd = Join_Pd.merge(Ann_Pd, how = 'outer', on="GEO.id")
                iii += 1
        if big_i == 0:
            Joined_Pd = Join_Pd
            big_i += 1
        else:
            Joined_Pd = Joined_Pd.merge(Join_Pd, how = 'outer', on="GEO.id")
            big_i += 1
        T.insert(END, "Finished selecting variables, you can click the button again to select more variables\n")
        Dyc_i_pd_List = [Dyc_ReferList, big_i, Joined_Pd, shppath, folderpath]
        toplevel.destroy()
        return Dyc_i_pd_List

    TotalList = []; ReferList = []; R_ReferList = []; iterator = 0
    del TotalList[:]
    del ReferList[:]
    del R_ReferList[:]
    T.insert(END, "In the popup dialog, select your desired Year-Data-Category combination data folder\n")
    RP = tkFileDialog.askdirectory()
    T.insert(END, "Grabing CSV from:\n" + RP +"\n")
    os.chdir(RP)
    Namelist = sorted(os.listdir(RP))#Get the variable name and description, get rid of all the variable start with "margin
    for Index, NamePart in enumerate(Namelist):# of error"
        if Index + 1 == len(Namelist):
            break
        else:
            Meta = NamePart
            Ann = Namelist[Index+1]
            if split_check(Meta, Ann, 4) == False:
                T.insert(END, "There is a mismatch between Meta and Ann csv, here is the Meta file name: "+"\n"+Meta)
                T.insert(END, "Skipping this pair of csv")
            else:
                MetaPd = pd.read_csv(Meta)
                GEOid_List = MetaPd["GEO.id"].tolist()[2:]
                id_List = MetaPd["Id"].tolist()[2:]
                GEOid_id_Dict = dict(zip(GEOid_List,id_List))
                for key, val in GEOid_id_Dict.items():# the key is the variable name, the val is the variable explaination
                    if "Margin of Error" in val:
                        del GEOid_id_Dict[key]
                TotalList.append([Ann, GEOid_id_Dict])# Annotation file contains the real data, each annotation file will have many variables
    T.insert(END, "finished grabing the csv\n")
    toplevel = Toplevel()
    toplevel.title("Move your desired variable into the BOTTOM listbox")
    upperLabel = Label(toplevel, text="All the available variables:", width=100, height=1, font=16)
    upperLabel.pack()
    listbox = Listbox(toplevel)
    listbox.config(width=200, height=15)
    listbox.pack()
    moveBtn = Button(toplevel, text="Move Down", command=moveDown)
    moveBtn.pack()
    lowerLabel = Label(toplevel, text="Variables you selected:", width=100, height=1, font=16)
    lowerLabel.pack()
    listbox2 = Listbox(toplevel)
    listbox2.config(width=200, height=15)
    listbox2.pack()
    scrollbar = Scrollbar(toplevel)
    scrollbar.pack(side=RIGHT, fill=Y)
    messLabel = Label(toplevel, text="Message Box", width=100, height=1, font=16)
    messLabel.pack()
    T2 = Text(toplevel, height=5, width=100, yscrollcommand=scrollbar.set)
    T2.pack()
    scrollbar.config(command=T2.yview)
    finishButton = Button(toplevel, text="Finish selecting & exit", command=FinishExit)
    finishButton.pack()
    for pair in TotalList:# Each pair represent a pair of csv
        Ann_R = pair[0]# Ann_R as Ann really used
        Identifier = Ann_R.split(".")[0].split("_")[3]#turn xxx_xxx_xxx_DP05_with_ann.csv into DP05, grab that as identifier
        G_I_Dict = pair[1]
        for key, val in G_I_Dict.items():
            iterator += 1
            listbox.insert(END, str(iterator) + ": " + Identifier + ">>>>>" + key + "------" + val + "\n")
            ReferList.append([iterator, Ann_R, key, val])

def showV():
    global Dyc_i_pd_List
    Dyc_ReferList = Dyc_i_pd_List[0]
    Joined_Pd = Dyc_i_pd_List[2]
    print "Take a look at the head of your selection:\n"
    print Joined_Pd.head()
    for R_list_2 in Dyc_ReferList:
        Change_name = R_list_2[4]
        T.insert(END, "\nThe original variable number in CSV:   " + str(R_list_2[0])+"\n")
        T.insert(END, "The associated CSV name:   " + R_list_2[1]+"\n")
        T.insert(END, "The orignial variable name:   " + R_list_2[2]+"\n")
        if Change_name == "" or Change_name == " ":
            T.insert(END, "The user-defined variable name:   None"+"\n")
        else:
            T.insert(END, "The user-defined variable name:   " + Change_name+"\n")
        T.insert(END, "The explanation of the variable:   " + R_list_2[3])
        T.insert(END, "\n")

def openshp():
    global Dyc_i_pd_List
    shppath = Dyc_i_pd_List[3]
    scriptpath = os.path.dirname(os.path.realpath(sys.argv[0]))
    Menhood_path = os.path.dirname(scriptpath)
    data_path = os.path.join(Menhood_path, "data")
    initial_path = os.path.join(data_path, "ShapeFiles")
    shppath = tkFileDialog.askopenfilename(filetypes=[('Shapefile','*.shp'), ('all files', '.*')], initialdir=initial_path)
    Dyc_i_pd_List[3] = shppath
    Button2.config(state=DISABLED)
    return Dyc_i_pd_List

def openfold():
    global Dyc_i_pd_List
    folderpath = Dyc_i_pd_List[4]
    scriptpath = os.path.dirname(os.path.realpath(sys.argv[0]))
    Menhood_path = os.path.dirname(scriptpath)
    data_path = os.path.join(Menhood_path, "data")
    initial_path = os.path.join(data_path, "output_Shapefiles")
    folderpath = tkFileDialog.askdirectory(initialdir=initial_path)
    Dyc_i_pd_List[4] = folderpath
    Button3.config(state=DISABLED)
    return Dyc_i_pd_List

def run():
    def running():
        T.insert(END, "\nInitiating the running process\n")
        Output_name = e_foldername.get()
        Shp_name = e_shpname.get()
        global Dyc_i_pd_List
        global move_text2
        move_text2 = str(move_text2)
        move_text2 = move_text2.strip("\n")
        Dyc_ReferList = Dyc_i_pd_List[0]
        Joined_Pd = Dyc_i_pd_List[2]
        shppath = Dyc_i_pd_List[3]
        folderpath = Dyc_i_pd_List[4]
        ylist = list(Joined_Pd)
        DC_Shp = shppath
        folderpath = folderpath
        Folder_Path=folderpath+"/"+Output_name
        os.mkdir(Folder_Path)
        T.insert(END, "Just made the output folder\n")
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
        T.insert(END, "Created a variable description file\n")
        arcpy.CopyFeatures_management(DC_Shp, Folder_Path+"\\"+Shp_name)#Copy a new shp to output folder from original one
        T.insert(END, "Copied the shp to the output folder\n")
        T.insert(END, "Merging your selection with the shp\n")
        Copied_Shp = Folder_Path+"\\"+Shp_name+".shp"
        Shp_csv = Folder_Path + "\\" + Shp_name + ".csv"
        Joined_shp_csv = Folder_Path + "\\Shp_Joined_variable.csv"
        dbf_to_csv(Folder_Path + "\\" + Shp_name + ".dbf")#Use self-defined function to change dbf to csv
        Shp_csv_pd = pd.read_csv(Shp_csv)#read csv as dataframe
        Shp_pd_lj = Shp_csv_pd.merge(Joined_Pd, how="left", left_on=move_text2, right_on="GEO.id")#Left join the csv-dataframe with variable df
        Shp_pd_lj = Shp_pd_lj.rename(columns = {move_text2:"GEO_ID_2"})#rename the joined df column so that it won't have same name in the future
        for n, i in enumerate(ylist):
            if i == "GEO.id":
                ylist[n]="GEO_ID_2"
        Shp_pd_lj_2 = Shp_pd_lj[ylist]#Drop uneeded columns, only leave Geoid, and variables
        Shp_pd_lj_2.to_csv(Joined_shp_csv, index=False)
        arcpy.TableToTable_conversion(Joined_shp_csv, Folder_Path, "Joined_variables.dbf")# Convert the joined-modified df to dbf
        arcpy.JoinField_management(Copied_Shp, move_text2, Folder_Path + "\\Joined_variables.dbf", "GEO_ID_2")#Join the dbf with new shp
        T.insert(END, "Finished!")
        top2.destroy()
    def selectGEOID():
        global move_text2
        move_text2 = listbox3.selection_get()
        GEOIDbutton.config(state=DISABLED)
        return move_text2
    move_text2 = ""
    top2 = Toplevel(root)
    frame1 = Frame(top2)
    frame1.pack()
    frame2 = Frame(top2)
    frame2.pack()
    frame3 = Frame(top2)
    frame3.pack()
    folderLabel = Label(frame1, text="Type in the output foldername you wished")
    folderLabel.pack(side=LEFT)
    e_foldername = Entry(frame1)
    e_foldername.pack(side=LEFT)
    shpnameLabel = Label(frame2, text="Type in the output shapefile name you wished, no .shp")
    shpnameLabel.pack(side=LEFT)
    e_shpname = Entry(frame2)
    e_shpname.pack(side=LEFT)
    listbox3 = Listbox(frame3)
    listbox3.pack()
    GEOIDbutton = Button(frame3, text="Select Join Field", command=selectGEOID)
    GEOIDbutton.config(state="normal")
    GEOIDbutton.pack()
    global Dyc_i_pd_List
    shppath = Dyc_i_pd_List[3]
    DC_Shp = str(shppath)
    DC_Shp = DC_Shp.replace("/", "\\\\")
    DC_Shp_dbf = DC_Shp[:-4] + ".dbf"
    DC_Shp_csv = DC_Shp[:-4] + ".csv"
    dbf_to_csv(DC_Shp_dbf)
    Shp_csv_pd = pd.read_csv(DC_Shp_csv)
    os.remove(DC_Shp_csv)
    col_list = Shp_csv_pd.columns.tolist()
    for col in col_list:
       listbox3.insert(END, col + "\n")
    runningButton = Button(top2, text="Run it!", command=running)
    runningButton.pack(side=BOTTOM)

def openoutput():
    global Dyc_i_pd_List
    folderpath = Dyc_i_pd_List[4]
    folderpath = folderpath
    os.startfile(folderpath)

def clean():
    global Dyc_i_pd_List
    Dyc_ReferList = Dyc_i_pd_List[0]
    big_i = Dyc_i_pd_List[1]
    Joined_Pd = Dyc_i_pd_List[2]
    shppath = Dyc_i_pd_List[3]
    folderpath = Dyc_i_pd_List[4]
    del Dyc_ReferList[:]
    big_i = 0
    empty_pd = pd.DataFrame()
    Joined_Pd = empty_pd
    empty_str = ""
    shppath = empty_str
    folderpath = empty_str
    Dyc_i_pd_List = [Dyc_ReferList, big_i, Joined_Pd, shppath, folderpath]
    T.delete('1.0', END)
    Button2.config(state="normal")
    Button3.config(state="normal")
    return Dyc_i_pd_List

def quitt():
    root.destroy()

def disclaim():
    def Isee():
        top3.destroy()
    top3 = Toplevel(root)
    disclaimer_label = Label(top3, text="Software author: Qi Yang, Shiyan Zhang\nThis software is used for non-commercial purpose only, mainly for academic research\nFor questions, contact email: yangkey87@gmail.com")
    disclaimer_label.pack()
    Iseebutton = Button(top3, text="I see", command=Isee)
    Iseebutton.pack()
##
root = Tk()
root.title("Qi-Shiyan's Shp Joiner")
mainLabel = Label(root, text="Main Dialog Box", font=14).grid(row=0)
T = Text(root, width=150)
T.grid(row=1)
Yscroll = Scrollbar(root, command=T.yview, orient=VERTICAL)
Yscroll.grid(row=1, sticky='ns'+E)
T.configure(yscrollcommand=Yscroll.set)
Yscroll.config(command=T.yview)
noteLabel = Label(root, text="Note:  proceed as the main dialog box prompted, cyan color button means it's multi-click-enabled", fg="orange").grid(row=2)
Button1 = Button(root, text="1. Select variable folder & variable", bg="cyan", command=clickAbout)
Button1.grid(row=3, sticky=W)
ShowSelectButton = Button(root, text="Show Selected Variables", bg="cyan", command=showV).grid(row=3, sticky=E)
Button2 = Button(root, text="2. Select the Shp", command=openshp)
Button2.grid(row=4, sticky=W)
Button3 = Button(root, text="3. Select the output folder location", command=openfold)
Button3.grid(row=4)
RunButton = Button(root, text="4. Run!!", command=run).grid(row=4, sticky=E)
OpenButton = Button(root, text="Open output folder", bg="cyan", command=openoutput).grid(row=5, sticky=W)
ClearButton = Button(root, text="Clear screen & Restart", bg="cyan", command=clean).grid(row=5)
QuitButton = Button(root, text="Quit", command=quitt).grid(row=5, sticky=E)
DisButton = Button(root, text="Disclaimer", bg="cyan", command=disclaim).grid(row=6, sticky=W+E)
root.mainloop()                 # Execute the main event handler