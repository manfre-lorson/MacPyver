# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 13:42:22 2016

@author: fw56moba

"""

import h5py



def Help(inhal = ''):
    HelpInhalt =  sorted(['get_sub_dataset_names', 'subnames', 'read_hdf', 'read_hdf_subset','write_hdf','write_hdf_subset'])
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
            ###            MacPyver.raster.hdf5            ###
            ###   The Swissknife like Python-Package for   ###
            ###        work in general and with GIS        ###
            __________________________________________________
                
                How to use the functions:
                __________
                
             """,
             
            "get_sub_dataset_names":""" get_sub_dataset_names: 
                returns the list of all subdatasets in the hdf
                
                >>> names = get_sub_dataset_names(full_path)
                
                full_path --> path + filename
                
 _______________________________________________________________________________
            """,
            
            "subnames":""" subnames:  
                this def is used by get_sub_dataset_names
                
                > don't use it <
                
 _______________________________________________________________________________
            """,
                     
            "read_hdf":""" read_hdf:      
                returns the data from a single band from the hdf as numpy.array
                
                >>>data = read_hdf(full_path,'subdataset_name')
                
                full_path      --> path + filename
                subdatasetname --> substring from the dataset name
                
                if there is no subdataset like your subdatasetname it will return 
                a list of available subdatasets

 _______________________________________________________________________________
            """,
            "read_hdf_subset" :""" read_hdf_subset:
                returns the a subdataset of the data from selected the subdataselayer
                
                >>>read_hdf_subset(full_path,sds_name,start_row,end_row,start_line,end_line)
                
                full_path  --> path + file
                sds_name   --> substring from the dataset name
                start_row  --> start ot the to read row
                end_row    --> end of the to read row
                start_line --> start of the lines to read
                end_line   --> end of the lines to read
                
                --> python starts counting with a zero                
            
 _______________________________________________________________________________
            """,
            
            "write_hdf":""" write_hdf:  
                write data to an hdf file
                
                >>>write_hdf(full_path, data, write_type = 'a', dtype = 6)
                
                full_path  --> path + file
                data       --> data to write to the file
                write_type --> option on how to write
                            'r+' --> read an write, file must exist
                            'w'  --> create file, truncate if exists
                            'w-' or 'x' --> create file, fail if exists
                            'a'  --> read/write if exists, create otherwise
                            --> default is set to 'a'
                dtypes    --> output datatype:
                    0 = h5py.h5t.IEEE_F32LE,
                    1 = h5py.h5t.IEEE_F32BE,
                    2 = h5py.h5t.IEEE_F64LE,
                    3 = h5py.h5t.IEEE_F64BE,
                    4 = h5py.h5t.STD_I8LE,
                    5 = h5py.h5t.STD_I16LE,
                    6 = h5py.h5t.STD_I32LE,
                    7 = h5py.h5t.STD_I64LE,
                    8 = h5py.h5t.STD_I8BE,
                    9 = h5py.h5t.STD_I16BE,
                   10 = h5py.h5t.STD_I32BE,
                   11 = h5py.h5t.STD_I64BE,
                   12 = h5py.h5t.STD_U8LE,
                   13 = h5py.h5t.STD_U16LE,
                   14 = h5py.h5t.STD_U32LE,
                   15 = h5py.h5t.STD_U64LE,
                   16 = h5py.h5t.STD_U8BE,
                   17 = h5py.h5t.STD_U16BE,
                   18 = h5py.h5t.STD_U32BE,
                   19 = h5py.h5t.STD_U64BE,
                   20 = h5py.h5t.NATIVE_INT8,
                   21 = h5py.h5t.NATIVE_UINT8,
                   22 = h5py.h5t.NATIVE_INT16,
                   23 = h5py.h5t.NATIVE_UINT16,
                   24 = h5py.h5t.NATIVE_INT32,
                   25 = h5py.h5t.NATIVE_UINT32,
                   26 = h5py.h5t.NATIVE_INT64,
                   27 = h5py.h5t.NATIVE_UINT64,
                   28 = h5py.h5t.NATIVE_FLOAT,
                   29 = h5py.h5t.NATIVE_DOUBLE
                --> default is set to Integer 32
                
                
 _______________________________________________________________________________
            """,
            
            "write_hdf_subset":""" write_hdf_subset:  
                writes a subset of data to the hdf file
                
                >>> write_hdf_subset(full_path, subdatasetname, data, 
                                     start_row = None, end_row = None, 
                                     start_line = None, end_line = None )
                
                full_path       --> path + file
                subdatasetnames --> name or substring of the subdataset
                data            --> data to write to the file
                start_row       --> start row to write 
                end_row         --> end row to write
                start_line      --> start line to wirte
                end_line        --> end line to write
                --> default of start and ends is None > means hdf[:,:] is usesd
                
                
                
 _______________________________________________________________________________
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
        print "     >>> Error: no function with %r <<<" % inhal
        print "" 
        print "     all available function: " 
        for ele in HelpInhalt:
            print myDic[ele]       
    
'''________________________________END-DIC______________________________________'''


def subnames(name):
    # def to append the names of the subdatasets to the meta list
    # function for get_sub_dataset_names --> to be able to run the hdf.visit() function
    #meta is the global variable created by get_sub_dataset_names
    meta.append(name)


    
def get_sub_dataset_names(hdf,sds_name):
    #returns a list --> meta with the names of all subdatasets in the hdf
    global meta
    meta = []#empty meta list
    name_match=[]
    m = h5py.File(hdf,'r') #open path to file
    #get the names of the subdatasets
    m.visit(subnames) # calls the function subnames
    for sds in meta: # loop thru all subdatasets to lock for the given substring in the subdatasetnames
        if sds_name.lower() in sds.lower(): # all letters in lower
            name_match.append(sds)
    if len(name_match)==1:
        return name_match[0]    
    elif len(name_match)==0: # if there is no substring subdatasetname match it prints all subdatasetnames
        print 'no sub_dataset with this name'
        print 'available sub_datasets are: '
        for sds in meta: #
            print "    " + sds  
        return False
    elif len(name_match)>1:
        print 'there are more than one subdataset with the name'
        for name in name_match:
            print name
        return False
    else:
        print 'unspecific error'
        return False
    
def read_hdf(full_path,sds_name):
    #returns the data from a subdataset as a numpy array
    sds = get_sub_dataset_names(full_path,sds_name) # creates a list of all subdatasets
    if sds != False:
        hdf = h5py.File(full_path,'r') # creates the hdf.object
        data = hdf[sds][:] # reads the  data from the selected subdataset
        hdf.close() # close the hdf file
        return data 
        
def read_hdf_subset(full_path,sds_name,start_row,end_row,start_line,end_line):
    sds = get_sub_dataset_names(full_path,sds_name) # creates string from the subdataset name
    if sds != False: # if sds is not a string, than its false
        hdf = h5py.File(full_path,'r') # creates the hdf.object
        data = hdf[sds][start_row:end_row, start_line:end_line] 
        hdf.close()
        return data

def write_hdf(full_path,subdatasetname,  data, write_type = 'a', dtype = 6, ):
    #available number types in hdf
    dtypes = [h5py.h5t.IEEE_F32LE,h5py.h5t.IEEE_F32BE,
              h5py.h5t.IEEE_F64LE,h5py.h5t.IEEE_F64BE,
              h5py.h5t.STD_I8LE,h5py.h5t.STD_I16LE,
              h5py.h5t.STD_I32LE,h5py.h5t.STD_I64LE,
              h5py.h5t.STD_I8BE,h5py.h5t.STD_I16BE,
              h5py.h5t.STD_I32BE,h5py.h5t.STD_I64BE,
              h5py.h5t.STD_U8LE,h5py.h5t.STD_U16LE,
              h5py.h5t.STD_U32LE,h5py.h5t.STD_U64LE,
              h5py.h5t.STD_U8BE,h5py.h5t.STD_U16BE,
              h5py.h5t.STD_U32BE,h5py.h5t.STD_U64BE,
              h5py.h5t.NATIVE_INT8,h5py.h5t.NATIVE_UINT8,
              h5py.h5t.NATIVE_INT16,h5py.h5t.NATIVE_UINT16,
              h5py.h5t.NATIVE_INT32,h5py.h5t.NATIVE_UINT32,
              h5py.h5t.NATIVE_INT64,h5py.h5t.NATIVE_UINT64,
              h5py.h5t.NATIVE_FLOAT,h5py.h5t.NATIVE_DOUBLE]
              
    new_hdf = h5py.File(full_path, write_type)
    dataset = new_hdf.create_dataset(subdatasetname,data.shape, dtypes[dtype])#, compression="gzip", compression_opts=9)
    dataset[...] = data
    #dataset[start_row:end_row, start_line:end_line] = data
    new_hdf.close()
    
    f = new_hdf.create_dataset(subdatasetname,data.shape,dtypes[dtype])
    dataset= f[subdatasetname]
    dataset[start_row:end_row, start_line:end_line] = data
    new_hdf.close()
    
    #dset = f.create_dataset("zipped", (100, 100), compression="gzip")

def write_hdf_subset(full_path, subdatasetname, data, start_row = None, end_row = None, start_line = None, end_line = None ):
    f = h5py.File(full_path, 'r+')
    sds = get_sub_dataset_names(full_path,subdatasetname)
    if sds != False:
        f[sds][start_row:end_row, start_line:end_line] = data
        f.close()
        
    
