
# coding: utf-8

# 1. Import system modules
import arcpy
import os
from arcpy import env

# Adding fields and autopopulating for some in ... mua, ... gfp, and ...gfl.

# 2. Set environment settings
# Put in the workspace location to the .gdb (ex. P:\Map_Data_Model\MAPS\Florence_Co_Pleisto\Florence_Co_Pleisto_Working.gdb)
env.workspace = "N:\TestCode\Florence_Co_Pleisto_Working.gdb"

# 3. Set inFeature variables
# Calling the name of the feature/layers you want to work with (ex. bn_bedgeo_GeologyUnitAreas)

# If you *do not* want to work with a certain layer, simply set the variable to a value which is "falsy" or interpreted as false in an 'if' statement.  
# the following values are interpreted as false (case-sensitive): False, None, numeric zero of all types, and empty strings and containers (including strings, tuples, lists, dictionaries, sets and frozensets). 
# All other values (such as a non-empty string) are interpreted as true.
# https://docs.quantifiedcode.com/python-anti-patterns/readability/comparison_to_true.html

inFeatures_mua = "fc_pg_MapUnitArea_1"             # Change this to whatever your mua layer is called. Set as an empty string or False or None to skip it. 
inFeatures_gfp = False             # Change this to whatever your gfp layer is called. Set as an empty string or False or None to skip it. 
inFeatures_GeologicLines = "fc_pg_GeoFeatLine_S_1_GeologicalLines"       # Change this to whatever your GeologicLines layer (or if split the GeologicLines) is called. Set as an empty string or False or None to skip it. 
inFeatures_ContactsAndFaults = "fc_pg_GeoFeatLine_B_1_ContactAndFaults"   # Change this to whatever your ContactsAndFaults layer is called. If the lines are split, use this as the ContactsAndFaults, may need to set this to empty string or False or None if no split lines
addOrientationPoints = False                      # indicate whether to include an empty orientationpoints layer. 


# 4. Set variables to be executed in expressions

# 4.1 defaultvalues from GeMS manual
x= -9          # Used in gfp.LocationConfidenceMeters, gfp.OrientationConfidenceDegrees, and gfl.LocationConfidenceMeters
x0= "('N')"    # used for the 'IsConcealed' field
x1 = 0         # Used in gfp.PlotAtScale
x2 = "('certain')" # Used in mua.IdentityConfidence, gfp.IdentityConfidence, gfl.ExistenceConfidence, and gfl.IdentityConfidence

# 4.2 Inputs from other columns

# from within the polygon layer
# x3 is equal to the column in the polygon layer that has the polygon MapUnits. (Ex. UNAME, Units)
x3 = "(!UNAME!)"

# from within the points layer
# Type, (ex. Type, Type_Original, Original_Type)
x4 = "(!Original_Type!)"

# from within the GeologicLines layer,  (ex. Type, Type_Original)
# Type
x5 = "(!UniqCode!)"

# ContactsAndFaults,  (ex. Type, Type_Original)
x6 = "(!UniqCode!)"





#------------------------POLYGON------------------------------------#


# 5. Layer for polygons (mua).
# This layer doesn't really change with what columns you are adding and populating
def polygonsLayer():
    try: 

        # 5.1 Set local variables and the names fields to be added.

        # Name of the fields you want to add for the polygons
        # Columns in the GeMS ...mua are typically: map unit**, identity confidence**, label**, symbol, datasourceid, notes, and MapUnitPolys_ID
        # (* are the columns added and populated before GeMS gdb, ** are populate with the code)

        fieldName1 = "MapUnit"            # text
        fieldName2 = "Label"              # text
        fieldName3 = "IdentityConfidence" # text


        # 5.2 Expression variables to be executed in the CalculateField.
        # MapUnit and Label are equal to each other and the column that has the polygon types.
        expression1 = x3 # Pulls from the column with values that match the MapUnit.
        expression2 = x3 # Pulls from the column with values that match the Label.

        # x2 is equal to "certain" which is the default value for IdentityConfidence.
        expression3 = x2 # Inputs the suggested default value for IdentityConfidence.


        #  5.3 Execute AddField. The format for AddField is: AddField(in_table, field_name, field_type, field_precision, field_scale, field_length, field_alias, field_is_nullable, field_is_required, field_domain)
        arcpy.AddField_management(inFeatures_mua, fieldName1, "TEXT") #http://webhelp.esri.com/arcgisdesktop/9.2/index.cfm?id=1548&pid=1547&topicname=Add_Field_%28Data_Management%29
        arcpy.AddField_management(inFeatures_mua, fieldName2, "TEXT", "", "", "", "", "NULLABLE") # This field accepts Null values.
        arcpy.AddField_management(inFeatures_mua, fieldName3, "TEXT")

       # 5.4 Execute CalculateField 
        arcpy.CalculateField_management(inFeatures_mua, fieldName1, expression1, "PYTHON") # In the mua layer for MapUnit, field equal to UNAME field.
        arcpy.CalculateField_management(inFeatures_mua, fieldName2, expression2, "PYTHON") # In the mua layer for Label, field equal to UNAME field.
        arcpy.CalculateField_management(inFeatures_mua, fieldName3, expression3, "PYTHON") # In the mua layer for IdentityConfidence, field defaults to "certain".

    # 5.5 If an error occurred, print line number and error message
    except Exception as e:
        import traceback, sys
        tb = sys.exc_info()[2]
        print ("Line %i" % tb.tb_lineno)
        print (e.message) 

    
    
    
    
#------------------------POINTS------------------------------------#

# 6. Next layer, points (gfp).
def pointsLayer():
    try: 
        # 6.1 Set local variables

        #### ----- START General Points ----- ####

        # Columns in the GeMS ...gfp are typically: Type**, LocationConfidenceMeters**(default value = -9, or x), PlotAtScale** (default = 0, or x1), MapUnit* 
        # Others that might be added: Symbol (null), Label (null), StationID(null), Notes, TableName_ID
        # (* are the columns added and populated before GeMS gdb, ** are populate with the code)

        #Adding names of fields to add
        fieldName1 = "Type_points" #text
        fieldName2 = "LocationConfidenceMeters" #float
        fieldName3 = "PlotAtScale" #float
        fieldName4 = "MapUnit" #text

        # create a fieldlength parameter to help with Type that has a long text.
        fieldlength = 1000

        # 6.2 Expression variables to be executed in the CalculateField.
        expression1 = x4
        expression2 = x
        expression3 = x1
        ##Typically need to populate the MapUnit column by doing a join in ArcMaps
        #expression4 = 

        # 6.3 Execute AddField
        arcpy.AddField_management(inFeatures_gfp, fieldName1, "TEXT", "", "", fieldlength)
        arcpy.AddField_management(inFeatures_gfp, fieldName2, "FLOAT")
        arcpy.AddField_management(inFeatures_gfp, fieldName3, "FLOAT")
        arcpy.AddField_management(inFeatures_gfp, fieldName4, "TEXT")

        # 6.4 Execute CalculateField with expression variables
        arcpy.CalculateField_management(inFeatures_gfp, fieldName1, expression1, "PYTHON")
        arcpy.CalculateField_management(inFeatures_gfp, fieldName2, expression2, "PYTHON")
        arcpy.CalculateField_management(inFeatures_gfp, fieldName3, expression3, "PYTHON") 

        ####END General Points####
    except Exception as e:
        import traceback, sys
        tb = sys.exc_info()[2]
        print ("Line %i" % tb.tb_lineno)
        print (e.message)

def addOrientationPointsLayer():
       
    try:
        ####START Orientation Points####

        # Columns in the GeMS ...gfp are typically: Type**, LocationConfidenceMeters**(default value = -9, or x), PlotAtScale** (default = 0, or x1), MapUnit*, IdentityConfidence**, OrientationConfidenceDegrees** 
        # Others that might be added: Inclination, Symbol (null), Label (null), StationID(null), LocationSourceID, OrientationSource_ID, Notes, OrientationPoints_ID
        # (* are the columns added and populated before GeMS gdb, ** are populate with the code)


        #Adding names of fields to add
        fieldName1 = "Type" #text
        fieldName2 = "LocationConfidenceMeters" #float, default = -9, or x
        fieldName3 = "PlotAtScale" #float, default = 0, or x1
        fieldName4 = "MapUnit" #text

        fieldName5 = "Azimuth" #float, no null, limited to 0-360
        fieldName6 = "IdentityConfidence" #text, default = "certain", or x2
        fieldName7 = "OrientationConfidenceDegrees" #float, default = -9, or x
        fieldName8 = "Inclination" #float, range -90 to 90, default = 0, or x1

        # create a fieldlength parameter to help with Type that has a long text.
        fieldlength = 1000

        # 6.2 Expression variables to be executed in the CalculateField.
        expression1 = x4
        expression2 = x
        expression3 = x1
        ##Typically need to populate the MapUnit column by doing a join in ArcMaps
        #expression4 =  
        #expression5 = y1
        expression6 = x2
        expression7 = x
        expression8 = x1

        # 6.3 Execute AddField
        arcpy.AddField_management(inFeatures_gfp2, fieldName1, "TEXT", "", "", fieldlength)
        arcpy.AddField_management(inFeatures_gfp2, fieldName2, "FLOAT")
        arcpy.AddField_management(inFeatures_gfp2, fieldName3, "FLOAT")
        arcpy.AddField_management(inFeatures_gfp2, fieldName4, "TEXT")
        arcpy.AddField_management(inFeatures_gfp2, fieldName5, "FLOAT")
        arcpy.AddField_management(inFeatures_gfp2, fieldName6, "TEXT")
        arcpy.AddField_management(inFeatures_gfp2, fieldName7, "FLOAT")
        arcpy.AddField_management(inFeatures_gfp2, fieldName8, "FLOAT")

        # 6.4 Execute CalculateField with expression variables
        arcpy.CalculateField_management(inFeatures_gfp2, fieldName1, expression1, "PYTHON") # In the gfp layer for LocationConfidenceMeters, default value of -9.
        arcpy.CalculateField_management(inFeatures_gfp2, fieldName2, expression2, "PYTHON") # In the gfp layer for IdentityConfidence, default value of "certain".
        arcpy.CalculateField_management(inFeatures_gfp2, fieldName3, expression3, "PYTHON") # In the gfp layer for OrientationConfidenceDegrees, default value of -9.
        #arcpy.CalculateField_management(inFeatures_gfp2, fieldName1, expression5, "PYTHON") # In the gfp layer for LocationConfidenceMeters, default value of -9.
        arcpy.CalculateField_management(inFeatures_gfp2, fieldName2, expression6, "PYTHON") # In the gfp layer for IdentityConfidence, default value of "certain".
        arcpy.CalculateField_management(inFeatures_gfp2, fieldName3, expression7, "PYTHON") # In the gfp layer for OrientationConfidenceDegrees, default value of -9.
        arcpy.CalculateField_management(inFeatures_gfp2, fieldName3, expression8, "PYTHON") # In the gfp layer for OrientationConfidenceDegrees, default value of -9.


        ###END Orientation Points####


    # 6.5 If an error occurred, print line number and error message
    except Exception as e:
        import traceback, sys
        tb = sys.exc_info()[2]
        print ("Line %i" % tb.tb_lineno)
        print (e.message)
  
   


#--------------------LINES--------------------------------#



# 7. Next layer for lines (gfl).


def geolinesLayer():
    try: 
        ####START GeologicLines, and All lines if in same layer (if lines already split use GeologicLines too below)####

        # Columns in the GeMS ...gfl GeologicLines are typically: Type**, IsConcealed** (default = "N", or x0), LocationConfidenceMeters** (default = -9, or x), ExistenceConfidence** (default = "certain", or x2), IdentityConfidence** (default = "certain", or x2)
        # Others that might be added or filled in GeMS: Label, Symbol, DataSourceID, Notes, GeologicLines_ID
        # (* are the columns added and populated before GeMS gdb, ** are populate with the code)

        # 7.1 Set local variables

        #Adding names of fields to add
        fieldName1 = "Type_GeologicLines" #text, x5
        fieldName2 = "IsConcealed" #text, default = "N", or x0
        fieldName3 = "LocationConfidenceMeters" #float
        fieldName4 = "ExistenceConfidence"#text
        fieldName5 = "IdentityConfidence" #text

        # create a fieldlength parameter to help with Type that has a long text.
        fieldlength = 1000

        # 7.2 Expression variables to be executed in the CalculateField.
        expression1 = x5
        expression2 = x0
        expression3 = x
        expression4 = x2
        expression5 = x2

        # 7.3 Execute AddField
        arcpy.AddField_management(inFeatures_GeologicLines, fieldName1, "TEXT", "", "", fieldlength)
        arcpy.AddField_management(inFeatures_GeologicLines, fieldName2, "TEXT", "", "")
        arcpy.AddField_management(inFeatures_GeologicLines, fieldName3, "FLOAT", "", "")
        arcpy.AddField_management(inFeatures_GeologicLines, fieldName4, "TEXT", "", "")
        arcpy.AddField_management(inFeatures_GeologicLines, fieldName5, "TEXT", "", "")

        # 7.4 Execute CalculateField with expression variables 
        arcpy.CalculateField_management(inFeatures_GeologicLines, fieldName1, expression1, "PYTHON") # In the gfl layer for LocationConfidenceMeters, default value of -9.
        arcpy.CalculateField_management(inFeatures_GeologicLines, fieldName2, expression2, "PYTHON") # In the gfl layer for ExistenceConfidence, default value of "certain".
        arcpy.CalculateField_management(inFeatures_GeologicLines, fieldName3, expression3, "PYTHON") # In the gfl layer for IdentityConfidence, default value of "certain".
        arcpy.CalculateField_management(inFeatures_GeologicLines, fieldName4, expression4, "PYTHON")
        arcpy.CalculateField_management(inFeatures_GeologicLines, fieldName5, expression5, "PYTHON")


    # 7.5 If an error occurred, print line number and error message
    except Exception as e:
        import traceback, sys
        tb = sys.exc_info()[2]
        print ("Line %i" % tb.tb_lineno)
        print (e.message)

    ####END GeologicLines####



def contactsLayer():
    try: 
        ####START ContactsAndFaults####

        ##Columns in the GeMS ...gfl ContactsAndFaults are typically: Type**, IsConcealed** (default = "N", or x0), LocationConfidenceMeters** (default = -9, or x), ExistenceConfidence** (default = "certain", or x2), IdentityConfidence** (default = "certain", or x2)
        ##Others that might be added or filled in GeMS: Label, Symbol, DataSourceID, Notes, ContactAndFaults_ID
        ##(* are the columns added and populated before GeMS gdb, ** are populate with the code)

        # 7.1 Set local variables

        #Adding names of fields to add
        fieldName1 = "Type_ContactsandFaults" #text, x6
        fieldName2 = "IsConcealed" #text, default = "N", or x0
        fieldName3 = "LocationConfidenceMeters" #float
        fieldName4 = "ExistenceConfidence"#text
        fieldName5 = "IdentityConfidence" #text

        # create a fieldlength parameter to help with Type that has a long text.
        fieldlength = 1000

        # 7.2 Expression variables to be executed in the CalculateField.
        expression1 = x6
        expression2 = x0
        expression3 = x
        expression4 = x2
        expression5 = x2

        # 7.3 Execute AddField
        arcpy.AddField_management(inFeatures_ContactsAndFaults, fieldName1, "TEXT", "", "", fieldlength)
        arcpy.AddField_management(inFeatures_ContactsAndFaults, fieldName2, "TEXT", "", "")
        arcpy.AddField_management(inFeatures_ContactsAndFaults, fieldName3, "FLOAT", "", "")
        arcpy.AddField_management(inFeatures_ContactsAndFaults, fieldName4, "TEXT", "", "")
        arcpy.AddField_management(inFeatures_ContactsAndFaults, fieldName5, "TEXT", "", "")

       #  7.4 Execute CalculateField with expression variables 
        arcpy.CalculateField_management(inFeatures_ContactsAndFaults, fieldName1, expression1, "PYTHON") # In the gfl layer for LocationConfidenceMeters, default value of -9.
        arcpy.CalculateField_management(inFeatures_ContactsAndFaults, fieldName2, expression2, "PYTHON") # In the gfl layer for ExistenceConfidence, default value of "certain".
        arcpy.CalculateField_management(inFeatures_ContactsAndFaults, fieldName3, expression3, "PYTHON") # In the gfl layer for IdentityConfidence, default value of "certain".
        arcpy.CalculateField_management(inFeatures_ContactsAndFaults, fieldName4, expression4, "PYTHON")
        arcpy.CalculateField_management(inFeatures_ContactsAndFaults, fieldName5, expression5, "PYTHON")


    # 7.5 If an error occurred, print line number and error message
    except Exception as e:
        import traceback, sys
        tb = sys.exc_info()[2]
        print ("Line %i" % tb.tb_lineno)
        print (e.message)


    ####END ContactsAndFaults####

    
# 8. for each layer, if a truthy value is provided above in section 3, call the function to handle that layer.  
# These appear at the bottom of the script because in Python we must define functions before we can call them


if inFeatures_mua: 
    polygonsLayer()

if inFeatures_gfp: 
      pointsLayer()

if addOrientationPoints: 
      addOrientationPointsLayer() 
  
if inFeatures_GeologicLines: 
      geolinesLayer()
  
if inFeatures_ContactsAndFaults: 
      contactsLayer()




