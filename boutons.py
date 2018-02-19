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
            "callback_id": "wopr_game",
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
