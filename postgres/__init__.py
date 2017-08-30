# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 19:15:18 2016

@author: fw56moba
"""


def Help(inhal = ''):
    HelpInhalt =  sorted(['create_pg_Table_sql_command', 'create_pg_Table', 'create_pg_Table_load_to_pg'])
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
            ###              MacPyver.postgres             ###
            ###   The Swissknife like Python-Package for   ###
            ###        work in general and with GIS        ###
            __________________________________________________
                
                How to use the functions:
                __________
                
                __________________________________________
                
             """,
             
            "create_pg_Table_sql_command":"""create_pg_Table_sql_command:       
                returns the executable SQL command for postgres
                
                >>> create_pg_Table_sql_command(fullpath, tablename, sep=';', header=0)
                
                fullPath  --> full path plus the filename
                tablename --> table name for the new table
                sep       --> default sep is ;
                header    --> default header is the first line in the csv
                

                ______________________________________________________________________
            """,
            
            "create_pg_Table":"""create_pg_Table:  
                creates a table in the postgres database
                
                >>> create_pg_Table(full_path, tablename, host, 
                                    user, password, dbname, 
                                    schema='public', port=5432, 
                                    sep=';', header=0):
                
                fullPath  --> full path plus the filename
                tablename --> table name for the new table
                host      --> database host
                user      --> your database user name
                password  --> your database password
                dbname    --> database you want to create the table
                schema    --> schema you want to create the table, default is public
                port      --> port of your database, default is 5432
                sep       --> default sep is ;
                header    --> default header is the first line in the csv

                ______________________________________________________________________
            """,
                     
            "create_pg_Table_load_to_pg":"""create_pg_Table_load_to_pg:  
                creates a table in the postgres database and loads the data to the 
                database
                
                >>> create_pg_Table_load_to_pg(full_path, tablename, host, 
                                    user, password, dbname, 
                                    schema='public', port=5432, 
                                    sep=';', header=0):
                
                fullPath  --> full path plus the filename
                tablename --> table name for the new table
                host      --> database host
                user      --> your database user name
                password  --> your database password
                dbname    --> database you want to create the table and load the data
                schema    --> schema you want to create the table, default is public
                port      --> port of your database, default is 5432
                sep       --> default sep is ;
                header    --> default header is the first line in the csv

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
        print ">>> Fehler: Wort nicht gefunden <<<"
        print ""      
        for ele in HelpInhalt:
            print myDic[ele]       


try:
    import psycopg2 as pg
    import pandas as pd
    from sqlalchemy import create_engine 


    def create_pg_Table_sql_command(full_path, tablename, sep=';', header=0, write= False):
        #read csv with pandas
        data = pd.read_csv(full_path, sep=sep,header=header)
        #get header from the readed data
        colL = list(data.columns)
        #turn the columnnames to lower letters and replace sp[ace by underline]
        colL = [x.lower().replace(' ','_') for x in colL]
        #update the columnnames
        data.columns = colL
        colType = list(data.dtypes)
        #create empty list, output
        op_list = []
        #append the columnname and the datatype /varchar length
        for x in range(len(colL)):
            if str(colType[x]) == 'int64':
                op_list.append(colL[x] + ' integer')
                #print colL[x] + ' integer, '
            elif str(colType[x]) == 'float64' or str(colType[x]) == 'float':
                op_list.append(colL[x] + ' float')
                #print colL[x] + ' float, '
            elif str(colType[x]) == 'object':
                #get max length of the cells in the column
                leng = data[colL[x]].map(lambda y: len(str(y))).max()
                op_list.append(str(colL[x]) + ' varchar(' + str(leng) +')')
                #print str(colL[x]) + ' varchar(' + str(leng) +'), '
            else:
                print colL[x] + ' error '
        #return sql command and the data; this is used in the function create_pg_Table_load_to_pg
        if write == True:
            sql = "CREATE TABLE IF NOT EXISTS %s (index integer, %s)" % (tablename   , (", ").join(op_list))
            return sql, data
        #return sql command and the data; this is used in the this function and create_pg_Table, 
        else:
            sql = "CREATE TABLE IF NOT EXISTS %s (%s)" % (tablename   , (", ").join(op_list))
            return sql
        
    
    def create_pg_Table(full_path, tablename, host, user, password, dbname, schema='public', port=5432, sep=';', header=0 ):
        #get the sql command         
        sql = create_pg_Table_sql_command(full_path, tablename, sep, header, write= False)
        #create the connection string for the database
        pg_conn_str = "host=%s port=%d user=%s password=%s dbname=%s" % (host, port, user, password, dbname)
        #connect to the database
        pg_conn = pg.connect(pg_conn_str)
        #create a cursor on the database
        pg_cur = pg_conn.cursor()
        try:
            #execute the sql command
            pg_cur.execute(sql)
            #commit the sql command
            pg_conn.commit()
            print 'table created'
        except:
            print 'table exists already'
        pg_conn.close()

    
    def create_pg_Table_load_to_pg(full_path, tablename, host, user, password, dbname, schema='public', port=5432, sep=';', header=0, ):
        #get the sql command and the data from the given table
        sql, data = create_pg_Table_sql_command(full_path, tablename, sep=sep, header=header, write= True)
        #create the connection string for the database
        pg_conn_str = "host=%s port=%d user=%s password=%s dbname=%s" % (host, port, user, password, dbname)
        #connect to the database
        pg_conn = pg.connect(pg_conn_str)
        #create a cursor on the database
        pg_cur = pg_conn.cursor()
        try:
            #execute the sql command
            pg_cur.execute(sql)
            #commit the sql command
            pg_conn.commit()
            print 'table created'
        except:
            print 'table exists already'
        #create a engine connection to the database
        engine = create_engine(r'postgresql://%s:%s@%s:%d/%s' % (user, password,host,port,dbname))
        #append the data to the created table
        data.to_sql(tablename,engine,if_exists='append')
        pg_conn.close()
    
except ImportError, e:
    pass # module doesn't exist, deal with it.
