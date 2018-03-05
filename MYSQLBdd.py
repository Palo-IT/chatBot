# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 15:32:58 2018

@author: Administrator
"""


import mysql.connector
from mysql.connector import errorcode

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
            " `quote` varchar(255) NOT NULL," 
            " `author` varchar(255) NOT NULL," 
            " PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB"    )


tables ["Blague"] = (
            "CREATE TABLE `Blague`  ("
            "`id` bigint (32) AUTO_INCREMENT,"
            " `text` varchar(255) NOT NULL," 
            " PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB"    )
    
tables ["Devinette"] = (
            "CREATE TABLE `Devinette`  ("
            "`id` bigint (32) AUTO_INCREMENT,"
            " `quote` varchar(255) NOT NULL," 
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



class monSql :
    def __init__ (self, 
                 http = "127.0.0.1",
                 base = "test_chatbot", 
                 user = "root",
                 port = 3306,
                 password =  "eisti0001",
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
    
    
    
    def getItemIntoTable(self, table):
        liste_item = []
        requete = """SELECT * FROM {}""".format(table)
        try:
            self.cursor.execute(requete)
            liste_item = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            raise
        return liste_item
    
    
    
        
    def insert_IntoTable(self ,table , liste_item , liste_value):
         print(liste_item)
         print(liste_value)
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
        requete = "DROP TABLE IF EXISTs  {}".format(table)
        try :
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
    
    
    
    def create_table(self,
                     tables,
                     http = "127.0.0.1" ,
                     base = "test_chatbot",
                     user = 'root',
                     password  = 'eisti0001', isNew  = False):
        
        
        for name, ddl in tables.items():
            if isNew :
                command = "DROP TABLE IF EXISTs " + name
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
    

            
    


def menu():
    print("\nGestion de la base de données:\n")
    print("0: quitter\n1: ajouter un élement dans la base\n2: supprimer un élement de la base\n3: afficher la base\n4: input a direct SQL command (check your syntax!!)\n5: creer ou maj la base de données")
    Base = monSql()
    choix = input("choix: ")
    print("\n")
    
    
    if choix == "5" :
        Base.create_table(tables)
        
        
    elif choix == "1" :
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
    
        
    elif choix == "0":
        Base.close()
        return 1
    else :
        menu()
        
    menu()
        
    
    
if __name__ == "__main__" :
    print ("on y va")
    menu()
    print ("end_of_job")