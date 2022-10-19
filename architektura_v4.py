import arcpy
import os

aprx = arcpy.mp.ArcGISProject("CURRENT")

nr_planu = arcpy.GetParameterAsText(0)
fold_doc = arcpy.GetParameterAsText(1)

aprxFile = aprx.filePath
folder = aprx.homeFolder
arcpy.env.workspace = r"{}\brg_mpzp.gdb".format(folder)
arcpy.env.overwriteOutput = True
workspace = arcpy.env.workspace
mpzpMap = aprx.listMaps(f"{nr_planu}_MPZP")[0]

if arcpy.Exists("PRZEZ_MIX"):
#if "PRZEZ_MIX" in [layer.name for layer in mpzpMap.listLayers()]:
    with arcpy.EnvManager(outputCoordinateSystem='PROJCS["ETRS_1989_Poland_CS2000_Zone_6",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",6500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",18.0],PARAMETER["Scale_Factor",0.999923],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]', transferDomains="TRANSFER_DOMAINS"):
        arcpy.conversion.FeatureClassToShapefile(r"POWIERZCHNIE\GRANICA;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_ULICE;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_INFR;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_KOM;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_MIX", fold_doc)
else:
    with arcpy.EnvManager(outputCoordinateSystem='PROJCS["ETRS_1989_Poland_CS2000_Zone_6",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",6500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",18.0],PARAMETER["Scale_Factor",0.999923],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]', transferDomains="TRANSFER_DOMAINS"):
        arcpy.conversion.FeatureClassToShapefile(r"POWIERZCHNIE\GRANICA;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_ULICE;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_INFR;POWIERZCHNIE\PRZEZNACZENIE\PRZEZ_KOM", fold_doc)

fcp = r"{}\PRZEZ.shp".format(fold_doc)

arcpy.management.DeleteField(fcp, "ozn_przezn", "DELETE_FIELDS")
arcpy.management.AddField(fcp, "ozn_przezn", "TEXT", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')

with arcpy.da.UpdateCursor(fcp, ["f1", "f2", "f3", "ozn_przezn", "d_f1", "d_f2", "d_f3", "d_ozn_prze"]) as cursor:
    for row in cursor:
        row[0] = row[4]
        row[1] = row[5]
        row[2] = row[6]
        row[3] = row[7]
        cursor.updateRow(row)
        
arcpy.management.DeleteField(fcp, "d_f1;d_f2;d_f3;d_ozn_prze", "DELETE_FIELDS")

fcp = r"{}\PRZEZ.shp".format(fold_doc)
arcpy.management.AddField(fcp, "text", "TEXT", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')

with arcpy.da.UpdateCursor(fcp, ["ozn_przezn", "text", "nr_terenu"])  as cursor:
    for row in cursor:
        row[1] = row[2]+"-"+row[0]
        cursor.updateRow(row)

fcpi = r"{}\PRZEZ_INFR.shp".format(fold_doc)

arcpy.management.DeleteField(fcpi, "ozn_przezn", "DELETE_FIELDS")
arcpy.management.AddField(fcpi, "ozn_przezn", "TEXT", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')

with arcpy.da.UpdateCursor(fcpi, ["ozn_przezn", "d_ozn_prze"]) as cursor:
    for row in cursor:
        row[0] = row[1]
        cursor.updateRow(row)
        
arcpy.management.DeleteField(fcpi, "d_ozn_prze", "DELETE_FIELDS")

fcpi = r"{}\PRZEZ_INFR.shp".format(fold_doc)
arcpy.management.AddField(fcpi, "text", "TEXT", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')

with arcpy.da.UpdateCursor(fcpi, ["ozn_przezn", "text", "nr_terenu"])  as cursor:
    for row in cursor:
        row[1] = row[2]+"-"+row[0]
        cursor.updateRow(row)

fcpk = r"{}\PRZEZ_KOM.shp".format(fold_doc)

arcpy.management.DeleteField(fcpk, "ozn_przezn", "DELETE_FIELDS")
arcpy.management.AddField(fcpk, "ozn_przezn", "TEXT", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')

with arcpy.da.UpdateCursor(fcpk, ["ozn_przezn", "przezn", "d_ozn_prze", "d_przezn"]) as cursor:
    for row in cursor:
        row[0] = row[2]
        row[1] = row[3]
        cursor.updateRow(row)

arcpy.management.DeleteField(fcpk, "d_przezn;d_ozn_prze", "DELETE_FIELDS")

fcpk = r"{}\PRZEZ_KOM.shp".format(fold_doc)
arcpy.management.AddField(fcpk, "text", "TEXT", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')

with arcpy.da.UpdateCursor(fcpk, ["ozn_przezn", "text", "nr_terenu"])  as cursor:
    for row in cursor:
        row[1] = row[2]+"-"+row[0]
        cursor.updateRow(row)

fcpu = r"{}\PRZEZ_ULICE.shp".format(fold_doc)

arcpy.management.DeleteField(fcpu, "ozn_przezn", "DELETE_FIELDS")
arcpy.management.AddField(fcpu, "ozn_przezn", "TEXT", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')

with arcpy.da.UpdateCursor(fcpu, ["ozn_przezn", "przekroj", "tramwaj", "chodnik", "rower", "parkowanie", "szp_drzew", "d_ozn_prze", "d_przekroj", "d_tramwaj", "d_chodnik", "d_rower", "d_parkowan", "d_szp_drze" ]) as cursor:
    for row in cursor:
        row[0] = row[7]
        row[1] = row[8]
        row[2] = row[9]
        row[3] = row[10]
        row[4] = row[11]
        row[5] = row[12]
        row[6] = row[13]
        cursor.updateRow(row)

arcpy.management.DeleteField(fcpu, "d_ozn_prze;d_przekroj;d_tramwaj;d_chodnik;d_rower;d_parkowan;d_szp_drze", "DELETE_FIELDS")

fcpu = r"{}\PRZEZ_ULICE.shp".format(fold_doc)
arcpy.management.AddField(fcpu, "text", "TEXT", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')

with arcpy.da.UpdateCursor(fcpu, ["ozn_przezn", "text", "nr_terenu"])  as cursor:
    for row in cursor:
        row[1] = row[2]+"-"+row[0]
        cursor.updateRow(row)

if arcpy.Exists("PRZEZ_MIX"):
#if "PRZEZ_MIX" in [layer.name for layer in mpzpMap.listLayers()]:
    fcpm = r"{}\PRZEZ_MIX.shp".format(fold_doc)

    arcpy.management.DeleteField(fcpm, "ozn_przezn", "DELETE_FIELDS")
    arcpy.management.AddField(fcpm, "ozn_przezn", "TEXT", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')
    
    with arcpy.da.UpdateCursor(fcpm, ["f1", "f2", "f3", "ozn_przezn", "przekroj", "tramwaj", "chodnik", "rower", "parkowanie", "szp_drzew", "d_f1", "d_f2", "d_f3", "d_ozn_prze", "d_przekroj", "d_tramwaj", "d_chodnik", "d_rower", "d_parkowan", "d_szp_drze"]) as cursor:
        for row in cursor:
            row[0] = row[10]
            row[1] = row[11]
            row[2] = row[12]
            row[3] = row[13]
            row[4] = row[14]
            row[5] = row[15]
            row[6] = row[16]
            row[7] = row[17]
            row[8] = row[18]
            row[9] = row[19]
            cursor.updateRow(row)
            
    arcpy.management.DeleteField(fcpm, "d_f1;d_f2;d_f3;d_ozn_prze;d_przekroj;d_tramwaj;d_chodnik;d_rower;d_parkowan;d_szp_drze", "DELETE_FIELDS")

    fcpm = r"{}\PRZEZ_MIX.shp".format(fold_doc)
    arcpy.management.AddField(fcpm, "text", "TEXT", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')
    
    with arcpy.da.UpdateCursor(fcpm, ["ozn_przezn", "text", "nr_terenu"])  as cursor:
        for row in cursor:
            row[1] = row[2]+"-"+row[0]
            cursor.updateRow(row)

else:
    pass

fcg = r"{}\GRANICA.shp".format(fold_doc)

arcpy.management.DeleteField(fcg, "skala", "DELETE_FIELDS")
arcpy.management.AddField(fcg, "skala", "TEXT", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')

with arcpy.da.UpdateCursor(fcg, ["dziel_urb", "jedn_urban", "autor", "status", "typ_uniew", "ukl_wsp", "skala", "d_dziel_ur", "d_jedn_urb", "d_autor", "d_status", "d_typ_unie", "d_ukl_wsp", "d_skala"]) as cursor:
    for row in cursor:
        row[0] = row[7]
        row[1] = row[8]
        row[2] = row[9]
        row[3] = row[10]
        row[4] = row[11]
        row[5] = row[12]
        row[6] = row[13]
        cursor.updateRow(row)

arcpy.management.DeleteField(fcg, "d_dziel_ur;d_jedn_urb;d_autor;d_status;d_typ_unie;d_ukl_wsp;d_skala", "DELETE_FIELDS")

os.rename(fcg, r'{0}\GRANICA_{1}.shp'.format(fold_doc, nr_planu))
os.rename(r'{}\GRANICA.cpg'.format(fold_doc), r'{0}\GRANICA_{1}.cpg'.format(fold_doc, nr_planu))
os.rename(r'{}\GRANICA.dbf'.format(fold_doc), r'{0}\GRANICA_{1}.dbf'.format(fold_doc, nr_planu))
os.rename(r'{}\GRANICA.prj'.format(fold_doc), r'{0}\GRANICA_{1}.prj'.format(fold_doc, nr_planu))
os.rename(r'{}\GRANICA.sbn'.format(fold_doc), r'{0}\GRANICA_{1}.sbn'.format(fold_doc, nr_planu))
os.rename(r'{}\GRANICA.sbx'.format(fold_doc), r'{0}\GRANICA_{1}.sbx'.format(fold_doc, nr_planu))
os.rename(r'{}\GRANICA.shx'.format(fold_doc), r'{0}\GRANICA_{1}.shx'.format(fold_doc, nr_planu))
os.rename(r'{}\GRANICA.shp.xml'.format(fold_doc), r'{0}\GRANICA_{1}.shp.xml'.format(fold_doc, nr_planu))

if arcpy.Exists("PRZEZ_MIX"):
    with arcpy.EnvManager(outputCoordinateSystem='PROJCS["ETRS_1989_Poland_CS2000_Zone_6",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",6500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",18.0],PARAMETER["Scale_Factor",0.999923],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'):
        arcpy.management.Merge(r"{0}\PRZEZ.shp;{0}\PRZEZ_INFR.shp;{0}\PRZEZ_KOM.shp;{0}\PRZEZ_MIX.shp;{0}\PRZEZ_ULICE.shp".format(fold_doc),
                               r"{0}\PRZEZ_ALL_{1}.shp".format(fold_doc, nr_planu),
                               r'nr_mpzp "nr_mpzp" true true false 10 Text 0 0,First,#,{0}\PRZEZ.shp,nr_mpzp,0,10,{0}\PRZEZ_INFR.shp,nr_mpzp,0,10,{0}\PRZEZ_KOM.shp,nr_mpzp,0,10,{0}\PRZEZ_MIX.shp,nr_mpzp,0,10,{0}\PRZEZ_ULICE.shp,nr_mpzp,0,10;nr_terenu "nr_terenu" true true false 2 Text 0 0,First,#,{0}\PRZEZ.shp,nr_terenu,0,2,{0}\PRZEZ_INFR.shp,nr_terenu,0,2,{0}\PRZEZ_KOM.shp,nr_terenu,0,2,{0}\PRZEZ_MIX.shp,nr_terenu,0,3,{0}\PRZEZ_ULICE.shp,nr_terenu,0,2;przezn "przezn" true true false 254 Text 0 0,First,#,{0}\PRZEZ.shp,przezn,0,254,{0}\PRZEZ_INFR.shp,przezn,0,254,{0}\PRZEZ_KOM.shp,przezn,0,254,{0}\PRZEZ_MIX.shp,przezn,0,254,{0}\PRZEZ_ULICE.shp,przezn,0,254;pow "pow" true true false 19 Double 0 0,First,#,{0}\PRZEZ.shp,pow,-1,-1,{0}\PRZEZ_INFR.shp,pow,-1,-1,{0}\PRZEZ_KOM.shp,pow,-1,-1,{0}\PRZEZ_MIX.shp,pow,-1,-1,{0}\PRZEZ_ULICE.shp,pow,-1,-1;ozn_przezn "ozn_przezn" true true false 254 Text 0 0,First,#,{0}\PRZEZ.shp,ozn_przezn,0,254,{0}\PRZEZ_INFR.shp,ozn_przezn,0,254,{0}\PRZEZ_KOM.shp,ozn_przezn,0,254,{0}\PRZEZ_MIX.shp,ozn_przezn,0,254,{0}\PRZEZ_ULICE.shp,ozn_przezn,0,254;text "text" true true false 254 Text 0 0,First,#,{0}\PRZEZ.shp,text,0,254,{0}\PRZEZ_INFR.shp,text,0,254,{0}\PRZEZ_KOM.shp,text,0,254,{0}\PRZEZ_MIX.shp,text,0,254,{0}\PRZEZ_ULICE.shp,text,0,254'.format(fold_doc), "NO_SOURCE_INFO")
else:
    with arcpy.EnvManager(outputCoordinateSystem='PROJCS["ETRS_1989_Poland_CS2000_Zone_6",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",6500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",18.0],PARAMETER["Scale_Factor",0.999923],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'):
        arcpy.management.Merge(r"{0}\PRZEZ.shp;{0}\PRZEZ_INFR.shp;{0}\PRZEZ_KOM.shp;{0}\PRZEZ_ULICE.shp".format(fold_doc),
                               r"{0}\PRZEZ_ALL_{1}.shp".format(fold_doc, nr_planu),
                               r'nr_mpzp "nr_mpzp" true true false 10 Text 0 0,First,#,{0}\PRZEZ.shp,nr_mpzp,0,10,{0}\PRZEZ_INFR.shp,nr_mpzp,0,10,{0}\PRZEZ_KOM.shp,nr_mpzp,0,10,{0}\PRZEZ_MIX.shp,nr_mpzp,0,10,{0}\PRZEZ_ULICE.shp,nr_mpzp,0,10;nr_terenu "nr_terenu" true true false 2 Text 0 0,First,#,{0}\PRZEZ.shp,nr_terenu,0,2,{0}\PRZEZ_INFR.shp,nr_terenu,0,2,{0}\PRZEZ_KOM.shp,nr_terenu,0,2,{0}\PRZEZ_MIX.shp,nr_terenu,0,3,{0}\PRZEZ_ULICE.shp,nr_terenu,0,2;przezn "przezn" true true false 254 Text 0 0,First,#,{0}\PRZEZ.shp,przezn,0,254,{0}\PRZEZ_INFR.shp,przezn,0,254,{0}\PRZEZ_KOM.shp,przezn,0,254,{0}\PRZEZ_MIX.shp,przezn,0,254,{0}\PRZEZ_ULICE.shp,przezn,0,254;pow "pow" true true false 19 Double 0 0,First,#,{0}\PRZEZ.shp,pow,-1,-1,{0}\PRZEZ_INFR.shp,pow,-1,-1,{0}\PRZEZ_KOM.shp,pow,-1,-1,{0}\PRZEZ_MIX.shp,pow,-1,-1,{0}\PRZEZ_ULICE.shp,pow,-1,-1;ozn_przezn "ozn_przezn" true true false 254 Text 0 0,First,#,{0}\PRZEZ.shp,ozn_przezn,0,254,{0}\PRZEZ_INFR.shp,ozn_przezn,0,254,{0}\PRZEZ_KOM.shp,ozn_przezn,0,254,{0}\PRZEZ_MIX.shp,ozn_przezn,0,254,{0}\PRZEZ_ULICE.shp,ozn_przezn,0,254;text "text" true true false 254 Text 0 0,First,#,{0}\PRZEZ.shp,text,0,254,{0}\PRZEZ_INFR.shp,text,0,254,{0}\PRZEZ_KOM.shp,text,0,254,{0}\PRZEZ_MIX.shp,text,0,254,{0}\PRZEZ_ULICE.shp,text,0,254'.format(fold_doc), "NO_SOURCE_INFO")

    

arcpy.management.PackageProject(aprxFile, r"{}\{}.ppkx".format(fold_doc, nr_planu), "INTERNAL", "PROJECT_PACKAGE",
                                "DEFAULT", "ALL", None, f"MPZP nr {nr_planu}", "MPZP, BRG", "CURRENT",
                                "NO_TOOLBOXES", "NO_HISTORY_ITEMS", "READ_WRITE", "KEEP_ALL_RELATED_ROWS")

arcpy.AddMessage(fold_doc)                                      
arcpy.AddMessage("Brawo! Architektura będzie przeszczęśliwa")


#aprx.save()

