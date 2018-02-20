# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:12:36 2016

@author: Floiran Wolf
"""

import sys
import numpy as np
import os

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
            """,

            "get_extent":"""get_extent:
                creates an object with the extent infomation of the passed raster

                >>> ext = get_extent(file_path)

                file_path       --> full path to the file
                inside are the following parametes:
                    left, top, columns, rows, px_size
                ______________________________________________________________________
            """,

            "raser2extent":"""raster2extent:
                slice raster to the same extent

                >>> data = raster2extent(data_path, dst_extent, nodata = False)

                data_path       --> full path to file which should be sliced
                dst_data        --> full path to file which works as the template
                nodata          --> can be specified to set nodata value in the sliced output
                                    default is np.nan (to check for np.nan you hav to use
                                    np.isnan(...)
                ______________________________________________________________________
            """
               }

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
    '''read tif into numpy array'''
    
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
    ''' set nodata value to the existing raster'''
    
    #update a raster --> burn nodata value to raster
    inTif = zz_gdalnum.gdal.Open(tif, zz_gdalcon.GA_Update)
    band = inTif.GetRasterBand(band)
    band.SetNoDataValue(nodata)
    band=None
    inTif = None
    

def mptype(obj):
    '''returns my object type'''
    try:
        return str(obj.__class__).split('.')[1]
    except:
        return str(type(obj)).split(" '")[1].split("'")[0]

def read_tif_info(tif):
    ''' to get the infos from the raster \
    returns the raster object, the driver, nr of cloumns and rows'''
    
    inTif = zz_gdalnum.gdal.Open(tif, zz_gdalcon.GA_ReadOnly)
    driver = zz_gdalnum.gdal.GetDriverByName('GTiff')
    inCols = inTif.RasterXSize
    inRows = inTif.RasterYSize
    return inTif, driver, inCols, inRows


def write_tif(file_with_srid,full_output_name, data, dtype= 1, nodata=False, option=False ): 
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

#create class to store the extent
#is used by the function get_extent
class extent():
    '''create class to store the extent
    is used by the function get_exten'''
    
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
        ''' returns the extent as a list'''
        
        if hasattr(self, 'right') and hasattr(self, 'bottom'):
            return (self.left, self.top, self.right, self.bottom, self.columns, self.rows, self.px_size, self.py_size)
        return (self.left, self.top, self.columns, self.rows, self.px_size, self.py_size)

    #calc missing corners
    def calc_corners(self):
        '''calc the missing extent corners'''
        
        self.right = self.left + self.columns * self.px_size
        self.bottom = self.top - abs(self.rows * self.py_size)
        print 'right: {0} and bottom: {1} are stored in the object'.format(self.right, self.bottom)

#returns an object with the extent of the passed image path
def get_extent(data_path):
    '''get the coordinates of the extent'''
    #path to be read in
    intif, driver, columns, rows = read_tif_info(data_path)
    #get info from raster
    left, px_x_size, tilt_x, top, tilt_y, px_y_size = intif.GetGeoTransform()
    intif, driver = [None]*2
    if abs(px_x_size) != abs(px_y_size):
        print 'WARNING: x-pixel-size is not equal to y-pixel-size'
        data_extent = extent((left, top, columns, rows, px_x_size, px_y_size))
        return data_extent
    else:
        data_extent = extent((left, top, columns, rows, px_x_size, px_y_size))
        return data_extent



def raster2extent(data_path, dst_extent, nodata = False):
    '''generates a raster with the same extent like the passed dst_extent raster
    to be able to calc with both in a numpy array
    the input-rasters need to have the same resolution (pixelsize) - (but its checking for that)'''
    
    #get extentdata from source / data_path or from extent class
    src_extent = get_extent(data_path)
    dst_extent = get_extent(dst_extent)

    if dst_extent.px_size == src_extent.px_size:
        data = read_tif(data_path)
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
        newdata[ y_offset:y_max, x_offset:x_max] = data[ : y_slice, : x_slice]
        #return data in the same dimensions like the inputed dst_extent raster
        return newdata
    else:
        print "ERROR: pixel-size dosent match / you need to resample one of the files; src: {0} != dst: {1}".format(src_extent.px_size, dst_extent.px_size)
        return None


class geoobj():
    '''  
         __________________________________________________
         ###            MacPyver.raster.tiff            ###
         ###   The Swissknife like Python-Package for   ###
         ###        work in general and with GIS        ###
         __________________________________________________


    geoobj is a "geo-tif" with all geoinformations and the data
    by generating the object it will read the infos,
    functions can read and write the data

    to inizialice the object do:

    go = geoobj(fullpath2tif) --> metadata is read
    
    
    functions:
        
        read_data   --> read in the raster vaules as an numpy array
        create_data2 --> create a second data frame in the object
        update_data --> update the red data
        write_tif   --> write data to file 
    '''

    def __init__(self, inpath):
        try:
            "create go with all values"
            self.intif   = zz_gdalnum.gdal.Open(inpath, zz_gdalcon.GA_ReadOnly)
            self.driver  = zz_gdalnum.gdal.GetDriverByName('GTiff')
            self.columns = self.intif.RasterXSize
            self.rows    = self.intif.RasterYSize
            geotransform = self.intif.GetGeoTransform()
            self.px_size = geotransform[1]
            self.py_size = geotransform[5]
            self.xmin = geotransform[0]
            self.ymax = geotransform[3]
            self.xmax = self.xmin + self.columns * self.px_size
            self.ymin = self.ymax + abs(self.rows * self.py_size)
            self.extent = [self.xmin, self.ymin, self.xmax, self.ymax, self.px_size, self.py_size]
            self.name = inpath.split(os.sep)[-1]
            self.path = (os.sep).join(inpath.split(os.sep)[:-1])
            #get nodata value from raster
            nodata = self.intif.GetRasterBand(1).GetNoDataValue()
            if nodata:
                self.nodata = nodata
            else:
                self.nodata = None
        except:
            #print 'ERROR: file is not a valid raster'
            raise NameError('ERROR: file is not a valid raster')


    def read_data(self, band_nr = 1):
        ''' creates the method data where the matrix of the raster is stored'''
        band = self.intif.GetRasterBand(band_nr)
        self.data = zz_gdalnum.BandReadAsArray(band)
        
        
    def write_tif(self, outname, data2write= False, dtype = 1, nodata = False, option = 'COMPRESS=DEFLATE'):
        '''dtype: ....
        
            if nodata set to True the orig nodata value will be assigned to the raster,
            if it is not a double ( in this case no nodata will be assigned)
            
            write_tif(outname, data2write=False, dtype=1, nodata=False, option='Compress=Deflate')
            
            dtypes:
                0 --> Int16
                1 --> Int32
                2 --> UIit16
                3 --> UInt32
                4 --> Float32
                5 --> Float64
                6 --> UInt8
                
        '''
        dtypeL = [zz_gdalcon.GDT_Int16, zz_gdalcon.GDT_Int32,
                  zz_gdalcon.GDT_UInt16, zz_gdalcon.GDT_UInt32,
                  zz_gdalcon.GDT_Float32, zz_gdalcon.GDT_Float64,
                  zz_gdalcon.GDT_Byte]
        try:
            if type(data2write) != type(self.data):
                data2write = self.data                
                  
            if len(data2write.shape)==3:
                nr_of_bands = data2write.shape[0]
            elif len(data2write.shape)==2:
                nr_of_bands = 1
            else:
                raise NameError('ERROR: in Number of Bands')

            if not 'int' in str(np.result_type(data2write)):
                dataOut = self.driver.Create(outname, self.columns, self.rows, nr_of_bands, dtypeL[dtype])
            else:
                dataOut = self.driver.Create(outname, self.columns, self.rows, nr_of_bands, dtypeL[dtype], options=[option])

            #dataOut.SetGeoTransform(self.intif.GetGeoTransform())
            zz_gdalnum.CopyDatasetInfo(self.intif, dataOut)

            for band in range(nr_of_bands):
                bandOut = dataOut.GetRasterBand(band+1)
                
                if nodata:
                    #test if nodate can be set
                    if isinstance(nodata, bool) and 'e' not in str(self.nodata):
                        nodata = self.nodata
                    if 'e' in str(nodata):
                        nodata = False
                    if nodata:
                        bandOut.SetNoDataValue(nodata)
                        
                if nr_of_bands==1:
                    zz_gdalnum.BandWriteArray(bandOut,data2write)
                else:
                    zz_gdalnum.BandWriteArray(bandOut,data2write[band,:,:])
                bandOut = None
            dataOut = None
            #print 0
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except ValueError:
            print ("Could not write the nodata value")
        except:
            print "Unexpected error:", sys.exc_info()
        

    def updata_data(self, newdata):
        '''
        updata the orig data with new data
        is checking if the shape of the data stays the same 
        
        is equal to go.data = newdata
        
        go.update_data(newdata)
        newdata is stored in go.data
        '''
        if self.data.shape == newdata.shape:            
            self.data = newdata
        else:
            print "ERROR: abord updating: updated Data has a differnet shape"
            print "       original shape: {0}".format(self.data.shape)
            print "       updated shape:  {0}".format(newdata.shape)
            
        
    def create_data2(self, indata):
        '''creates a second data frame
        but no change in the metadata'''
        
        self.data2 = indata
        if self.data2.shape != self.data.shape:
            print "WARNING: data2 has a different shape then data"
            print "data: {0} != data2: {1}".format(self.data.shape, self.data2.shape)
            
    
    def extrem_values(self, band_nr = 1):
        '''gets the extrem values of a raster
            will read the data if it is not done befor
            is list of 2 lowest and  2 highest values in the tif'''
            
        if not hasattr(self, 'data'):
            self.read_data(band_nr)
        unique = np.unique(self.data)
        if self.nodata:
            unique = np.delete(unique, self.nodata)
            self.min_max_value = [unique[0], unique[-1]]
        elif len(unique)<4:
            self.min_max_value = unique
        else:
            self.min_max_value = [unique[0], unique[1], '...', unique[-2], unique[-1]]

