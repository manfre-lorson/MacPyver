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

                   --> send eMails

                   --> raster work (common Filetypes and hdf5)

                   --> PostgreSQL


              To see the functions in the Subpackages navigate into
              the Subpackage and call the Help() function

              Inside the Help() you see the "HOW TO WORK" with the functions"




      ######################################################################### 
      #########################################################################

      """}

    print myDic["header"]
    
    def outname(path, new_name_part = False , extension = False):
    no_change = path[:path.rfind('.')]
    if new_name_part == False and extension == False:
        print 'error in naming, input is the same as output'
        return False
    if extension == False:
        extension = path[path.rfind('.'):]
    if extension.startswith('.'):
        extension = extension[1:]
    if new_name_part == False:
        new_name_part = ''
    if new_name_part.startswith('_'):
        new_name_part = new_name_part[1:]
    outname = no_change+'_'+new_name_part+'.'+extension
    if path == outname:
        print 'error in naming, input is the same as output'
        return False
    return outname
