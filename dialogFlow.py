# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 19:44:24 2018

@author: Administrator
"""


listRes = ['Citation', 'Blague', 'Devinette', 'Image', 'Video']

#import bddConn
import boutons
from random import randint
import datetime
import MYSQLBdd
import pandas as pd



class Dialog:
    
    def __init__(self, channel, publique):
        self.channel = channel
        self.publique = 0 
        if publique == 1:
            self.publique = 1          
        self.dialog = []
        self.humeur = 0
        self.intensite = 0
        self.humeurString = None
        self.demandPrivate = 0      
        self.state = None
    
    def incoming(self, event_data):
        print('incoming')
        msg = ''
        if event_data['type'] == "message":
            msg = event_data['text']
        if event_data['type'] == "buttonClicked":
            msg = event_data['value']
        time = datetime.datetime.fromtimestamp(float(event_data['time'])).strftime('%Y/%m/%d %H:%M:%S')
        self.dialog.append([msg, time, event_data['author']])
        return self.chooseAnswer()
          
    def sendMSG(self, message, attachment, private, user):
        print("message")  
        
    def chooseAnswer(self):
        print("chooseAnswer")
        lastMSG = self.dialog[-1][0]
        lastTime = self.dialog[-1][1]
        lastAuth = self.dialog[-1][2]
        
        answerText = lastMSG
        answerAttachment = None
        answerPrivate = 0
        answerTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y/%m/%d %H:%M:%S')
        answerAuth = lastAuth

        
        if self.humeur == 0 and not self.publique :
            self.state = "waitingHumeur"
            self.humeur = "unknown"
            answerText = boutons.button1[0]
            answerAttachment = boutons.button1[1]
        
        elif self.publique :
            answerText = "Et si nous allions discuter en privé ;)... \nj'ai plein de choses à te raconter,\n envoie moi un message !\(en bas à gauche :p )"
            answerPrivate = 1
            answerAuth = lastAuth
            
        elif self.state == "waitingHumeur":
            self.humeur = lastMSG
            self.state = "waitingIntensite"
            answerText = boutons.button2[0]
            answerAttachment = boutons.button2[1]
            
        
        elif self.state == "waitingIntensite":
            self.intensite = lastMSG
            self.state = "waitingHumeurExplanation"
            answerText = "Est ce que tu peux me dire pourquoi ??"
        
        elif self.state == "waitingHumeurExplanation":
            self.humeurString = lastMSG
            self.state = None
            
            #append the mood in db
            print('saving')
            print(lastAuth, self.humeur, self.intensite, self.humeurString ,lastTime)
            self.saveHumeur(lastAuth, self.humeur, self.intensite, self.humeurString ,lastTime)
            
            if self.humeur == "super" or self.humeur == "genial":
                answerText = "Ok, c'est parti pour une super journée alors :joy:"
        
            elif self.humeur == "moyen":
                answerText = "Courage ça va bien se passer :grinning:"
            
            elif self.humeur == "pas terrible" :
                answerText = "Courage! Ca va bien se passer :relieved:"
            
            elif self.humeur == "pas bien" :
                answerText = "Je suis là si tu as besoin de parler :hushed:"
                
            answerAttachment = self.getCookie()
            
            if '#mood' in lastMSG.split():
                if '#daily' in lastMSG.split():
                    answerText = "Mood"
                    answerAttachment = self.getHumeur("daily")
               
                if '#weekly' in lastMSG.split():
                    answerText = "Mood"
                    answerAttachment = self.getHumeur("weekly")
            
        
        if lastMSG == '#logs':
            answerText = str(self.dialog)
            
        if lastMSG == '#cookie':
            answerText = "Miam"
            answerAttachment = self.getCookie()
        
        #self.sendMSG(answerText, answerAttachment, 1)
        self.dialog.append([answerText, answerTime, 'BOT'])
        return (answerText, answerAttachment, answerPrivate, answerAuth)
 
    
    def getHumeur(self, range = "daily", hour =None):
        conn = MYSQLBdd.monSql()
        df = pd.DataFrame(data=[mood[1:] for mood in conn.getItemIntoTable("Mood")], columns = ["user", "humeur", "intensite", "humeurStr", "date"])
        conn.close()
        
        today = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        if range == "daily":
            rangeDays = [today]
            
        if range == "weekly":
            rangeDays =joursAvant(today, 7)
        
        #print(rangeDays)
            
        #df = df.drop[[df.date not in rangeDays]]
        
        #[user, humeur, intensite, humeurStr, date]
        #print(df)
        return "ok"
        
        
        
    def saveHumeur(self, user, humeur, intensite, humeurStr, date):
        conn = MYSQLBdd.monSql()
        liste_item = ['user', 'humeur', 'intensite', 'humeurSTR', 'dateStr']
        liste_value = [user, humeur, intensite, humeurStr, date]
        conn.insert_IntoTable("Mood" , liste_item , liste_value)
        conn.close()
        return 1    
    
    def getCookie(self):
        attachment = None
        cat = chooseRandom(listRes)
        conn = MYSQLBdd.monSql()
        res = conn.getItemIntoTable(cat)
        conn.close()
        if len(res) > 0:
            item = res[chooseRandom(range(len(res)))]            
            attachment = boutons.makeCake(cat, item)
        if attachment == []:
            print('erreur sur la ressource :')
            print(res)
            return self.getCookie()
        print(attachment)
        return attachment
            
    def getHumeur(self, delta):
        conn = MYSQLBdd.monSql() 
        if delta == "daily":
            rangeDays = MYSQLBdd.getDates(1)
            res = conn.agregationMood(rangeDays[1] , rangeDays[0])
            attachment = boutons.attachMood(rangeDays , res)
        if delta == "weekly":
            rangeDays = MYSQLBdd.getDates(7)
            res = conn.agregationMood(rangeDays[1] , rangeDays[0])
            attachment = boutons.attachMood(rangeDays , res)
        conn.close()        
        return attachment      
     
     
def chooseRandom(liste):
    return liste[randint(0, len(liste)-1)]

def joursAvant(date, deltaAvant):
    madate = datetime.datetime.strptime(date, '%Y/%m/%d %H:%M:%S').date()
    liste_jour = [(madate - dat.timedelta(i)) for i in range(deltaAvant)]
    liste_format = [i.strftime('%Y/%m/%d') for i in liste_jour]
    return liste_format   

def processTime(ts):
    return datetime.datetime.fromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M:%S')   
     

if __name__ == "__main__":
    cb = Dialog('None', 1)
    #print(str(cb.getHumeur()))
    #☼cb.getHumeurs()
    #print(cb.getHumeurs())
    #date = "2018-02-01"
    #liste = septDernierjours(date)
    #print(type(liste))
    #print(liste)
    #for res in cb.getCookie("all"):
    #    print(res)
    #print(chooseRandom(["a", "b", "c"]))
    #print(cb.getCookie("all"))
    #print(cb.getHumeur("weekly"))
    cb.getCookie()
    #cb.getHumeur("weekly")
    



"""Nathi
## Dates Nathi
def septDernierjours(date):
    madate = datetime.datetime.strptime(date, '%Y-%m-%d')
    liste_jour = [madate]
    liste_format = []
    for i in range(6):
        tmp = madate - dat.timedelta(1)
        liste_jour.append(tmp)
        madate =tmp
    for i in liste_jour:
       liste_format.append(i.strftime('%m/%d/%Y'))
    return liste_format    
    """

"""
def afficherMood():
    while 1:
        heure = dat.datetime.now().strftime('%H,%M,%S')
        if heure == "11,00,00" or heure =="16,00,00":
"""          
        


#datetime.now()