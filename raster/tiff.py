# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:12:36 2016

@author: Florian Wolf


            __________________________________________________
            ###              MacPyver.raster.tiff          ###
            ###   The Swissknife like Python-Package for   ###
            ###        work in general and with GIS        ###
            __________________________________________________

"""

import sys
import numpy as np

from osgeo import gdal
import osgeo.gdalnumeric as zz_gdalnum
import osgeo.gdalconst as zz_gdalcon


def read_tif(tif,band=1,nodata=0):
    '''
        reads in a tif, and returns a numpy array;

        to read a tif into python

        >>> data = read_tif(fullPath, bandNr)

        fullPath --> full path plus the filename
        bandNr   --> the number of the band you want to read

        if band is set to a certain value it will read just this band;
    default is to read the first band; to read in all bands set band to zero; 
    band can also be a list e.g.: [1,4,5] will be readin in the same order as passed
    (if band is a list start counting by 1);
    creates a 2d or 3d stack;

    shape is (rows, columns for 2d) (band, rows, columns for 3d) 

    '''
    def read_data(inTif, band_nr, nodata=0):
        band = inTif.GetRasterBand(band_nr)
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

    try:
        #default band is 1 and default for return nodata value is False ~ 0 ;1 ~ True
        inTif = zz_gdalnum.gdal.Open(tif, zz_gdalcon.GA_ReadOnly)
        if band == 0:
            #get number of available bands and create list from it with range
            if inTif.RasterCount != 1:
                nr_of_bands = range(1,inTif.RasterCount+1)
            else:
                nr_of_bands = 1
        elif type(band)== int:
            nr_of_bands = 1
        elif type(band)==list:
            nr_of_bands = band
            #test if max passed value is in the range of possible bands
            if np.array(nr_of_bands).max() > inTif.RasterCount:
                raise ValueError('max Value in the list is higher then the max possible nr of Bands in the raster\n --> max Value is: {0}'.format(inTif.RasterCount))
                sys.exit(1)

        #read in band(s)
        if type(inTif)!='NoneType':
            if nr_of_bands == 1:
                return read_data(inTif, band, nodata)
            elif type(nr_of_bands) == list and len(nr_of_bands) > 1:
                for b in nr_of_bands:
                #initialize and create the stack
                    if b == 1 :
                        stack = read_data(inTif, b)
                        stack = stack.reshape(1, stack.shape[0], stack.shape[1])
                    else:
                        #read in all other bands
                        stack = np.vstack((stack, read_data(inTif, b).reshape((1, stack.shape[1], stack.shape[2]))))
                return stack
            elif type(nr_of_bands) == list and len(nr_of_bands) <=1:
                raise ValueError('error in passed band option\nband is not a list longer then 1\nto read in one band use: band = 1 (or any other possible band nr)')
            else:
                raise NameError('input is not a file or file is broken')
    except:
        print "Error:", sys.exc_info()[:2]
        inTif = None
        raise

def set_nodata(tif,band,nodata):
    '''
    updates a tif and assigns the nodata value

        set_nodata(fullPath,band,nodata)

        >>> set_nodata(fullPath,1,-9999)

        fullPath --> full path plus the filename
        band     --> band to work with
        nodata   --> nodata value

    '''
    #update a raster --> burn nodata value to raster
    inTif = zz_gdalnum.gdal.Open(tif, zz_gdalcon.GA_Update)
    band = inTif.GetRasterBand(band)
    band.SetNoDataValue(nodata)
    band=None
    inTif = None

def read_tif_info(tif):
    '''
        read infos from tif

        >>> inTif, driver, inCols, inRows = read_tif_info(fullpath)

        fullPath --> full path plus the filename

    reads the infos ot the tif
    returns the filepointer, driver, nr of columns and rows
    used by write tif function, 
    but can be used stand alone
    '''

    # to get the infos from the raster \
    # returns the raster object, the driver, nr of cloumns and rows
    inTif = zz_gdalnum.gdal.Open(tif, zz_gdalcon.GA_ReadOnly)
    driver = zz_gdalnum.gdal.GetDriverByName('GTiff')
    inCols = inTif.RasterXSize
    inRows = inTif.RasterYSize
    return inTif, driver, inCols, inRows


def write_tif(file_with_srid,full_output_name, data, dtype= 1, nodata=False, option=False ):
    '''
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


        if data is a 3d array it will write all bands to the tif (in single bands)
    '''
    dtypeL = [zz_gdalcon.GDT_Int16,
              zz_gdalcon.GDT_Int32,
              zz_gdalcon.GDT_UInt16,
              zz_gdalcon.GDT_UInt32,
              zz_gdalcon.GDT_Float32,
              zz_gdalcon.GDT_Float64,
              zz_gdalcon.GDT_Byte]
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
            if nodata == 0 or nodata:
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
        
def add_band(src_file, src_add, option="COMPRESS=DEFLATE"):
    """ 
        adding a band/bands to an existing file
        just working if the files have the same extent, resolution and nr of pixel
        
        add_band(src_file, file_to_add) (bands will be added to src_file)
    """
    #pointer/open to files
    src_ds = gdal.OpenShared(src_file)    
    add_ds = gdal.OpenShared(src_add)

    #check extent and resolution and ...
    src_ext = get_extent(src_file)    
    add_ext = get_extent(src_add)
    if src_ext.ret_extent() != add_ext.ret_extent():
        print("Error in extent, the files are not equal in extent/resolution/pixel\nnot able to perform the function")
        print("src_file:", src_ext.ret_extent())
        print("src_add:", add_ext.ret_extent())
    else:
        #get band counts for the rasters
        src_bands_count = src_ds.RasterCount
        add_bands_count = add_ds.RasterCount
        #create copy of orig in RAM
        tmp_ds = gdal.GetDriverByName('MEM').CreateCopy('', src_ds, 0)
        #add all bands
        del src_ds
        for bands2add in range(1,add_bands_count+1):
            add_b = add_ds.GetRasterBand(bands2add).ReadAsArray()
            tmp_ds.AddBand()
            tmp_ds.GetRasterBand(src_bands_count+bands2add).WriteArray(add_b)
        #write / overwrite file to disk
        gdal.GetDriverByName('GTiff').CreateCopy(src_file, tmp_ds, 0, options=[option]) #CreateCopy(output_path, data2write)
        del tmp_ds, add_b, add_ds


####################################################################################

#create class to store the extent
#is used by the function get_extent
class extent():
    def __init__(self, coordinates = False, quite = False):
        if coordinates:
            if len(coordinates)==6:
                for x in coordinates:
                    if isinstance(x, (float, int)) == False:
                        print "Error in given coordinates, at least one given value is not a number"
                        print "all values set to zero"
                        coordinates = [0,0,0,0,0,0]
                self.left, self.top, self.columns, self.rows, self.px_size, self.py_size = coordinates
        else:
            self.left=0
            self.top=0
            self.columns=0
            self.rows = 0
            self.px_size = 0
            self.py_size = 0
            if quite == False:
                print "WARNING: all extent values are set to zero"

    #retun list with extent infos
    def ret_extent(self):
        if hasattr(self, 'right') and hasattr(self, 'bottom'):
            return (self.left, self.top, self.right, self.bottom, self.columns, self.rows, self.px_size, self.py_size)
        return (self.left, self.top, self.columns, self.rows, self.px_size, self.py_size)

    #calc missing corners
    def calc_corners(self):
        self.right = self.left + self.columns * self.px_size
        self.bottom = self.top - abs(self.rows * self.py_size)
        print 'right: {0} and bottom: {1} are stored in the object'.format(self.right, self.bottom)

#returns an object with the extent of the passed image path
def get_extent(data_path):
    '''
                creates an object with the extent infomation of the passed raster

                >>> ext = get_extent(file_path)

                file_path       --> full path to the file
                inside are the following parametes:
                    left, top, columns, rows, px_size
    '''

    #path to be read in
    intif, driver, columns, rows = read_tif_info(data_path)
    #get info from raster
    left, px_x_size, tilt_x, top, tilt_y, px_y_size = intif.GetGeoTransform()
    intif, driver = [None]*2 #delete intif and driver
    if abs(px_x_size) != abs(px_y_size):
        print 'WARNING: x-pixel-size is not equal to y-pixel-size'
        data_extent = extent((left, top, columns, rows, px_x_size, px_y_size))
        return data_extent
    else:
        data_extent = extent((left, top, columns, rows, px_x_size, px_y_size))
        return data_extent


#generates a raster with the same extent like the passed dst_extent raster
#to be able to calc with both in a numpy array
#the input-rasters need to have the same resolution (pixelsize) - (but its checking for that)
def raster2extent(data_path, dst_extent, nodata = False, return_orig_x0_y0_value = False):
    '''
                slice raster to the same extent

                >>> data = raster2extent(data_path, dst_extent, nodata = False)

                data_path       --> full path to file which should be sliced
                dst_data        --> full path to file which works as the template
                nodata          --> can be specified to set nodata value in the sliced output
                                    default is np.nan (to check for np.nan you hav to use
                                    np.isnan(...)
    '''
    #get extentdata from source / data_path or from extent class
    src_extent = get_extent(data_path)
    dst_extent = get_extent(dst_extent)

    if src_extent.ret_extent() == dst_extent.ret_extent():
        data = read_tif(data_path)
        data = np.where(data==data[0,0], np.nan, data)
        print "red data"
        return data

    elif dst_extent.px_size == src_extent.px_size:
        data = read_tif(data_path)
        orig_x0_y0 = data[0,0]
        #calc x offset (left)
        x_offset = (src_extent.left-dst_extent.left)*src_extent.px_size
        #calc y offset (top)
        y_offset = (dst_extent.top-src_extent.top)*src_extent.px_size

        #create empyt out raster
        newdata = np.zeros((dst_extent.rows, dst_extent.columns))
        #assign nodata value
        if nodata:
            noData = nodata
        else:
            noData = np.nan

        #fill empty raster with noData value
        newdata = np.where(newdata ==0 , noData, noData)

        #get the mx dimensions of the raster and borders to slice
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
        if x_slice > dst_extent.columns:
            x_slice = dst_extent.columns
        newdata[ y_offset:y_max, x_offset:x_max] = data[ : y_slice, : x_slice]
        newdata = np.where(newdata==orig_x0_y0, np.nan, newdata)

        #return data in the same dimensions like the inputed dst_extent raster
        print "slicesd data"
        if return_orig_x0_y0_value:
            return newdata, orig_x0_y0
        else:
            return newdata
    else:
        print "ERROR: pixel-size dosent match / you need to resample one of the files; src: {0} != dst: {1}".format(src_extent.px_size, dst_extent.px_size)
        return None
