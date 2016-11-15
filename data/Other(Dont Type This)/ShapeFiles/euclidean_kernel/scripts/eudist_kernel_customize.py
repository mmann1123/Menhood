# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 19:02:34 2015

@author: Shiyan
"""

# Name: EucDistance_kernalDensity.py
# Description: Calculates euclidean distance and kernel density for feature classes in a folder
# Can automaticly establish GDBs and process a batch of feature classes

# Import system modules
import arcpy
from arcpy import env
import arcgisscripting
import os
gp = arcgisscripting.create(9.3)
arcpy.env.overwriteOutput = True

# Create the path and geodatabases which store the input data and the processed data
# Because euclidean distance and kernal density only can be executed in a geodatabase,
# so we need to create an inputDatabase to import the feature classes for executing eudist and kernel,
# in order to distinguash the outputs and inputs, we create another ouputGDB to store the outputs.
outFolderPath = raw_input("Please input the path of input data: ")
featureInputGDB = raw_input("Please name a database for input features with .gdb: ") 
outputGDB = raw_input("Please name the database for outputs with .gdb: ")
# Execute CreateFileGDB
arcpy.CreateFileGDB_management(outFolderPath, featureInputGDB)
arcpy.CreateFileGDB_management(outFolderPath, outputGDB)

print 'completed creating database'

# Set environment setting and use ListFeatureClasses to generate a list of shapefiles in the
# workspace.
env.workspace = outFolderPath
fcList = arcpy.ListFeatureClasses() 
# Execute FeatureClassToGeodatabase for each input shapefile
for shapefile in fcList:
    # Determine the new output feature class path and name
    outFeatureClass = os.path.join(outFolderPath,featureInputGDB)
    arcpy.FeatureClassToGeodatabase_conversion(shapefile, outFeatureClass)

#arcpy.FeatureClassToGeodatabase_conversion(fcList, featureInputGDB)
print "completed feature to database"
# This is the part of execute eudistance and kernalDensity
# Set environment settings of eudistance and kernelDensity
gp.workspace = os.path.join(outFolderPath, featureInputGDB) 
# Use ListFeatureClasses to generate a list of shapefiles in the featureInputGDB workspace.
    # Set the parameter of those tools 
maxDistance = ''
cellSizeE = '' 
populationField = "NONE"
cellSizeK = ''
searchRadius = ''
# Check out the ArcGIS Spatial Analyst extension license
gp.CheckOutExtension("Spatial")

fcs = gp.ListFeatureClasses()
# Execute eudistance and kernelDensity for each input shapefile
for shapefile in fcs:
    # Determine the new output feature class path and name
    outDistanceRaster = os.path.join(outFolderPath, outputGDB, 'eu_' + shapefile.strip('.shp'))
    outKernelDensityRaster = os.path.join(outFolderPath, outputGDB, 'krnl_' + shapefile.strip('.shp'))
    # Execute eudistance and kernelDensity
    gp.EucDistance_sa(shapefile, outDistanceRaster, maxDistance, cellSizeE)
    gp.KernelDensity_sa(shapefile, populationField, outKernelDensityRaster, cellSizeK, searchRadius)
# To remind the procedure running successful
print 'complete'