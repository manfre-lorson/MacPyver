# -*- coding: utf-8 -*-


      #########################################################################
      ##                                                                     ##
      ##                                                                     ##
      ##         #     #             #######                                 ##
      ##         ##   ##             #     #                                 ##
      ##         # # # #  #### ##### #     # #   # #   # ##### #####         ##
      ##         #  #  #     # #     ####### #   # #   # #   # #             ##
      ##         #     # ##### #     #       #   # #   # ##### #             ##
      ##         #     # #   # #     #        # #   # #  #     #             ##
      ##         #     # ##### ##### #         #     #   ##### #             ##
      ##                                      #                              ##
      ##                                     #                               ##
      ##                                    #                                ##
      ##  _________________________________________________________________  ##
      ## THE SWISKNIVE LIKE PYTHON-PACKAGE FOR WORK IN GENERAL AND WITH GIS  ##
      ##  _________________________________________________________________  ##
      ##                                                                     ##
      #########################################################################

                          # T-S-L-P-P-F-W-I-G-A-W-G #

"""
Created on Fri Nov 20 12:17:03 2015

@author: Florian Wolf
@eMail : florian.wolf@idiv.de


"""

from __send_email import send_mail
import info
import raster
import postgres





def README():
    myDic = {"header": """  
      
      
      #########################################################################
      ##                                                                     ##
      ##                                                                     ##
      ##         #     #             #######                                 ##
      ##         ##   ##             #     #                                 ##
      ##         # # # #  #### ##### #     # #   # #   # ##### #####         ##
      ##         #  #  #     # #     ####### #   # #   # #   # #             ##
      ##         #     # ##### #     #       #   # #   # ##### #             ##
      ##         #     # #   # #     #        # #   # #  #     #             ##
      ##         #     # ##### ##### #         #     #   ##### #             ##
      ##                                      #                              ##
      ##                                     #                               ##
      ##                                    #                                ##
      ##  _________________________________________________________________  ##
      ## THE SWISKNIVE LIKE PYTHON-PACKAGE FOR WORK IN GENERAL AND WITH GIS  ##
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
