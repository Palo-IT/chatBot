        # -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 01:41:43 2018

@author: Administrator
"""

#Ce fichier gère la partie serveur du programme
#Il gère donc la partie Flask qui écoute les informations provenant de l'application Slack
#Il transmet les informations recus à la partie Chatbot (dialogFlow) et renvoie les messages sur les channels Slack


from flask import Flask, request, make_response 
import json
from slackclient import SlackClient
from pyee import EventEmitter
import sys
import platform
import dialogFlow
from threading import Timer
import boutons
import datetime


#VARS
#get the tokens to get access to Slack, port number and public url to access the server
for line in open("tokens.txt", "r").readlines():
    if "SLACK_VERIFICATION_TOKEN =" in line:
        SLACK_VERIFICATION_TOKEN = line[line.index('='):][1:].replace("\n","")
    if "SLACK_BOT_TOKEN =" in line:
        SLACK_BOT_TOKEN = line[line.index('='):][1:].replace("\n","")       
    if "serverURL" in line:
        serverURL = line[line.index('='):][1:].replace("\n","")
    if "serverPortNumber" in line:
        PORT = int(line[line.index('='):][1:].replace("\n",""))
    if "channelmood" in line:
        channelmood = line[line.index('='):][1:].replace("\n","")

app = Flask(__name__)
#dictionnaire stockant les différents channels que le bot écoute
#le numéro du channel (voir url du channel sur Slack) correspond à la key du dictionnaire, l'item correspondant est un pointeur vers un objet
# de classe Conversation (voir le fichier dialogFlow).
convs = {}    


#RTM client to send msgs/, ie Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)


class DialogSlack(dialogFlow.Dialog):

#Overide Conversation object to send messages with slack api
#Permet de Plus l'envoi automatique de la demande d'humeur a une  certaine aléatoire dans la jounée    
    
    
    def handle_function(self):
      self.test()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()
      
      
    def start(self):
      self.last = datetime.datetime.now().strftime('%H:%M:%S')
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()


    def cancel(self):
      self.thread.cancel()     
    
    def test(self):      
                
        date = datetime.datetime.now().strftime('%H:%M:%S') 
        
        if (self.last < self.randomHour <= date) and isWeekDay() and self.asked == 0: #genere la demande d'humeur de maniere aleatoire dans la tranche horaire [9:00-14h00]
            self.state = "waitingHumeur"
            self.sendMSG(message = boutons.button1[0] , attachments = boutons.button1[1] )
            
            
        if self.last < "00:00:00" <= date : # a minuit tous les jours les variable decisionnel en lien avec le mood sont remise a 0 
            self.asked = 0
            self.humeur = 0
            self.state = None
        self.last= date
       
        return

    
        
    def sendMSG(self, message = None, attachments = None, private = 0,  user= None):
        if message != None:
            if private:
                slack_client.api_call("chat.postEphemeral", channel = self.channel, text=message, attachments=attachments, user= user)
            else:
                slack_client.api_call("chat.postMessage", channel = self.channel, text=message, attachments=attachments)
        else :
            return 




class MoodSlack(dialogFlow.Dialog):
    #class permettant l'affichage du Mood des palowans a 11h et 16h pour la journée et a  12h pour la semaine (7jours)
    #channelmood defini dans le token       
    def __init__(self, channel, publique,t):
      self.t=t
      self.channel = channelmood
      
    def test(self):        
        date = datetime.datetime.now().strftime('%H:%M:%S')

        if (self.last < "11:00:00" <= date )and isWeekDay():
            
              self.sendMSG(message="Mood" , attachments = self.getHumeur("daily"))
              
        if (self.last < "12:00:00" <= date )and isWeekDay():
            
              self.sendMSG(message="Mood " , attachments = self.getHumeur("weekly"))

        if (self.last < "16:00:00" <= date )and isWeekDay():
            
              self.sendMSG(message="Mood " , attachments = self.getHumeur("daily"))              

        self.last = date
        return        
      
    def handle_function(self):
      self.test()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()
      
    def start(self):
      self.last = datetime.datetime.now().strftime('%H:%M:%S')
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

    def cancel(self):
      self.thread.cancel()     

    def sendMSG(self, message = '', attachments = None, private = 0,  user= None):
 
        slack_client.api_call("chat.postMessage", channel = self.channel, text=message, attachments=attachments)
  
    
#Initialisation de la classe 
mood = MoodSlack(channelmood, 1,1)
mood.start()



#For handling buttons clicked
@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])
    handleIncoming(form_json)
    return ""



#for listening for messages
@app.route("/slack/events", methods=["POST"])
def listenerMSG():
    
    def get_package_info():
        client_name = __name__.split('.')[0]
        client_version = '1.1.0'
        # Collect the package info, Python version and OS version.
        package_info = {
                "client": "{0}/{1}".format(client_name, client_version),
                "python": "Python/{v.major}.{v.minor}.{v.micro}".format(v=sys.version_info),
                "system": "{0}/{1}".format(platform.system(), platform.release())
            }
        # Concatenate and format the user-agent string to be passed into request headers
        ua_string = []
        for key, val in package_info.items():
            ua_string.append(val)
        return " ".join(ua_string)
    
    emitter = EventEmitter()
    
    # If a GET request is made, return 404.
    if request.method == 'GET':
        return make_response("These are not the slackbots you're looking for.", 404)

    event_data = json.loads(request.data.decode('utf-8'))
    
     # Echo the URL verification challenge code
    if "challenge" in event_data:
         return make_response(event_data.get("challenge"), 200, {"content_type": "application/json"})
    
    # Verify the request token
    request_token = event_data.get("token")
    if SLACK_VERIFICATION_TOKEN != request_token:
        emitter.emit('error', 'invalid verification token')
        return make_response("Request contains invalid Slack verification token", 403)

     # Parse the Event payload and emit the event to the event listener
    if "event" in event_data:       
        emitter.emit(event_data["event"]["type"], event_data)
        response = make_response("", 200)
        response.headers['X-Slack-Powered-By'] = get_package_info()
        handleIncoming(event_data)

    return "OK"


def handleIncoming(event_data):
    #let's get the json informations from slack, identify type of event and build a short json info to pass to bot
    event  = {"type":"None"}
    channel = event_data.get("channel")
    
    if "event" in event_data:
        #check if event is message from a user:
        if event_data["event"]["type"] == "message":
            if event_data["event"].get("subtype") is None:
                #print(event_data)
                event = {
                        "type":"message",
                        "author":event_data['event']['user'],
                        "text":event_data['event']['text'],
                        "time":event_data['event']['ts']
                        }
                channel = event_data['event']['channel']
    #check if event is button clicked
    if "actions" in event_data:
        event = {
                "type":"buttonClicked",
                "buttonId":event_data['callback_id'],
                "value":event_data["actions"][0]["value"],
                "author":event_data['user']['id'],
                "time":event_data['message_ts']
                }
        channel = event_data['channel']['id']

    
    if channel == None or event['type'] == 'None':
        return 'ok'
    
    print("event")

    if channel not in convs.keys():
        isPublic = int(privateOrNot(channel))
        convs[channel] = DialogSlack(channel, isPublic , 1)
        convs[channel].start()
        print("creation d'un Thread")
            
        

    (message, attachments , private, author) = convs[channel].incoming(event)
    convs[channel].sendMSG(message, attachments , private, author )   
    

    return 'ok'    

#Donne la liste de tout les channels utilisé par le user exepté ceux qui sont dans l onglet app
def privateOrNot(channel):
    listeChannel = [channel["id"] for channel in slack_client.api_call("channels.list")["channels"]]
    if channel in listeChannel:
        return True
    return False

#Find the Slack name of a user, given its pseudo
def findMemberName(id):
    return slack_client.api_call("users.info", user = id)["user"]["name"]	


def isWeekDay():
    weekno = datetime.datetime.today().weekday()
    if weekno<5:
        return True   
    else:
        return False
        
        
        
if __name__ == "__main__":    
    print("Flask server running on {}".format( PORT))
    print("public access on {}".format( serverURL))
    try :
        app.run(port = PORT)
    finally:
        for i in convs:
            convs[i].cancel()
        mood.cancel()
        