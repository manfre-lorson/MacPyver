# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 16:49:28 2018

@author: Florian Wolf


            __________________________________________________
            ###              MacPyver.vector               ###
            ###   The Swissknife like Python-Package for   ###
            ###        work in general and with GIS        ###
            __________________________________________________

"""

import os
import pandas as pd
from osgeo import ogr
import numpy as np
#import cPickle as pickle

class shp_attr_tbl():
    ''' put in full path of shp file

        init creates list of fieldnames in the shape

        with the method get_attr_tbl it reads in the dbf to a pandas dataframe
        
        possible to read dbf's directly to dataframe, just put ending .dbf instead
        of .shp
        '''

    def __init__(self,shp_name):
        #dictionary to translate the geometry
        _geometry_dic = {-2147483647:"Point25D",
                         -2147483646:"LineString25D",
                         -2147483645:"Polygon25D",
                         -2147483644:"MultiPoint25D",
                         -2147483643:"MultiLineString25D",
                         -2147483642:"MultiPolygon25D",
                         0: "Geometry",
                         1: "Point",
                         2: "Line",
                         3:"Polygon",
                         4:"MultiPoint",
                         5: "MultiLineString",
                         6: "MultiPolygon",
                         100: "No Geometry"}

        self.name =shp_name.split(os.sep)[-1]
        self.path = (os.sep).join(shp_name.split(os.sep)[:-1])
        driver = ogr.GetDriverByName("ESRI Shapefile")
        ds = driver.Open(shp_name)
        layer = ds.GetLayer()
        layerDefinition = layer.GetLayerDefn()
        self.fieldnames = []
        if not shp_name.endswith('.dbf'):
            self.geometrytype = _geometry_dic[layer.GetGeomType()]
            self.extent = layer.GetExtent()
            self.spatialref = layer.GetSpatialRef().ExportToPrettyWkt()
            self.featurecount = layer.GetFeatureCount()

        for i in range(layerDefinition.GetFieldCount()):
            self.fieldnames.append(layerDefinition.GetFieldDefn(i).GetName())
            
    def get_attr_tbl(self, fields = None):
        '''if no fields passed, it will read in all columns,
            if some field passed, it will just read this subset

            returned data is pandas dataframe'''

        if not fields:
            used_fields = self.fieldnames
        else:
            #create difference list
            diffl = list(set(fields).difference(self.fieldnames))
            #create intersection list
            intersl = list(set(fields).intersection(self.fieldnames))
            if diffl:
                print ("ERROR: one or more fields are not in fieldnames:\n{0}".format(diffl))
                print ("used matching fields to create the attribute table:\n{0}".format(intersl))
            #create list of columns (fields) to use
            used_fields = intersl

        #create empty dictionary to store all values
        dic = {}
        for fi in used_fields:
            dic[fi] = []

        #reset pointer to begining of the file
        driver = ogr.GetDriverByName("ESRI Shapefile")
        ds = driver.Open(self.path + os.sep + self.name)
        layer = ds.GetLayer()

        #fill dic per row in layer / and per field
        for feature in layer:
            for fi in used_fields:
                get_value = feature.GetField(fi)
                #if missing value np.nan is assigned
                if not get_value:
                    get_value = np.nan
                dic[fi].append(get_value)
        #save as pd in object
        self.attributes  = pd.DataFrame(dic)

    def to_csv(self, outpath, sep = ';', na_rep= 'NaN'):
        '''writes the dataframe to csv,
        to use the all opotions, just use name.attributes.to_csv()'''

        if hasattr(self, 'attributes'):
            self.attributes.to_csv(outpath, sep, na_rep)
        else:
            print("ERROR: no data to write\nuse >>> .get_attr_tbl first")

    def stats(self, min_max=False):
        if hasattr(self,'geometrytype') :
            '''prints several infos of the passed shp'''

            _dtype_dic = {'int64':'int', 'object':'string', 'float64':'float'}
            if not hasattr(self, 'attributes'):
                self.get_attr_tbl()
            rows , cols = self.attributes.shape
            print ('\n')
            print ('directory:',self.path)
            print ('filename:',self.name)
            print ('\nshape: columns: {0}; rows: {1}\n'.format(cols, rows))
            print (self.spatialref)
            print ("\nGeometryType: {0}".format(self.geometrytype))

            print ("\nExtent (lon min, lon max, lat min, lat max)")
            print ("{0}\n".format(self.extent))
            #to make the printing nice
            #get length of the longest fieldname and use it for printing
            maxlen = len(max(self.fieldnames, key=len))
            colname ='Column Name'
            if len(colname)>=maxlen:
                maxlen = len(colname)
            if min_max:
                min_max='| min, max'
            else:
                min_max = ''
            print (colname+" "*maxlen)[:maxlen+2]+"| dtype    "+min_max
            if min_max:
                add = 12
            else:
                add = 0
            print ("-"*(maxlen+2+10+add))

            for x in self.fieldnames:
                if min_max:
                    if _dtype_dic[str(self.attributes[x].dtype)] == 'float':
                        minmax = "| not created because its float"
                    else:
                        unique = list(set(self.attributes[x]))
                        unique.sort()
                        minV, maxV = unique[0], unique[-1]
                        minmax = "| {0}, {1}".format(minV, maxV)
                else:
                    minmax = ''

                print('{0} | {1} {2}'.format( (x+" "*maxlen)[:maxlen+1],(_dtype_dic[str(self.attributes[x].dtype)]+'  '*4)[:8], minmax ))
                #print (x+" "*maxlen)[:maxlen+1],'|', (self.attributes[x].dtype +'     ')[:8]+ ' | ' + 
        else:
            print('WARNING: no stats due to missing geometry, file was a dbf')
                
    def uniqueValue(self, ColumnName):
        '''returns the unique values of the specified column'''

        if ColumnName not in self.fieldnames:
            print ('ERROR: ColumnName does not exists in  fieldnames')
            print ('Check existing names with *.fieldnames')
        if self.attributes[ColumnName].dtype in [np.int, np.int8, np.int16, np.int32, np.int64, np.object]:
            return list(set(self.attributes[ColumnName]))
        else:
            print ("ERROR: function was not build to create unique values from floats")
            print ("to do that use: foo = set(*.attributes[ColumnName])")


if __name__=='__main__':
    '''can be used as stand alone commandline tool\n
    all the script with a shapefile'''

    import argparse
    parser = argparse.ArgumentParser(description='    prints the information of the passed shp file\n\
    is part of the python site-package MacPyver\n\
    https://github.com/manfre-lorson/MacPyver\n', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('infile',
                help='put in the full path input file, with filename (shapefile)\nextension dosent matter (can be dbf/prj/shp/shx/...)',
                type=str#argparse.FileType('r')
                )
    parser.add_argument('-w','--wait',
                        help='you are willing to wait until all entries are sorted \nand you get the min and max value per column',
                        default=False, action='store_true')

    parse = parser.parse_args()
    #assign variables
    infile = parse.infile
    wait = parse.wait

    #check if file exists
    if not infile.endswith('.shp'):
        infile = infile[:infile.rfind('.')]+'.shp'
    if not os.path.exists(infile):
        print ('\nERROR: file {0} dosent exists in the filesystem'.format(infile))
    else:
        shp = shp_attr_tbl(infile)

        if wait:
            shp.stats(1)
        elif shp.featurecount > 10000:
            shp.stats()
            print ("\nWARNING: didnt do the min-max values because of to many entries")
            print ("If you are willing to wait use the -w flag")
        else:
            shp.stats(1)

'''
for windows users: for an easy use of the commandline, do:
create a ogrinfo2.bat file in a directory which is in your windows path variable (if you are able to use the gdal commands from the cmd
just put the created .bat in the same directory)

inside the .bat you need to have the following (you need to adjust your paths)

@echo off
set args1=%1
set args2=%2
C:\Anaconda2\python.exe C:\Anaconda2\lib\site-packages\MacPyver\vector\__init__.py %args1% %args2%

save this and then you can run it directly from your cmd '''


"""
#save dataframe:
def save_df(dataframe, fullpath, timeit=False):
    '''
    uses the c function of pickle,
    there is also a normal pure python pickle function
    -- but not here

    save a pandas dataframe as pickle format
    https://docs.python.org/2/library/pickle.html
    
    '''
    if timeit:
        from datetime import datetime
        start = datetime.now()
    pickle.dump( dataframe, open(fullpath, 'wb'))
    if timeit:
        stop = datetime.now()
        print ('duration:', stop - start)

def read_df(fullpath, timeit = False):
    '''
    read pickled datarame into pandas dataframe
    '''
    if timeit:
        from datetime import datetime
        start = datetime.now()
    ret =  pickle.load( open(fullpath, 'rb'))
    if timeit:
        stop = datetime.now()
        print ('duration:', stop - start)
    return ret
"""