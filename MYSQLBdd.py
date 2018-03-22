# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 15:32:58 2018

@author: Administrator
"""

import time
import mysql.connector
from mysql.connector import errorcode
import csv
import os
import datetime
from threading import Timer,Thread,Event


#VARS
#get the tokens to get access to Slack, port number and public url to access the server
for line in open("tokens.txt", "r").readlines():
    if "dbURL =" in line:
        dbURL = line[line.index('='):][1:].replace("\n","")
    if "baseSchemaName =" in line:
        schName = line[line.index('='):][1:].replace("\n","")       
    if "userDB =" in line:
        userName = line[line.index('='):][1:].replace("\n","")
    if "portDB =" in line:
        PORT = line[line.index('='):][1:].replace("\n","")
    if "passwordDB =" in line:
        pswDB = line[line.index('='):][1:].replace("\n","")
        
        
SQLtypes = ["TEXT", "TINYTEXT", "INT"]
CWD = os.getcwd()

"""        
print(dbURL, schName, userName, PORT, pswDB)
"""


        #tables c'est un dictionnaire contenant le nom des tables en clé et leurs descriptions en valeurs
tables = {}


tables ["Mood"] = (
            "CREATE TABLE `Mood`  ("
            "`id` bigint (32) AUTO_INCREMENT,"
            " `user` varchar(255) NOT NULL," 
            " `humeur` varchar(255) NOT NULL," 
            " `intensite` int(1) ," 
            "`humeurSTR` varchar(255),"
            "`dateSTR` varchar(255),"
            " PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB"   )


tables ["Citation"] = (
            "CREATE TABLE `Citation`  ("
            "`id` bigint (32) AUTO_INCREMENT,"
            " `quote` TEXT NOT NULL," 
            " `author` varchar(255) NOT NULL," 
            " PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB"    )


tables ["Blague"] = (
            "CREATE TABLE `Blague`  ("
            "`id` bigint (32) AUTO_INCREMENT,"
            " `text` TEXT NOT NULL," 
            " PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB"    )
    
tables ["Devinette"] = (
            "CREATE TABLE `Devinette`  ("
            "`id` bigint (32) AUTO_INCREMENT,"
            " `quote` TEXT NOT NULL," 
            " `answer` varchar(255) NOT NULL,"
            " PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB"    )
    

tables ["Video"] = (
            "CREATE TABLE `Video`  ("
            "`id` bigint (32) AUTO_INCREMENT,"
            " `url` varchar(255) NOT NULL," 
            " `shot_description` varchar(255) NOT NULL,"
            " PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB"    )


tables ["Image"] = (
            "CREATE TABLE `Image`  ("
            "`id` bigint (32) AUTO_INCREMENT,"
            " `url` varchar(255) NOT NULL," 
            " `shot_description` varchar(255) NOT NULL,"
            " PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB"    )

#class perpetualTimer():
#
#      self.t=t
#   def __init__(self,t,hFunction):
#      self.hFunction = hFunction
#      self.thread = Timer(self.t,self.handle_function)
#
#   def handle_function(self):
#      self.hFunction()
#      self.thread = Timer(self.t,self.handle_function)
#      self.thread.start()
#
#   def start(self):
#      self.thread.start()
#
#   def cancel(self):
#      self.thread.cancel()
      

class monSql :
    def __init__ (self, 
                 http = dbURL,
                 base = schName, 
                 user = userName,
                 port = PORT,
                 password =  pswDB,
                 ) :
        self.cnx = mysql.connector.connect(user=user, password=password,
                                           host=http, port=port,
                                           )
        self.cursor = self.cnx.cursor()
        # on regarde si la base existe et  sinon on cree
        try:
            self.cnx.database = base
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(base)
                self.cnx.database = base
            else:
                raise
                
                
                
    def create_database(self, base):
        try:
            self.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(base))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            raise
        return
    
    def close (self,) :
        self.cnx.close()
        
        


    def getFieldTable(self ,table , schema = "test_chatbot" ):
        liste_item = []        
        requete = """SELECT COLUMN_NAME AS `Field`
                 FROM information_schema.COLUMNS  
             WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}'
             ;""".format(schema , table)
        self.cursor.execute(requete)
        tmp =  self.cursor.fetchall()
        for i in tmp :
            liste_item.append(i[0])
        return liste_item[1:]
    
    #retun all rows of the table
    def getItemIntoTable(self, table):
        liste_item = []
        requete = """SELECT * FROM {}""".format(table)
        try:
            self.cursor.execute(requete)
            liste_item = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print("Failed retrieving database: {}".format(err))
            raise
        return liste_item
    
    #insert a row in a table    
    def insert_IntoTable(self ,table , liste_item , liste_value):
         """print(liste_item)
         #print(liste_value)
         #print([type(val) for val in liste_value])
         """
         liste_value = [mysqlStringPP(val) if type(val) == str else val for val in liste_value]
         """print(liste_value)
         """
         requete = "INSERT INTO `{}` ".format(table)
         requete +="("
         for i in range(len(liste_item)) :
             if liste_item[-1] == liste_item[i] :
                 requete = requete +liste_item[-1] 
             else:
                 requete = requete + liste_item[i] + ','
         requete +=") VALUES ("
         for j in range(len(liste_value)) :
             if liste_value[j] == liste_value[-1]:
                 requete = requete + "'" + liste_value[j] + "'"
             else :
                 requete = requete + "'" + liste_value[j] + "',"
         requete += ");"
         try :
             self.cursor.execute(requete)
             print('insertion succed')
             self.cnx.commit()
             
         except :
             print('insertion error')     
         

    def delete_IntoTable(self,table, id_table) :
        pre_requete = "SELECT COUNT(id) FROM {} WHERE id = {};".format(table , id_table)
        try :
            self.cursor.execute(pre_requete)
            val = self.cursor.fetchall()
            if val[0][0] == 1:                
                requete = "DELETE FROM {} WHERE id = {} ".format(table , id_table)
                self.cursor.execute(requete)
                print("delete item succed")
                self.cnx.commit()
            else: 
                print ("L'item que vous essayez de supprimer n'existe pas")
        except:
             print("Impossible de se connecter a la bdd")
        
    def delete_Table(self , table):
        requete = "DROP TABLE IF EXISTS  {}".format(table)
        try :
            print("!Deleting: {}".format(table))
            self.cursor.execute(requete)
            print("delete table  succed")
            self.cnx.commit()
        except :
            print ("delete table error")
    
    def getDBInfo(tabl = tables):
        liste_tables = []
        for name in tables.keys():
            liste_tables.append(name)
        return liste_tables    
     
    def execSqlcommand(self):
        requete = input("veuillez saisir votre SQL commande : \n")
        try:
            self.cursor.execute(requete)
            print("requete executée")
            val = self.cursor.fetchall()
            print(val)            
            self.cnx.commit()
        except :
            print("syntax invalid")   
            
            
    def sommeMood(self , date1 ,date2):       
        requete = """select count(*) from Mood as m 
        WHERE STR_TO_DATE( m.dateSTR , '%Y/%m/%d %T') BETWEEN '{}' AND '{}'
        ;""".format(date1, date2)
        try:
            
            print(requete)
            self.cursor.execute(requete)
            somme =(self.cursor.fetchall())
            print(somme)
        except mysql.connector.Error as err:
            print("Failed retrieving database: {}".format(err))
        return somme[0][0]
    
    
    def agregationMood(self, date1, date2):
        agr = {}
        requete = """select humeur ,count(*) as nb from Mood as m 
        WHERE STR_TO_DATE( m.dateSTR , '%Y/%m/%d %T') BETWEEN '{}' AND '{}'
        group by m.humeur;""".format(date1, date2)
        print(requete)
        try:
            self.cursor.execute(requete)
            agregation =(self.cursor.fetchall())
        except mysql.connector.Error as err:
            print("Failed retrieving database: {}".format(err))
        for i in agregation:
            agr[i[0]] = i[1]
        return agr
 
 
    def getMood(self):
        requete = """select * from Mood order by STR_TO_DATE( Mood.dateSTR , '%Y/%m/%d %T') desc;"""
        try:
            self.cursor.execute(requete)
            mood =(self.cursor.fetchall())
        except mysql.connector.Error as err:
            print("Failed retrieving database: {}".format(err))
        return(mood[:6])
         
    def create_table(self,
                     tables,
                     http = dbURL ,
                     base = schName,
                     user = userName,
                     password  = pswDB, 
                     isNew  = False):
        
        
        for name, ddl in tables.items():
            if isNew :
                command = "DROP TABLE IF EXISTS " + name
                try :
                    print ("Dropping table {}  =>".format(name))
                    self.cursor.execute(command)
                except:
                    print (" error during drop ?")
                    raise
                else:
                    print (" Drop ok")
                    
            try:
                print("Creating table {}: ".format(name))
                self.cursor.execute(ddl)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
                    raise
            else:
                print("OK")
            continue
        return
    
    
    #import a table from a csv file
    #will create a table adapted to the file
    #if table name already exists, will be deleted
    def importTable(self, csvFile, delimiter, colTypes):      
        tableName = csvFile.split(".")[-2].split("\\")[-1]
        if csvFile.split("\\")[0] not in ['C:', 'H:', 'D:']:
           csvFile = mysqlStringPP(CWD + '\\' + csvFile)
        print(csvFile)
              
        #Delete existing tablez       
        
        self.delete_Table(tableName)
        """
        command = "DROP TABLE IF EXISTS " + tableName
        try :
            print ("Dropping table {}  =>".format(tableName))
            self.cursor.execute(command)
        except:
            print (" error during drop ?")
            raise
        else:
            print (" Drop ok")
        """

        #create sql table creation statement
        ddl = "CREATE TABLE `{}`  (""`ID` bigint (32) AUTO_INCREMENT,".format(tableName)
        for col, typ in colTypes.items():
            ddl += " `{}` {} NOT NULL,".format(col, typ)   
        ddl += " PRIMARY KEY (`ID`)"") ENGINE=InnoDB"

        #execute it
        try:
            print("Creating table {}: ".format(tableName))
            self.cursor.execute(ddl)
            self.cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
                raise
        else:
            print("OK") 
        
        #finally load the file
        headers = 1
        #LINES TERMINATED BY '\\r \\n' IGNORE
        ddl = "LOAD DATA LOCAL INFILE '{}' INTO TABLE {} FIELDS TERMINATED BY '{}' IGNORE {} ROWS (".format(csvFile, tableName, delimiter, headers)
        for col in  colTypes.keys():
            ddl+= "{}.{} ,".format(tableName, col)
        ddl = ddl[:-1]
        ddl+= ")  SET ID = NULL ;"
        print(ddl)
        try:
            print("import file: {}".format(csvFile))
            self.cursor.execute(ddl)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print(err.msg)
            raise
        else:
            print("ok")
        return      

def mysqlStringPP(text):    
    import re
    
    # define desired replacements here
    rep = {
            "'":"''",
            '"':'""',
            "\n":"\n",
            '\{}'.format(''):"\\\\"
            
           }
    # use these three lines to do the replacement
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    
 




def menu():
    print("\nGestion de la base de données:\n")
    print("0: quitter\n1: ajouter un élement dans la base\n2: supprimer un élement de la base\n3: afficher la base\n4: input a direct SQL command (check your syntax!!)\n5: creer ou maj la base de données\n6: importer une table depuis un .csv")
    Base = monSql()
    choix = input("choix: ")
    print("\n")
        
    if choix == "1" :
        liste_table = Base.getDBInfo()
        for table in liste_table :
            print(table)
        table = ''
        while table not in liste_table:
            table = input("Dans quelle table voulez vous faire une insertion ?\n")
        res =  []
        fields = Base.getFieldTable(table)
        print(fields)
        for col in fields :
            if col[1] != 'id' :
                res.append(input("{} :".format(col)))
        Base.insert_IntoTable(table , fields , res)
        
        
    elif choix == "2" :
        liste_table = Base.getDBInfo()
        for table in liste_table :
            print(table)
        choixTable = ''
        while choixTable not in liste_table:
            choixTable = input("De quelle table s'agit-il ? \n")
        print('[' + choixTable + ']')
        listeItem =  Base.getItemIntoTable(choixTable)
        for  items in listeItem :
            print(items)
        choixId = input("Quelle id voulez vous supprimer \n")
        
        Base.delete_IntoTable(choixTable, choixId)
    
    
    elif choix == "3":
        liste_table = Base.getDBInfo()
        for table in liste_table:
            print('[' + table + ']')
            listeItem =  Base.getItemIntoTable(table)
            for  items in listeItem :
                print(items)
            print('\n')
            
    elif choix == "4":
        Base.execSqlcommand()
        
    elif choix == "5" :
        Base.create_table(tables)
        
    elif choix == "6":
        try:
            from Tkinter import Tk
            from tkFileDialog import askopenfilename
            Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
            filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        except:
            filename = input("entrer le nom du fichier avec son chemin\n")
            pass
        delimiter = input("delimiter?\n")        
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter = delimiter)
            cols = next(reader)
            colTypes = {}
            for col in cols:
                colName = input("Nom de la colonne: (sugg: {})\n".format(col))
                colTypes[colName] = None
                while colTypes[colName] not in SQLtypes:
                    colTypes[colName] = input("type de la columne parmi {}\n".format(SQLtypes))          
        Base.importTable(filename, delimiter, colTypes) 
    
        
    elif choix == "0":
        Base.close()
        return 1
    else :
        menu()
        
    menu()
   
def getDates(delta):
    d = datetime.datetime.now()
    print(d)
    d2=d- datetime.timedelta(days=delta)
    print(d2)
    date1 = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    date2=d2.strftime('%Y/%m/%d %H:%M:%S')
    print(date1)
    print(date2)
    return date1, date2   
 

    
if __name__ == "__main__" :
#    Base = monSql()
#    menu()
#    getDates(delta=3)
#    print(date1)
#    print(date2)
#    res = Base.agregationMood(date2 ,date1)
#    print(res)  
#    #print(mysqlStringPP("aujourd'hui j'ai \ mangé un poisson\n :)"))
    
    t = perpetualTimer(1,test)
    t.start()
    
    print("ok 2248")
    
#    print(Base.getMood())
    
