# -*- coding: utf-8 -*-


      #########################################################################
      ##                                                                     ##
      ##                                                                     ##
      ##         @     @             #######                                 ##
      ##         @@   @@             ##   ##                                 ##
      ##         @ @ @ @  @@@@ @@@@@ ##   ## ## ## @   @ @@@@@ @@@@@         ##
      ##         @  @  @     @ @     ####### ## ## @   @ @   @ @             ##
      ##         @     @ @@@@@ @     ##      ## ## @   @ @@@@@ @             ##
      ##         @     @ @   @ @     ##       ###   @ @  @     @             ##
      ##         @     @ @@@@@ @@@@@ ##       ##     @   @@@@@ @             ## 
      ##                                     ##                              ##
      ##                                    ##                               ##
      ##  _________________________________________________________________  ##
      ## THE SWISSKNIFE LIKE PYTHON-PACKAGE FOR WORK IN GENERAL AND WITH GIS ##
      ##  _________________________________________________________________  ##
      ##                                                                     ##
      #########################################################################

                          # T-S-L-P-P-F-W-I-G-A-W-G #

"""
Created on Fri Nov 20 12:17:03 2015

@author: Florian Wolf
@eMail : florian.wolf@idiv.de


"""
try:
	from __send_email import send_mail
except:
	pass
import info
import raster
import postgres
import vector



def README():
    myDic = {"header": """


      #########################################################################
      ##                                                                     ##
      ##                                                                     ##
      ##         @     @             #######                                 ##
      ##         @@   @@             ##   ##                                 ##
      ##         @ @ @ @  @@@@ @@@@@ ##   ## ## ## @   @ @@@@@ @@@@@         ##
      ##         @  @  @     @ @     ####### ## ## @   @ @   @ @             ##
      ##         @     @ @@@@@ @     ##      ## ## @   @ @@@@@ @             ##
      ##         @     @ @   @ @     ##       ###   @ @  @     @             ##
      ##         @     @ @@@@@ @@@@@ ##       ##     @   @@@@@ @             ## 
      ##                                     ##                              ##
      ##                                    ##                               ##
      ##  _________________________________________________________________  ##
      ## THE SWISSKNIFE LIKE PYTHON-PACKAGE FOR WORK IN GENERAL AND WITH GIS ##
      ##  _________________________________________________________________  ##
      ##                                                                     ##
      #########################################################################



             Until now the Package provides the Subpackages:

                   --> info

                   --> raster work (common Filetypes and hdf5)

                   --> PostgreSQL
                   
                   --> vector (work with shape files)


      ######################################################################### 
      #########################################################################

      """}

    print myDic["header"]
    
def outname(path, new_name_part = False , extension = False):
    '''this function is to rename / create output name for files
        the new_name_part will be added to the orig filename, 
        the extension is the new, if wanted
        if not, its the same like the input
        new_name_part or extension has to be given'''
        
    no_change = path[:path.rfind('.')] #split on last point in string
    if new_name_part == False and extension == False: #checjk if new_name_part and extension are give
        print 'error in naming, input is the same as output'
        return False
    if extension == False: #if no extension is given, take the on from the input file
        extension = path[path.rfind('.'):]
    if extension.startswith('.'): #remove . from the extension if given
        extension = extension[1:]
    if new_name_part == False: #if new_name_part is not given assign empty string to the variable
        new_name_part = ''
    if new_name_part.startswith('_'): #if given check if it starts with _ if yes, remove it
        new_name_part = new_name_part[1:]
    outname = no_change+'_'+new_name_part+'.'+extension #put all things together
    if path == outname: #check if new outname is equal to input
        print 'error in naming, input is the same as output'
        return False
    return outname #return the new name
