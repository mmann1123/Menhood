# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 00:54:16 2015

@author: Shiyan
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 05 19:36:26 2015

@author: Shiyan
"""

import arcpy
from arcpy import env
import arcpy.sa

arcpy.env.overwriteOutput = True
# Set environment settings
env.workspace = raw_input("Please input the workspace, where the point file located: ")
rasterLocation = raw_input("Please input the location of cost raster, should be inside a GDB, so include the gdb as the path: ")
# Because the origional file may be not in the working space you use,
# so we import the origional data into the working space using list feature class and for loop
featureclasses = arcpy.ListFeatureClasses()
for fc in featureclasses:
    arcpy.FeatureClassToGeodatabase_conversion(fc, rasterLocation)
# Set the workspace as the final working space
env.workspace = rasterLocation
# Set the coordinates extent
arcpy.env.extent = "s_rasterStreets"
# Set Snap Raster environment
arcpy.env.snapRaster = "s_rasterStreets"

# Set local variables
inCostRaster = "s_rasterStreets"
maxDistance = ''   
arcpy.CheckOutExtension("Spatial")
# using for loop to execute cost distance and save the out put
fcs = arcpy.ListFeatureClasses()
for fc in fcs:
    print fc
    outCostDistance = arcpy.sa.CostDistance(fc, inCostRaster, maxDistance)
    outCostDistance.save(env.workspace + "\cost_"+fc[:-4])

print "completed"