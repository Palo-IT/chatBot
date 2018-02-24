# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:59:13 2018

@author: Nathaniel
"""


#AddHumeur
#manage logs
#Add unique ID for every ressources


listRes = ['Citation', 'Blague', 'Devinette', 'Image', 'Video']

import sqlite3
import os 
import shutil
import urllib.request
from tkinter.filedialog import askopenfilename

DBPATH = os.getcwd() + '\dataBase'
CATEGORIES = ["Citation", "Blague", "Devinette", "Video", "Image"]
TYPES = {"INTEGER":int, "TEXT":str}

def createDB():
    
    #create a database: create a folder dataBase, in which there is the database.db, the ressources in a rec folder and all logs in a 
    #logs folders
    if os.path.exists(DBPATH) == False:
        os.mkdir(DBPATH)
    os.chdir(DBPATH)
           
    connexion = sqlite3.connect('{}\{}'.format(DBPATH, 'DBTAM.db')) 
    curseur = connexion.cursor()  #Récupération d'un curseur
    
    curseur.execute('''   
        CREATE TABLE IF NOT EXISTS Citation(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        quote TEXT , 
        author TEXT
    );    
    ''')
        
    #def addHumeurs(user, humeur, intensite, humeurStr, date):
    curseur.execute('''   
        CREATE TABLE IF NOT EXISTS Mood(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        user TEXT,
        humeur TEXT,
        intensite INTEGER,
        humeurSTR TEXT,
        date TEXT
    );    
    ''')
        
        
    curseur.execute('''   
        CREATE TABLE IF NOT EXISTS Blague(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        text TEXT 
    );    
    ''')
        
    curseur.execute('''   
        CREATE TABLE IF NOT EXISTS Devinette(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        quote TEXT , 
        answer TEXT
    );    
    ''')
        
    curseur.execute('''   
        CREATE TABLE IF NOT EXISTS Video(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        url TEXT , 
        short_description TEXT
    );    
    ''')
        
    curseur.execute('''   
        CREATE TABLE IF NOT EXISTS Image(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        url TEXT , 
        short_description TEXT
    );    
    ''')
        
    
        
    connexion.commit() 
    connexion.close()
    
    resPath = "{}\{}".format( DBPATH, "res") 
    if os.path.exists(resPath) == False:
        os.mkdir(resPath)

    
    logPath = "{}\{}".format( DBPATH, "logs") 
    if os.path.exists(logPath) == False:
        os.mkdir(logPath)
    os.chdir(logPath)
    #create en empty file for the logs 
    open('logs', 'a').close()

    #create an empty file to record the moods
    open('humeurs.csv', 'a').close()
    
    return "base créée ou mis à jour avec succès!"  
    
def addRes(table, res):
    db = '{}\{}'.format(DBPATH, 'DBTAM.db')
    connexion = sqlite3.connect(db)
    curseur = connexion.cursor()
    
    colStr=''
    valStr=''

    cols = [cols[1] for cols in curseur.execute("PRAGMA table_info({})".format(table))]

    cols.remove('id')
    for i in range(len(cols)):
        colStr += str(cols[i]) + ","
        valStr += "?,"
        
        #in case we have an url, ie a ressource to import:
        if str(cols[i]) == "url":
            resPath = "{}\{}\{}".format( DBPATH, "res", table) 
            if os.path.exists(resPath) == False:
                os.mkdir(resPath)
            if "www" in res[i] or "http" in res[i]:
                urllib.request.urlretrieve(res[i], "{}\{}".format(resPath, str(res[i]).split("/")[-1]))
            else:
                shutil.copy(res[i], resPath)              
        
    curseur.execute('INSERT INTO {} ({}) VALUES ({})'.format(table, colStr[:-1], valStr[:-1]), res)     
    connexion.commit()
    connexion.close()
    return "Ajouté: {} a {}".format(res, table)   
def deleteRes(category, id):
    db = '{}\{}'.format(DBPATH, 'DBTAM.db')
    connexion = sqlite3.connect(db)
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM {} WHERE id = {}".format(category, id))
    connexion.commit()  #Validation des modifications
    connexion.close()
    return("Delete item with id = {} from {} with success!".format(id, category))

def getRes(category = "None"):
    db = '{}\{}'.format(DBPATH, 'DBTAM.db')
    connexion = sqlite3.connect(db)
    curseur = connexion.cursor()
    tables = [table[0] for table in curseur.execute("select name from sqlite_master where type = 'table';").fetchall()]
    req = []
    
    if category == "all":
        for table in tables:
            #req.append("-----------------------")
            req.append(table)
            cols = [cols[1] for cols in curseur.execute("PRAGMA table_info({})".format(table))]
            req.append(cols)
            for row in curseur.execute("SELECT * FROM {}".format(table)).fetchall():
                req.append(row)
            req.append("")
        return req
    
    elif category in tables :
        req = [[cols[1] for cols in curseur.execute("PRAGMA table_info({})".format(category))]]
        for row in curseur.execute( "SELECT * FROM {}".format(category) ).fetchall():
            req.append(row)
        
        return req          
    
    connexion.close()
    
def directCmdSQL(cmdSQL):
    db = '{}\{}'.format(DBPATH, 'DBTAM.db')
    connexion = sqlite3.connect(db)
    curseur = connexion.cursor()
    curseur.execute(cmdSQL)
    connexion.commit()  #Validation des modifications
    return curseur.fetchall()
    connexion.close()

def getDBInfo():
        db = '{}\{}'.format(DBPATH, 'DBTAM.db')
        connexion = sqlite3.connect(db)
        curseur = connexion.cursor()
        tree = {}
        for table in curseur.execute("select name from sqlite_master where type = 'table';").fetchall():
            tree[table[0]] = [cols for cols in curseur.execute("PRAGMA table_info({})".format(table[0]))]
        connexion.close()
        return tree
        
def getLog():
    return "{}\{}\{}".format( DBPATH, "logs", "logs")

def addLog(logs):
    with open("{}\{}\{}".format( DBPATH, "logs", "logs"), "a") as file:
        for log in logs:
            file.write(log+ '\n')
    return 1 


def dbUI():
    print("\nGestion de la base de données:\n")
    print("0: quitter\n1: ajouter un élement dans la base\n2: supprimer un élement de la base\n3: afficher la base\n4: input a direct SQL command (check your syntax!!)\n5: creer ou maj la base de données")
    choix = input()
    
    if choix == "5":
        print(createDB())
        
    elif choix == "1":
        tree = getDBInfo()        
        [print(table) for table in tree.keys()]
        table = ''
        while table not in tree.keys():
            table = input("Quelle Catégorie/ table remplir?\n")
        print("Renseigner les valeurs au format renseigné:\n")
        res = []
        cols = tree[table]
        for col in cols:
            if col[1]!= 'id': 
                if col[1] == 'url':
                    if input("local?\nO si fichier stocké en local\nN si fichier disponible par URL\n") == "O":
                        url = askopenfilename() # show an "Open" dialog box and return the path to the selected file
                    else:
                        url = input("entrer l'url\n")
                    res.append(url)
                else:
                    res.append(TYPES[col[2]](input("{} as {}:\n".format(col[1],col[2]))))   
        print(addRes(table, res))    
        
    elif choix == "2":
        for table in getDBInfo().keys():
            print(table)
        table = str(input("Catégorie ?\n"))
        [print(row) for row in getRes(table)]
        id = str(input("ID de la ressource a supprimer ?\n"))
        print(deleteRes(table, id ))
    
    elif choix == "3":
        [print(row) for row in getRes(str(input("Entrer all pour toute la base\nou nom d'une table \n")))]
            
    
    elif choix == "4":
        retour = directCmdSQL(str(input("enter a SQL command\n")))
        if len(retour) != 0:
            [print(row) for row in retour]
            
    
    elif choix == "0":
        return 1
    
    else:
        dbUI()
    dbUI()

        
if __name__ == "__main__":
     dbUI()
    #print(getRes("Image",3))
