import arcpy
import os

aprx = arcpy.mp.ArcGISProject("CURRENT")

nr_planu = arcpy.GetParameterAsText(0)
fold_doc = arcpy.GetParameterAsText(1)

folder = aprx.homeFolder
arcpy.env.workspace = r"{}\brg_mpzp.gdb".format(folder)
arcpy.env.overwriteOutput = True
workspace = arcpy.env.workspace
mpzpMap = aprx.listMaps(f"{nr_planu}_MPZP")[0]

if "PRZEZ_MIX" in [layer.name for layer in mpzpMap.listLayers()]:
    with arcpy.EnvManager(outputCoordinateSystem='PROJCS["ETRS_1989_Poland_CS2000_Zone_6",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",6500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",18.0],PARAMETER["Scale_Factor",0.999923],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'):
        arcpy.conversion.FeatureClassToShapefile(r"POWIERZCHNIE\GRANICA\GRANICA;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_ULICE;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_INFR;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_KOM;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_MIX", fold_doc)
else:
    with arcpy.EnvManager(outputCoordinateSystem='PROJCS["ETRS_1989_Poland_CS2000_Zone_6",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",6500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",18.0],PARAMETER["Scale_Factor",0.999923],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'):
        arcpy.conversion.FeatureClassToShapefile(r"POWIERZCHNIE\GRANICA\GRANICA;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_ULICE;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_INFR;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_KOM", fold_doc)

arcpy.AddMessage(fold_doc)                                      
arcpy.AddMessage("Brawo! Architektura będzie szczęśliwa")

aprx.save()
