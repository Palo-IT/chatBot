# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 22:06:11 2018

@author: Administrator
"""

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

def attachMood(dates , agrMood):
 
    titre = "humeur des palowan du {} au {}".format(dates[1], dates[0])
    attach =  [
                    {
                            "title": titre,
                            "fields": [
                                    {
                                        "title": "Heureux",
                                        "value": str(agrMood["heureux"]),
                                        "short": "true"
                                    },
                                    
                                    {
                                        "title": "Serein",
                                        "value": str(agrMood["serein"]),
                                        "short": "true"
                                    },
                                    {
                                        "title": "Surpris",
                                        "value": str(agrMood["surpris"]),
                                        "short": "true"
                                    },
                                            
                                    {
                                        "title": "Stressé",
                                        "value": str(agrMood["stressé"]),
                                        "short": "true"
                                    },
                                    {
                                        "title": "En colère",
                                        "value": str(agrMood["en colère"]),
                                        "short": "true"
                                    }
                                ]
                            }
                        ]
    return attach





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
    
    
def makeCake(kind, res):
    title = ''
    text = ''
    image_url = ''
    
    if kind == "Blague":
        text = res[1]
        
    elif kind == "Devinette":
        title = res[1]
        text = res[2]
        
    elif kind == "Video":
        title = res[2]
        text = res[1]
        
    elif kind == "Image":
        image_url = res[2]
        
        if image_url[-2:] == "/r":
             image_url= image_url[-2:]
            
        title = res[1]
        
        
    elif kind == "Citation":
        title = res[1]
        text = res[2]
        
    
    
    attach = [
            {
            "title": title,
            "text": text, 
            "image_url": image_url,
        }]
        
        
    return attach