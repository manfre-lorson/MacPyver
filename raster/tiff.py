# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:12:36 2016

@author: Floiran Wolf
"""

import osgeo.gdalnumeric as zz_gdalnum
import osgeo.gdalconst as zz_gdalcon



def Help(inhal = ''):
    HelpInhalt =  sorted(['read_tif', 'read_tif_info', 'write_tif'])
    if inhal =='':
        inhal = HelpInhalt
    inhalt = inhal
    if type(inhalt)== str:
        cList = []
        cList.append(inhalt)
        cList.append("nix")
        inhalt = cList
        
    myDic = {"header": """        
            __________________________________________________
	    ###            MacPyver.raster.tiff            ###
            ###   The Swissknife like Python-Package for   ###
            ###        work in general and with GIS        ###
            __________________________________________________
                
                How to use the functions:
                __________
                
                __________________________________________
                
             """,
             
            "read_tif":"""read_tif:       
                to read a tif into python
                
                >>> data = read_tif(fullPath, bandNr)
                
                fullPath --> full path plus the filename
                bandNr   --> the number of the band you want to read

                ______________________________________________________________________
            """,
            
            "read_tif_info":"""read_tif_info:  
                read infos from tif
                
                >>> inTif, driver, inCols, inRows = read_tif_info(fullpath)
                
                fullPath --> full path plus the filename

                ______________________________________________________________________
            """,
                     
            "write_tif":"""write_tif:      
                write data to tif
                
                >>> write_tif(file_with_srid, full_output_name, data, 1, nodata=False)
                
                file_wite_srid   --> the original file with spatial infromations
                full_output_name --> path + filename + tile type e.g.: r'c:\\temp\\file1.tif'
                data             --> data you want to write to tif
                dtype            --> Output data type (int, float ...) 
                                     input number between 0 and 5:
                                        - 0 --> Int16
                                        - 1 --> Int32
                                        - 2 --> UInt16
                                        - 3 --> UInt32
                                        - 4 --> Float32
                                        - 5 --> Float64 
                                 --> default is Int32
                nodata           --> by default there will be no NoData Value asigned
                                       if True:
                                          it will put the max Value for Unsigned Integers
                                          it will put the min Value for signed Integers and floats
                                       if you put a Value --> this Value will be the NoData Value

                ______________________________________________________________________
            """}
            
    print myDic["header"]
    counter = 0
    inhalt.sort()
    op = []
    for ele in inhalt:
        for el in myDic.keys():
            if ele.lower() in el.lower():
                op.append(el)
                #print myDic[el]
                counter += 1

    if counter >0:
        op = sorted(list(set(op)))
        for ele in op:
            print myDic[ele]   
    elif counter == 0:
        print ">>> Couldnt find what you are looking for<<<"
        print ""      
        for ele in HelpInhalt:
            print myDic[ele]       




def read_tif(tif,band):
    inTif = zz_gdalnum.gdal.Open(tif, zz_gdalcon.GA_ReadOnly)
    band = inTif.GetRasterBand(band)
    data = zz_gdalnum.BandReadAsArray(band)
    return data
    

def read_tif_info(tif):
    inTif = zz_gdalnum.gdal.Open(tif, zz_gdalcon.GA_ReadOnly)
    driver = zz_gdalnum.gdal.GetDriverByName('GTiff')
    inCols = inTif.RasterXSize
    inRows = inTif.RasterYSize
    return inTif, driver, inCols, inRows
    
def write_tif(file_with_srid,full_output_name, data, dtype= 1, nodata=False ):
    dtypeL = [zz_gdalcon.GDT_Int16,
              zz_gdalcon.GDT_Int32,
              zz_gdalcon.GDT_UInt16,
              zz_gdalcon.GDT_UInt32,
              zz_gdalcon.GDT_Float32, 
              zz_gdalcon.GDT_Float64]
    '''writes data to a tiff and writes the srid infos ot it
        file_with_srid --> original file which has geoinformation
        full_output_name --> path + filename + .tiff
        data_to_write --> your new calculated data
        
        dtype --> define the output datatype default is Int32:
                imput number between 0 and 5:
                    - 0 --> Int16
                    - 1 --> Int32
                    - 2 --> UInt16
                    - 3 --> UInt32
                    - 4 --> Float32
                    - 5 --> Float64
        
        produces a new tiff
    '''
    try:
        inTiff, driver, inCols, inRows = read_tif_info(file_with_srid)
        dataOut = driver.Create(full_output_name,inCols,inRows,1, dtypeL[dtype])
        zz_gdalnum.CopyDatasetInfo(inTiff,dataOut)
        bandOut = dataOut.GetRasterBand(1)
        if nodata ==True or type(nodata)==int or type(nodata) == float:
            if type(nodata)==int or type(nodata) == float:
                nodataV = nodata
            elif dtype>3:#min Value from the floats
                nodataV = np.finfo(NoDataL[dtype]).min
            elif dtype<2: #min value from signed Integers
                nodataV = np.iinfo(NoDataL[dtype]).min
            else:
                nodataV = np.iinfo(NoDataL[dtype]).max
            bandOut.SetNoDataValue(nodataV)
        zz_gdalnum.BandWriteArray(bandOut,data)
        dataOut = None
        bandOut = None
    except:
        print "coundn't execute write_tiff"
        

    

    

    
