# coding: utf-8
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 19:44:24 2018

@author: Administrator
"""

#Ce fichier est centré sur la classe Dialog, qui a pour objectif de gérer une conversation
#Elle est donc uniquement focalisé sur des problématique de dialogue (étant donné ce qe dit ou fait l'utilisateur, que doit répondre ou envoyer le bot)
#L'état de la discussion est repéré notamnent par la variable state, qui permet de connaitre le stade de la conversation et ce qu'attend le bot
#Un historique de la conversation est stocké dans la variable dialog (mais non exporté dans la bdd)
#Les actions comme un clique sur un bouton sont considérés comme un message, dont le texte est la valeur du bouton cliqué.
#Selon le statut publique ou non de la conversation, le bot peut avoir affaire a plusieurs utilisateurs différents

listRes = ['Citation', 'Blague', 'Devinette', 'Image', 'Video']

import boutons
from random import randint
import datetime
import MYSQLBdd
import random
import logging


class Dialog:
    # Objet Dialog a chaque utilisateur un objet dialogue et crée et ainsi que pour chaque chaine (Slack) utilisant le bot
    def __init__(self, channel, publique , t):
        self.channel = channel
        self.bool = 1
        self.chaine= datetime.date.today()
        self.publique = 1 if publique == 1 else 0        
        self.users = {} if publique == 1 else None      
        self.dialog = []
        self.humeur = 0
        self.intensite = 0
        self.humeurString = None
        self.demandPrivate = 0      
        self.state = None
        self.t = t
        self.randomHour= "not possible" if self.publique == 1 else getRandomhour()
        self.asked = 0
        self.conn = MYSQLBdd.monSql()
        #logging.basicConfig(filename ='test', level=logging.INFO, 
        #                   format='[%(levelname)s] %(asctime)s %(message)s',
        #                   datefmt='%d/%m/%Y %H:%M:%S',)
        
        
        
        
    
    def incoming(self, event_data):
        #fonction incoming permet d'analyser un evenement qui se produit sur les channel afin d'assigner des veleurs au attibut d'un objet Dialog
        print('incoming')
        logging.info('incoming')
        msg = ''
        if event_data['type'] == "message":
            msg = event_data['text']
            #logging.info('text'+msg)
        if event_data['type'] == "buttonClicked":
            msg = event_data['value']
            #logging.info('buttonClicked'+msg)
        time = datetime.datetime.fromtimestamp(float(event_data['time'])).strftime('%Y/%m/%d %H:%M:%S')
        self.dialog.append([msg, time, event_data['author']])
        if self.publique == 1:
            if event_data['author']  not in self.users:
                self.users[event_data['author']] = self.chaine
        
        return self.chooseAnswer()
          
    def sendMSG(self, message, attachment, private, user):
        #fct inutile mes permets de verifier l'intégrité des classe héritant de la class dialog
        print("message")  
    
    
        
    def chooseAnswer(self):
        #fonction qui choisis parmis l'evenement qui viens de se passer une réponse adéquat
        print("chooseAnswer")
        lastMSG = self.dialog[-1][0]
        lastTime = self.dialog[-1][1]
        lastAuth = self.dialog[-1][2]
        
        
        answerText = None
        answerAttachment = None
        answerPrivate = 0
        answerTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y/%m/%d %H:%M:%S')
        answerAuth = lastAuth

        
        if self.humeur == 0 and not self.publique :
            self.state = "waitingHumeur"
            self.humeur = "unknown"
            answerText = boutons.button1[0]
            answerAttachment = boutons.button1[1]
            
        elif self.publique == 0  and self.state == "explanationGived" :
            answerText = "Merci d'avoir participé à notre questionnaire sur le Mood. Pour afficher le mood du jour, entrez #mood #daily et pour la semaine entrez #mood #weekly"
      
        
        elif self.publique and ( self.users[lastAuth] == datetime.date.today() ):
            
            answerText = "Et si nous allions discuter en privé ;)... "
            self.users[lastAuth]  = datetime.date.today() + datetime.timedelta(days=1)
            answerPrivate = 1
            answerAuth = lastAuth
            
            
            
            
        elif self.state == "waitingHumeur" and self.asked == 0:
            self.humeur = lastMSG
            self.state = "waitingIntensite"
            answerText = boutons.button2[0]
            answerAttachment = boutons.button2[1]
            
        
        elif self.state == "waitingIntensite" and self.asked == 0:
            self.intensite = lastMSG
            self.state = "waitingHumeurExplanation"
            answerText = "Est ce que tu peux me dire pourquoi ??"
        
        elif self.state == "waitingHumeurExplanation" and self.asked == 0:
            self.humeurString = lastMSG
            self.state = None
            self.state = "explanationGived"
            self.randomHour = getRandomhour()
            self.asked = 1
            #append the mood in db
            print('saving')
            print(lastAuth, self.humeur, self.intensite, self.humeurString ,lastTime)
            self.saveHumeur(lastAuth, self.humeur, self.intensite, self.humeurString ,lastTime)
            
            if self.humeur == "heureux" or self.humeur == "serein":
                answerText = "Ok, c'est parti pour une super journée alors :joy:"
        
            elif self.humeur == "surpris":
                answerText = "Courage ça va bien se passer :grinning:"
            
            elif self.humeur == "stressé" :
                answerText = "Courage! Ca va bien se passer :relieved:"
            
            elif self.humeur == "en colère" :
                answerText = "Je suis là si tu as besoin de parler :hushed:"
                
            answerAttachment = self.getCookie()
            
        if '#mood' in lastMSG.split() and not self.publique:
            if '#daily' in lastMSG.split():
                answerText = "Mood"
                answerAttachment = self.getHumeur("daily")
                #logging.info("reponse mood daily" + answerAttachment)
               
            if '#weekly' in lastMSG.split():
                answerText = "Mood"
                answerAttachment = self.getHumeur("weekly")
            
            
        
        if lastMSG == '#logs':
            answerText = str(self.dialog)
            
        if lastMSG == '#cookie' and self.publique!= 1:
            answerText = "Miam"
            answerAttachment = self.getCookie()
        
        #self.sendMSG(answerText, answerAttachment, 1)
        self.dialog.append([answerText, answerTime, 'BOT'])
        return (answerText, answerAttachment, answerPrivate, answerAuth)
 
                    
        
    def saveHumeur(self, user, humeur, intensite, humeurStr, date):
        #permet de sauvgarder l'humeur sur la base mySql
        
        liste_item = ['user', 'humeur', 'intensite', 'humeurSTR', 'dateStr']
        liste_value = [user, humeur, intensite, humeurStr, date]
        self.conn.insert_IntoTable("Mood" , liste_item , liste_value)
        return 1    
    
    def getCookie(self):
        # Se connecte a la base de donner pour allé chercher un cookie (Blaque , citation , Image , ...) de maniere aleatoire
        attachment = None
        cat = chooseRandom(listRes)
        res = self.conn.getItemIntoTable(cat)
        if len(res) > 0:
            item = res[chooseRandom(range(len(res)))]            
            attachment = boutons.makeCake(cat, item)
        if attachment == []:
            print('erreur sur la ressource :')
            print(res)
            return self.getCookie()
        return attachment
            
    def getHumeur(self,delta):
        #Se connecte a la base pour renvoyer soit le mood de la semaine, soit de le journée... dépant du parametre delta
        if delta == "daily":
            rangeDays = MYSQLBdd.getDates(1)
            res = self.conn.agregationMood(rangeDays[1] , rangeDays[0])
            #logging.info("days"+rangeDays[1]+"day0"+rangeDays[0])
            
            resSomme = self.conn.sommeMood(rangeDays[1] , rangeDays[0])
            for i in res:
                res[i] = str(round((res[i]/resSomme)*100,1)) +"%"
                attachment = boutons.attachMoodDaily(res)
                """
                logging.info("res daily"+res[i])
                try:
                    logging.info("reponse"+attachment)
                except Exception as e:
                    logging.error(str(e))
                """
                
        if delta == "weekly":
            rangeDays = MYSQLBdd.getDates(7)
            res = self.conn.agregationMood(rangeDays[1] , rangeDays[0])
            resSomme = self.conn.sommeMood(rangeDays[1] , rangeDays[0])
            for i in res:
                res[i] = str(round((res[i]/resSomme)*100,1)) +"%"
                attachment = boutons.attachMoodWeekly(res)       
        return attachment               
     
     
   
     
     
def chooseRandom(liste):
    return liste[randint(0, len(liste)-1)]

     
def getRandomhour():
    #return une heure de manière aléatoire fixer entre 9h00 et 14h00 
    a=random.randint(0,18000)
    h=int(a/3600) + 9
    if h<10:
        heure=str("0" + str(h))
    else:
        heure=str(h)
    res_h = a%3600
    m=int(res_h/60)
    if m<10:
        minute=str("0" + str(m))
    else:
        minute=str(m)
    s=res_h%60
    if s<10:
        seconde=str("0" + str(s))
    else:
        seconde=str(s)
    randomhour=str(heure + ":" + minute + ":" + seconde)
    return randomhour

if __name__ == "__main__": 
    print("Not this file to execute please try serverSlack.py")
