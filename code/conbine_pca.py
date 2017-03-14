import pandas as pd
import os
import fnmatch

os.chdir(os.getcwd() + 'data/pca_results/DEC_00')

pca_files =  fnmatch.filter(os.listdir("."),'*result_v1.csv')
pca_dfs = []
for csv in pca_files:
    pca_df = pd.read_csv(os.getcwd() + '/' + csv)
    pca_colName = csv.split('PCA')[0][0:3]
    pca_df= pca_df.rename(columns = {'Component_1':pca_colName})
    pca_df.set_index(pca_df.columns[0])
    pca_dfs.append(pca_df)

pcas_df = pd.concat(pca_dfs, axis=1, join='inner')

pcas_df.to_csv('pcas.csv')
