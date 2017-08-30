# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:12:36 2016

@author: Floiran Wolf
"""

import osgeo.gdalnumeric as zz_gdalnum
import osgeo.gdalconst as zz_gdalcon



def Help(inhal = ''):
    HelpInhalt =  sorted(['set_nodata','read_tif', 'read_tif_info', 'write_tif'])
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

             """,
            "set_nodata":"""set_nodata(fullPath,band,nodata)

                >>> set_nodata(fullPath,1,-9999)

                fullPath --> full path plus the filename
                band     --> band to work with
                nodata   --> nodata value

    ______________________________________________________________________
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

                >>> write_tif(file_with_srid, full_output_name, data, 1, nodata=False, option=False)

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
                                        - 6 --> UInt8
                                 --> default is Int32
                nodata           --> by default there will be no NoData Value asigned
                                       if True:
                                          it will put the max Value for Unsigned Integers
                                          it will put the min Value for signed Integers and floats
                                       if you put a Value --> this Value will be the NoData Value
                option           --> "COMPRESS=DEFLATE"

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




def read_tif(tif,band,nodata=0):
    inTif = zz_gdalnum.gdal.Open(tif, zz_gdalcon.GA_ReadOnly)
    band = inTif.GetRasterBand(band)
    data = zz_gdalnum.BandReadAsArray(band)
    if nodata==0:
        return data
    elif nodata==1:
        noda = band.GetNoDataValue()
        return data, noda

def set_nodata(tif,band,nodata):
    inTif = zz_gdalnum.gdal.Open(tif, zz_gdalcon.GA_Update)
    band = inTif.GetRasterBand(band)
    band.SetNoDataValue(nodata)
    band=None

def read_tif_info(tif):
    inTif = zz_gdalnum.gdal.Open(tif, zz_gdalcon.GA_ReadOnly)
    driver = zz_gdalnum.gdal.GetDriverByName('GTiff')
    inCols = inTif.RasterXSize
    inRows = inTif.RasterYSize
    return inTif, driver, inCols, inRows

def write_tif(file_with_srid,full_output_name, data, dtype= 1, nodata=False, option=False ):
    dtypeL = [zz_gdalcon.GDT_Int16,
              zz_gdalcon.GDT_Int32,
              zz_gdalcon.GDT_UInt16,
              zz_gdalcon.GDT_UInt32,
              zz_gdalcon.GDT_Float32,
              zz_gdalcon.GDT_Float64,
              zz_gdalcon.GDT_Byte]
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
                    - 6 --> Byte
        produces a new tiff

        option = 'COMPRESS=DEFLATE'
    '''
    try:
        inTiff, driver, inCols, inRows = read_tif_info(file_with_srid)
        if option != False:
            dataOut = driver.Create(full_output_name,inCols,inRows,1, dtypeL[dtype],options=[option])
        else:
            dataOut = driver.Create(full_output_name,inCols,inRows,1, dtypeL[dtype])
        zz_gdalnum.CopyDatasetInfo(inTiff,dataOut)
        bandOut = dataOut.GetRasterBand(1)
        if nodata ==True or type(nodata)==int or type(nodata) == float:
            if type(nodata)==int or type(nodata) == float:
                nodataV = nodata
            elif dtype>3:#min Value from the floats
                nodataV = np.finfo(dtype).min
            elif dtype<2: #min value from signed Integers
                nodataV = np.iinfo(dtype).min
            else:
                nodataV = np.iinfo(dtype).max
            bandOut.SetNoDataValue(nodataV)
        zz_gdalnum.BandWriteArray(bandOut,data)
        dataOut = None
        bandOut = None
    except:
        print "coundn't execute write_tiff"


#dstImg = driver.Create(dstName, srcImg.RasterXSize, srcImg.RasterYSize, 1, gdal.GDT_Int32, options = [ 'COMPRESS=DEFLATE' ])

def write_tif_bands(file_with_srid,full_output_name, data, dtype= 1, nodata=False, option=False ):
    dtypeL = [zz_gdalcon.GDT_Int16, zz_gdalcon.GDT_Int32, zz_gdalcon.GDT_UInt16, zz_gdalcon.GDT_UInt32,
              zz_gdalcon.GDT_Float32, zz_gdalcon.GDT_Float64, zz_gdalcon.GDT_Byte]
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
                    - 6 --> Byte
        produces a new tiff

        option = 'COMPRESS=DEFLATE'
    '''
    try:
        inTiff, driver, inCols, inRows = read_tif_info(file_with_srid)
        if len(data.shape)==3:
            nr_of_bands = data.shape[0]
        elif len(data.shape)==2:
            nr_of_bands = 1
        else:
            print('error in Bands')
            sys.exit(1)
        #print(nr_of_bands)
        if option != False:
            dataOut = driver.Create(full_output_name,inCols,inRows,nr_of_bands, dtypeL[dtype],options=[option])
        else:
            dataOut = driver.Create(full_output_name,inCols,inRows,nr_of_bands, dtypeL[dtype])
        zz_gdalnum.CopyDatasetInfo(inTiff,dataOut)
        for band in range(nr_of_bands):
            bandOut = dataOut.GetRasterBand(band+1)
            if nodata:
                bandOut.SetNoDataValue(nodata)
            if nr_of_bands==1:
                zz_gdalnum.BandWriteArray(bandOut,data)
            else:
                zz_gdalnum.BandWriteArray(bandOut,data[band,:,:])
            bandOut = None
        dataOut = None
    except:
        print "coundn't execute write_tiff"
