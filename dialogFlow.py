# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 19:44:24 2018

@author: Administrator
"""


listRes = ['Citation', 'Blague', 'Devinette', 'Image', 'Video']

import bddConn
#import pandas as pd
import boutons
import datetime as dat
from random import randint
import datetime

class Dialog:
    
    def __init__(self, channel, publique):
        self.channel = channel
        
        #print("public", publique)
        if publique == 1:
            self.publique = 1
        else:
            self.publique = 0
            
        self.dialog = []
        self.humeur = 0
        self.intensite = 0
        self.humeurString = None
        self.demandPrivate = 0
        
        self.state = None
        
            
    def newMSG(self, newMSG, time, author):
        self.dialog.append([newMSG, time, author])
        
        
        ans = self.chooseAnswer()
        if type(ans) != str:
            (ans, attach) = ans
        else:
            (ans, attach) = (ans, None)
        self.dialog.append([ans, '', 'BOT'])
        print(self.dialog)
        
        return (ans, attach)
        
        
    def chooseAnswer(self):
        lastMSG = self.dialog[-1][0]
        lastTime = self.dialog[-1][1]
        lastAuth = self.dialog[-1][2]

        
        if self.humeur == 0 and not self.publique :
            self.state = "waitingHumeur"
            self.humeur = "unknown"
            print("1")
            return (boutons.button1[0], boutons.button1[1])  
        
        if self.humeur == 0 and  self.publique and self.demandPrivate == 0:
            self.demandPrivate = 1
            print("2")
            return("Et si nous allions discuter en privé ;)... \nj'ai plein de choses à te raconter,\n envoie moi un message !\(en bas à gauche :p )")
            
        if self.state == "waitingHumeur":
            self.humeur = lastMSG
            self.state = "waitingIntensite"
            print("3")
            return (boutons.button2[0], boutons.button2[1])
        
        if self.state == "waitingIntensite":
            self.intensite = lastMSG
            self.state = "waitingHumeurExplanation"
            print("4")
            return("Est ce que tu peux me dire pourquoi ??", None)
        
        if self.state == "waitingHumeurExplanation":
            self.humeurString = lastMSG
            print("5")
            self.state = None
            
            #append the mood in db
            print('saving')
            print(lastAuth, self.humeur, self.intensite, self.humeurString ,lastTime)
            self.saveHumeur(lastAuth, self.humeur, self.intensite, self.humeurString ,lastTime)
            
            if self.humeur == "super" or self.humeur == "genial":
                print("6.1")
                return ("Ok, c'est parti pour une super journée alors :joy:", None)
        
            elif self.humeur == "moyen":
                print("6.2")
                return ("Courage ça va bien se passer :grinning:", None)   
            
            elif self.humeur == "pas terrible" :
                print("6.3")
                return ("Courage! Ca va bien se passer :relieved:", None) 
            
            elif self.humeur == "pas bien" :
                print("6.4")
                return ("Je suis là si tu as besoin de parler :hushed:", None)
        
        #if lastMSG == '#mood #daily':
        if '#mood' in lastMSG.split():
            if '#daily' in lastMSG.split():
                print("7.1")
                return self.getHumeur(range = "daily")
            
            if '#weekly' in lastMSG.split():
                print("7.2")
                return self.getHumeur("weekly")
            
        
        if lastMSG == '#logs':
            print("8")
            return (str(self.dialog),None)
        
        return (lastMSG, None)
 
    
    def getHumeur(self, range = "daily"):
        
        moods = [mood for mood in bddConn.getRes("Mood")]
        #print(moods)
        moods = moods[1:]
        #print(moods)
        dictH = {}
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).strftime('%m/%d/%Y')
        
        #print(today)
        if range == "daily":
            rangeDays = [today]
            
        if range == "weekly":
            rangeDays = septDernierjours(today)
            
            
        print(rangeDays)
        hums = ['super','genial','pas terrible','pas bien','moyen']
        for hum in hums:
            dictH[hum] = 0
        
        for mood in moods:
            print(mood)
            hum = mood[2]
            day = mood[5]#.strftime('%m/%d/%Y')
            print(day)
            dayt = day[:-8]
            dayt = dayt[5:] + dayt[:4]
            dayt = dayt.replace(' ','/').replace('-', '/')
            print(dayt)
            #dayt.replace()
            
            try:
                dayt = datetime.datetime.strptime(day, '%m/%d/%Y').replace(hour=0, minute=0, second=0, microsecond=0)
                #print(type(dayt))
                dayt = dayt.strftime('%m/%d/%Y')
                #print(type(dayt))
            except:
                pass
            
            #print("days" , day, dayt, today)
            if hum in hums:
                if dayt in rangeDays:
                    #print (dayt)
                    dictH[hum] += 1
                    
        if len(rangeDays) == 1:
            return ("humeurs pour le jour : {} \n".format(rangeDays[0]) + str(dictH))
        return ("humeurs pour l'intervalle : {} a {} \n".format(rangeDays[0], rangeDays[-1]) + str(dictH))

        
        
        
    def saveHumeur(self, user, humeur, intensite, humeurStr, date):
        bddConn.addRes("Mood", [user, humeur, intensite, humeurStr, date]) 
        return 1 
    
    """
    def getCookie(self, category = "all"):
        
        cookie = 0
        while cookie == 0:
            if category == 'all':
                category = chooseRandom(listRes)
                print (category)
            
            
            if category not in listRes:
                return ("error, invalid category")
        
            res = bddConn.getRes(category)
            if len(res) > 2:
                print(res)
                headers = res[0]
                res = chooseRandom(res.pop(0))
                cookie = res
                
        if "text" in headers:
            return 
            
        
        
        return res
        
   """     
        
        
def chooseRandom(liste):
    return liste[randint(0, len(liste)-1)]

def septDernierjours(date):
    madate = dat.datetime.strptime(date, '%m/%d/%Y')
    liste_jour = [madate]
    liste_format = []
    for i in range(6):
        tmp = madate - dat.timedelta(1)
        liste_jour.append(tmp)
        madate =tmp
    for i in liste_jour:
       liste_format.append(i.strftime('%m/%d/%Y'))
    return liste_format   
        
        
            
            
if __name__ == "__main__":
    cb = Dialog('None', 1)
    #print(str(cb.getHumeur()))
    #☼cb.getHumeurs()
    #print(cb.getHumeurs())
    date = "2018-02-01"
    #liste = septDernierjours(date)
    #print(type(liste))
    #print(liste)
    #for res in cb.getCookie("all"):
    #    print(res)
    #print(chooseRandom(["a", "b", "c"]))
    #print(cb.getCookie("all"))
    print(cb.getHumeur("weekly"))



"""Nathi
## Dates Nathi
def septDernierjours(date):
    madate = dat.datetime.strptime(date, '%Y-%m-%d')
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











#datetime.now()