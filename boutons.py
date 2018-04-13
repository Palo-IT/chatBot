# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 22:06:11 2018

@author: Administrator
"""

#Toutes les fonctions de ce fichier ont pour objectif de construire des objets attachemets
#Ces objets, de format JSON peuvent être directement inclus dans les messages passés à l'api Slack


#bouton1 constuit l'attachement (les boutons qui apparaisent sur Slack) pour la première partie du scénario humeur du jour
button1 = [
        "Comment décrirais tu ton humeur du jour?",
            [
        {
            "text": "Choisis ton intensité !",
            "fallback": "Disons: Heureux, Serein, Surpris, Stressé, En colère",
            "callback_id": "humeur_type",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "humeur",
                    "text": " Heureux :smiley:",
                    "type": "button",                  
                    "value": "heureux"
                    
                },
                {
                    "name": "humeur",
                    "text": "Serein :relaxed:",
                    "type": "button",
                    "value": "serein"
                },
                {
                    "name": "humeur",
                    "text": "Surpris :flushed:",
                    "type": "button",
                    "value": "surpris"
                },
       
                {
                    "name": "humeur",
                    "text": "Stressé :worried:",
                    "type": "button",
                    "value": "stressé"
                 },
                 {
                    "name": "humeur",
                    "text": "En colère :angry:",
                    "type": "button",
                    "value": "en colère"
                 }
                
                
            ]
        }
    ]
            
            ]

#bouton2 construit les boutons pour la deuxième partie du scénario humeur          
button2 = [
        "Et quelle est l'intensité de ton humeur ?",
        [
        {
            "text": "Sur une echelle de 1 a 5, comment evalurais tu l'intensité de ton humeur",
            "fallback": "Disons: Super, génial, moyen, ok, pas terrible, pas bien",
            "callback_id": "intensité",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
              
       
            
                 {
                    "name": "intensite",
                    "text": "  1  ",
                    "type": "button",
                    "value": "1"
                 },
                
                {
                    "name": "intensite",
                    "text": "  2  ",
                    "type": "button",
                    "value": "2"
                 },
                 {
                    "name": "intensite",
                    "text": "  3  ",
                    "type": "button",
                    "value": "3"
                 },
                                {
                    "name": "intensite",
                    "text": "   4   ",
                    "type": "button",
                    "value": "4"
                },
                                        
                  {
                    "name": "intensite",
                    "text": "   5  ",
                    "type": "button",                  
                    "value": "5"
                    
                }
             
           
            ]
        }
    ]
            ]


#Cette fonction permet de construire les boutons qui affichent l'humeur du jour
#Note; Ces boutons ne sont pas prévus pour être cliqués
def attachMoodDaily(agrMood):
    titre = "humeur du jour"
    attach =  [
                    {
                            "title": titre,
                            "fields":  []
                        }
                    ]
    for key, val in agrMood.items():
        dic = {}
        dic["title"] = key
        dic["value"] = val
        dic["short"] = "true"
        attach[0]["fields"].append(dic)
    return attach

def attachMoodWeekly(agrMood):
    titre = "humeur de la semaine"
    attach =  [
                    {       "color": "#3AA3E3",
                            "title": titre,
                            "fields":  []
                        }
                    ]
    for key, val in agrMood.items():
        dic = {}
        dic["title"] = key
        dic["value"] = val
        dic["short"] = "true"
        attach[0]["fields"].append(dic)
    return attach


#fonction pour construire un object
def attachImg(fallback= "", title = "", title_link = "", text = "", image_url = "", color = ""):
    return [
        {
            "fallback": fallback,
            "title": title,
            "title_link": title_link,
            "text": text, 
            "image_url": image_url,
            "color": color
        }
    ]
    


#Fonction pour construire un objet attachement a partir des données de la bdd
#res est le résultat de la requete sur la bdd
#kind est le type de ressource utilisée: Blague, Devinette, Vidéo, Image ou Citation
#le résultat, sous format json peut ensuite etre envoé à slack
  
def makeCake(kind, res):
    title = ''
    text = ''
    image_url = ''
    actions = ''
    
    if kind == "Blague":
        text = res[1]
        text = text.replace('\\n', '\n')
        
    elif kind == "Devinette":
        return [
        {
            "text": res[1],
            "fallback": "You are unable to choose a game",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "game",
                    "text": "Reponse",
                    "type": "button",
                    "value": None,
                    "confirm": {
                        "title": "",
                        "text": res[2],
                        "ok_text": "Je savais !",
                        "dismiss_text": "Je saurais la prochaine"
                    }
                }
            ]
        }
    ]

        
        
    elif kind == "Video":
        title = res[2]
        text = res[1]
        
    elif kind == "Image":
        image_url = res[2]
        if image_url[-2:] == "/r":
            image_url = image_url[-2:] 
        
        title = res[1]
        
        
    elif kind == "Citation":
        title = res[1]
        text = res[2]
        
    
    
    attach = [
            {
            "title": title,
            "text": text, 
            "image_url": image_url,
            "actions" : actions
        }]
        
        
    return attach