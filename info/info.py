#-*- coding: utf-8 -*-

from datetime import datetime
import  socket
from glob import glob
import os



def Help(inhal = ''):
    HelpInhalt =  sorted(['timestr', 'time', 'hostname', 'folderCount','getsizeMB'])
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
            ###               MacPyver.info                ###
            ###   The Swissknife like Python-Package for   ###
            ###        work in general and with GIS        ###
            __________________________________________________
                
                How to use the functions:
                __________
                
             """,
             
            "timestr":""" timestr: 
                returns the time as a string
                
                >>> timestr()
                
 _______________________________________________________________________________
            """,
            
            "time":""" time:  
                returns the time to calculate 
                
                >>> time()
                
 _______________________________________________________________________________
            """,
                     
            "hostname":""" hostname:      
                returns the hostname where you are running the Python
                
                >>>hostname()

 _______________________________________________________________________________
            """,
            "folderCount" :""" folderCount
                returns the number of Folders in the directory

		>>>folderCount(fillpath, wildcard= "*",position = "m")
		
		fullpath --> path to the folder
		wildcard --> if not set, it will use '*' as default
		position --> to specify the wildcard 
			     by default m --> '*'
			     options:
			     	s --> startswith 'name*'
				e --> endswith '*name'
		if you just want to count tiffs:
		folderCount(path,'.tiff','e')
		--> returns the count of all tiffs in the folder

 _______________________________________________________________________________
            """,
            
            "getsizeMB":""" getsizeMB:  
                raturns the size of a file or folder in MB

		>>>getsizeMB(fullpath)

		fullpath --> full path to file or folder
                
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


def timestr():
	""" returns the actual time as a string -> HH:MM:SS"""
	ti = datetime.now().strftime("%H:%M:%S")
	return ti

def time():
	ti = datatime.now()
	return ti

def hostname():
	""" returns the actual host where the script is running"""
	host = socket.gethostname()
	return host


def folderCount(path, wildcard= "*",position = "m"):
	""" 
	retuns the count of folders or files in a folder

	with no given wildcard it uses * 
	with given wildcard the default is "*wildcard*"
	if you need to specify the wildcard you can use:
	      s for wildcard starts with --> str*  or  
	      e for wildcard ends with	 --> *.tif 
	"""
	if path[-1] != "/" or path[-1]!="\\":
		path = path+"/"
	if position == "m":
		wildcard = "*"+wildcard+"*"
	elif position == "s":
		wildcard = wildcard+"*"
	elif position == "e":
		wildcard == "*"+wildcard
	count = len(glob(path+wildcard))
	return count
		
def getsizeMB(fullpath):
    size = ("%.2f" % (os.path.getsize(fullpath)/1024/1024.0))
    return size
