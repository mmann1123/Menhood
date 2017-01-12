
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
import math
from matplotlib import pyplot as plt


# In[ ]:

#Get directory of the table
print "Let's start by locating the orignial table data, the data format should be csv"
print "\nPlease provide the directory of your data"
direc = raw_input(">>>>>>")
print "\nPlease provide the full name of your data"
name = raw_input(">>>>>>")
datapath = direc + "/" + name


# In[ ]:

#Read and show the table
Origin = pd.read_csv(datapath)
Origin.head()


# In[ ]:

#Preprocess the table, deal with NA problem
print "I will delete those empty rows. Do you want to replace the empty rows with 0? "
print "\nEnter yes to replace rows with 0, enter other words to delete rows"
rowDecision = raw_input(">>>>>>")
if rowDecision == "yes":
    Origin_NA = Origin.fillna(0)
else:
    Origin_NA = Origin.dropna(how="any", inplace=False)
#Get the  separately as future index to join back
print "Getting the first column as the index column"
OID = Origin_NA.iloc[:,[0]]
OID_NA = OID.dropna(how='any', inplace=False)
OID_NA_rein = OID_NA.reset_index()
OID_NA_rein.drop('index', axis=1, inplace=True)


# In[ ]:

#Get user-defined columns as PCA input
headerList = Origin_NA.columns.values.tolist()
headerListS = [str(x) for x in headerList]
headerDic = {}
headerDic.clear()
i = 1
for names in headerListS:
    headerDic.update({i:names})
    i = i + 1
nameList = []
del nameList[:]
print "Now let's decide which columns will be used in PCA, in other words," 
print "which columns of data do you want to combined together and extract the essential information as well as reduce the dimensionalities\n"
print headerDic
print "\nplease enter all the desire index number corresponding to the column names"
print "Enter one number at a time, if you entered all the columns please enter finish"
while True:
    try:
        number = raw_input("please enter the number here:>>>")
        if number == "finish":
            print "\nfinish recording"
            break
        Inumber = int(number)
        namee = headerDic[Inumber]
        nameList.append(namee)
        print "Thanks for typing, if there's no further number needed to be entered, please enter 'finish'\n"
    except ValueError:
        print "Please only enter integers or 'finish', let's try again, from the beginning"
        del normalField[:]
print "OK, this is the columns you selected:" 
print nameList
print "If you selected wrong columns, please run this script from the beginning"
#Standardize the data
PCAinput = Origin_NA[nameList]
print "Standarizng the data"
from sklearn.preprocessing import StandardScaler
X_std = StandardScaler().fit_transform(PCAinput)


# In[ ]:

#Show the covariance matrix, eigenvectors, eigenvalues
print "showing the covariance matrix, eigenvectors, eigenvalues"
print('\nNumPy covariance matrix: \n%s' %np.cov(X_std.T))
cov_mat = np.cov(X_std.T)
eig_vals, eig_vecs = np.linalg.eig(cov_mat)
print('\nEigenvectors \n%s' %eig_vecs)
print('\nEigenvalues \n%s' %eig_vals)


# In[ ]:

#Showing the precent of variance explained by each components by graph
#print "Showing the precent of variance explained by each components by graph"
#tot = sum(eig_vals)
#var_exp = [(i / tot)*100 for i in sorted(eig_vals, reverse=True)]
#cum_var_exp = np.cumsum(var_exp)
#get_ipython().magic(u'matplotlib inline')
#with plt.style.context('gtk3'):
#    plt.figure(figsize=(6, 4))

#    plt.bar(range(len(nameList)), var_exp, alpha=0.5, align='center',
#            label='individual explained variance')
#    plt.step(range(len(nameList)), cum_var_exp, where='mid',
#             label='cumulative explained variance')
#    plt.ylabel('Explained variance ratio')
#    plt.xlabel('Principal components')
#    plt.legend(loc='best')
#    plt.tight_layout()


# In[ ]:

print "After seeing this graph, you should know how many components you want to keep"
print "Please enter the number of components you want to keep, only enter the integer"
Ncom = raw_input(">>>>>>")
IntegerNcom = int(Ncom)
print "Now performing the PCA"
from sklearn.decomposition import PCA as sklearnPCA
sklearn_pca = sklearnPCA(n_components=IntegerNcom)
Y_sklearn = sklearn_pca.fit_transform(X_std)
listCom = range(IntegerNcom)
ComName = ["Component_" + str(x+1) for x in listCom]
PCAresult = pd.DataFrame(Y_sklearn, columns = ComName)
frames = [OID_NA_rein, PCAresult]
PCAresult2 = pd.concat(frames, axis=1)
PCAresult2.head()


# In[ ]:

print "Job is done, now saving the PCA result to the directory where the original data located"
PCAresult2.to_csv(direc+"/" + name[0:-4] + "_PCAresult.csv", index=False)
print "Saved it successfully"


# In[ ]:




# In[ ]:



