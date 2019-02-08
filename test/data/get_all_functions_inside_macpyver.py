# -*- coding: utf-8 -*-
"""
Created on Thu Feb 07 16:42:00 2019

@author: fw56moba
"""

import MacPyver

import inspect as ins

#list all files in the package:

all_files = MacPyver.info.info.glob_rec(MacPyver.__path__[0])

#filter entries:
all_files = [x for x in all_files if '.git' not in x and '.pyc' not in x]

all_files = [x.split('\\MacPyver\\')[-1] for x in all_files]

all_files = list(set([x.split('\\')[0] for x in all_files]))

print all_files

sub_mod = {'info':MacPyver.info.info,
           'tif' : MacPyver.raster.tiff,
           'hdf' : MacPyver.raster.hdf5,
           'postgres' : MacPyver.postgres.pg,
           'vector' : MacPyver.vector}


fl = [x for x in ins.getmembers(MacPyver, ins.isfunction)]

for f in sub_mod:
    fl.extend( [x for x in ins.getmembers(sub_mod[f], ins.isfunction)])

def_dic = {}

for entry in fl:
    def_dic[entry[0]] = entry[1].__module__

d = def_dic
for w in sorted(d, key=d.get, reverse=False):
  print w,':', d[w]

'''
outname : MacPyver
README : MacPyver
hostname : MacPyver.info.info
glob_rec : MacPyver.info.info
timestr : MacPyver.info.info
UNSIGNED : MacPyver.info.info
folderCount : MacPyver.info.info
getsizeMB : MacPyver.info.info
pathdepth : MacPyver.info.info
cksum : MacPyver.info.info
time : MacPyver.info.info
create_pg_Table_load_to_pg : MacPyver.postgres.pg
create_pg_Table_sql_command : MacPyver.postgres.pg
create_pg_Table : MacPyver.postgres.pg
read_hdf_subset : MacPyver.raster.hdf5
subnames : MacPyver.raster.hdf5
write_hdf_subset : MacPyver.raster.hdf5
get_sub_dataset_names : MacPyver.raster.hdf5
read_hdf : MacPyver.raster.hdf5
write_hdf : MacPyver.raster.hdf5
add_band : MacPyver.raster.tiff
get_extent : MacPyver.raster.tiff
read_tif : MacPyver.raster.tiff
set_nodata : MacPyver.raster.tiff
write_tif : MacPyver.raster.tiff
read_tif_info : MacPyver.raster.tiff
mptype : MacPyver.raster.tiff
raster2extent : MacPyver.raster.tiff
read_df : MacPyver.vector
save_df : MacPyver.vector
glob : glob
create_engine : sqlalchemy.engine
'''


