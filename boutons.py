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
            "fallback": "Disons: Super, génial, moyen, ok, pas terrible, pas bien",
            "callback_id": "humeur_type",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "humeur",
                    "text": " Super :smiley:",
                    "type": "button",                  
                    "value": "super"
                    
                },
                {
                    "name": "humeur",
                    "text": "génial :blush:",
                    "type": "button",
                    "value": "genial"
                },
                {
                    "name": "humeur",
                    "text": "Moyen :flushed:",
                    "type": "button",
                    "value": "moyen"
                },
       
                {
                    "name": "humeur",
                    "text": "Pas terrible :unamused:",
                    "type": "button",
                    "value": "pas terrible"
                 },
                 {
                    "name": "humeur",
                    "text": "Pas bien :weary:",
                    "type": "button",
                    "value": "pas bien"
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



def attachMood():
{
    "attachments": [
        {
            "title": "humeur de la journée",
            "fields": [
                {
                    "title": "Bien",
                    "value": "80 %",
                    "short": "true"
                },
                {
                    "title": "Génial",
                    "value": "10 %",
                    "short": "true"
                },
    {
                    "title": "Pas terrible",
                    "value": "2%",
                    "short": "true"
                },
    {
                    "title": "Pas bien",
                    "value": "2%",
                    "short": "true"
                },
    {
                    "title": "Pas bien",
                    "value": "2%",
                    "short": "true"
                }
            ]
        }
    ]
}



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