# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:12:36 2016

@author: Floiran Wolf
"""

import sys
import numpy as np

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

###############################################################################
###############################################################################



###############################################################################
####                            Functions                                  ####
###############################################################################

def read_tif(tif,band=1,nodata=0):
    try:
        #default band is 1 and default for return nodata value is False ~ 0 ;1 ~ True
        inTif = zz_gdalnum.gdal.Open(tif, zz_gdalcon.GA_ReadOnly)
        if type(inTif)!='NoneType':
            band = inTif.GetRasterBand(band)
            data = zz_gdalnum.BandReadAsArray(band)
            inTif = None
            if type(data)==None.__class__:
                raise
            else:
                if nodata==0:
                    return data
                elif nodata==1:
                    noda = band.GetNoDataValue()
                    return data, noda
        else:
            raise NameError('input is not a file or file is broken')
    except:
        print "Error:", sys.exc_info()[:2]
        inTif = None
        raise

def set_nodata(tif,band,nodata):
    #update a raster --> burn nodata value to raster
    inTif = zz_gdalnum.gdal.Open(tif, zz_gdalcon.GA_Update)
    band = inTif.GetRasterBand(band)
    band.SetNoDataValue(nodata)
    band=None
    inTif = None

def read_tif_info(tif):
    # to get the infos from the raster \
    # returns the raster object, the driver, nr of cloumns and rows
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

        option = 'COMPRESS=DEFLATE' (gdal like options (-co "NAME=VALUE"))

        if the passed data has more the onw band all bands will be written to the output

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
        if option:
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
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except ValueError:
        print ("Could not write the nodata value")
    except:
        print "Unexpected error:", sys.exc_info()
        
        
####################################################################################
 

class extent():
    def __init__(self, coordinates = False, quite = False):
        if coordinates:
            if len(coordinates)==5:
                for x in coordinates:
                    if isinstance(x, (float, int)) == False:
                        print "Error in given coordinates, at least one given value is not a number" 
                        print "all values set to zero"
                self.left, self.top, self.columns, self.rows, self.px_size = coordinates
        else:
            self.left=0
            self.top=0
            self.columns=0
            self.rows = 0
            self.px_size = 0
            if quite == False:
                print "WARNING: all extent values are set to zero"
        
    def ret_extent(self):
        return (self.left, self.top, self.columns, self.rows, self.px_size)


        
def get_extent(data_path):
    #path to be read in
    intif, driver, columns, rows = read_tif_info(data_path)
    #get info from raster
    left, px_x_size, tilt_x, top, tilt_y, px_y_size = intif.GetGeoTransform()
    intif, driver = [None]*2
    if abs(px_x_size) != abs(px_y_size):
        print "x-pixel-size is not equal to y-pixel-size"
        return False
    else:
        data_extent = extent((left, top, columns, rows, px_x_size))
        return data_extent
        



def raster2extent(data_path, dst_extent, nodata = False):
    #get extentdata from source / data_path or from extent class
    src_extent = get_extent(data_path)
    dst_extent = get_extent(dst_extent)

    #check if dst_extent is the right format
    #if len(dst_extent)!=5:
    #    print "ERROR: given extent do's not match needed pattern {0}".format("extent = (left, top, columns, rows, px_size)")
    if dst_extent.px_size != src_extent.px_size:
        print "ERROR: pixel-size dosent match / you need to resample one of the files; src: {0} != dst: {1}".format(src_extent.px_size, dst_extent.px_size)
    
    data = read_tif(data_path)

    x_offset = (src_extent.left-dst_extent.left)*src_extent.px_size
    #right_x_mismatch = src_extent[2]*src_extent[-1] -  (left_x_mismatch+dst_extent[2]*dst_extent[-1]) 
    
    y_offset = (dst_extent.top-src_extent.top)*src_extent.px_size
    #bottom_mismatch = src_extent[1]*src_extent[3]*src_extent[-1]- (top_y_mismatch+dst_extent[2]*dst_extent[-1])
    
    
    #create empyt out raster 
    newdata = np.zeros((dst_extent.rows, dst_extent.columns))
    
    #assign nodata value
    if nodata:
        noData = nodata
    else:
        noData = np.nan
    
    #fill empty raster with noData value
    newdata = np.where(newdata ==0 , noData, noData)
    
    if x_offset < 0:
        data = data[:,abs(x_offset):abs(x_offset)+newdata.shape[1]]
        x_offset = 0
    
    if y_offset < 0:
        data = data[abs(y_offset):abs(y_offset)+newdata.shape[0],:]
        y_offset = 0
    

    if y_offset+data.shape[0]>newdata.shape[0]:
        y_max = newdata.shape[0]
    else:
        y_max = y_offset+data.shape[0]
    
    
    if x_offset+data.shape[1]>newdata.shape[1]:
        x_max = newdata.shape[1]
    else:
        x_max = x_offset+data.shape[1]
        
    if x_offset+data.shape[1]>data.shape[1]:
        x_slice = -(x_offset+data.shape[1]-x_max)
    else:
        x_slice = data.shape[1]

    if y_offset+data.shape[0]>y_max:
        y_slice = -(y_offset+data.shape[0]-y_max)
    else:
        y_slice = data.shape[0]

    
    #insert data to out dataset
    newdata[ y_offset:y_max, x_offset:x_max] = data[ : y_slice, : x_slice]
    return newdata
    
    
    
'''
import MacPyver as mp


data_big_path = r'D:\IPBES_work\biodiverity_models\test\SSP1xRCP2.6_cSAR_degree_2015-2050_CC_DC_0_per_mean_nr1.tif'

data_small_path = r'D:\IPBES_work\biodiverity_models\test\SSP1xRCP2.6_cSAR_degree_2015-2050_CC_DC_0_per_mean.tif'

data_big = mp.raster.tiff.read_tif(data_big_path)

data_small = mp.raster.tiff.read_tif(data_small_path)

new = mp.raster.tiff.raster2extent(data_big_path, data_small_path)

mp.raster.tiff.write_tif(data_small_path, data_small_path[:-4]+'_clip6.tif', new, 4)


data_path = data_big_path
dst_extent = data_small_path

src_extent.ret

'''
