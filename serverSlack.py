# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 01:41:43 2018

@author: Administrator
"""

from flask import Flask, request, make_response 
import json
from slackclient import SlackClient
from pyee import EventEmitter
import sys
import platform
import dialogFlow
from threading import Timer,Thread,Event
import datetime
import MYSQLBdd
import time
import boutons


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
convs = {}    


#RTM client to send msgs/, ie Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)

#Overide Conversation object to send messages with slack api
class DialogSlack(dialogFlow.Dialog):
    
    
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
        #"16:00:00"
        # self.randomHour
        if self.last < "22:19:30"  <= date:
            self.state = "waitingHumeur"
            self.sendMSG(message = boutons.button1[0] , attachments = boutons.button1[1] )
        self.last= date
        #self.randomHour = dialogFlow.getRandomhour()
        
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
    def __init__(self, channel, publique,t):
      #dialogFlow.Dialog.__init__(self, channel, publique)
      self.t=t
      self.channel = channelmood
      
    def test(self):        
        date = datetime.datetime.now().strftime('%H:%M:%S')
        #print(date)
        if self.last < "11:00:00" <= date:
              self.sendMSG(message="Mood" , attachments = self.getHumeur("daily"))
        if self.last < "12:00:00" <= date:
              self.sendMSG(message="Mood " , attachments = self.getHumeur("weekly"))
              #time.sleep(5)
        if self.last < "16:00:00" <= date:
              self.sendMSG(message="Mood " , attachments = self.getHumeur("daily"))
              #time.sleep(5)
              

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
        print(message, private, attachments)
        print(0)
        slack_client.api_call("chat.postMessage", channel = self.channel, text=message, attachments=attachments)
  
    
    
    
    
    


       
        
#convs[channelmood] = MoodSlack(channelmood, 1,1)         
#convs[channelmood].start()
mood = MoodSlack(channelmood, 1,1)
mood.start()

#print(convs) 
#convs[channelmood].cancel()




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

def findMemberName(id):
    return slack_client.api_call("users.info", user = id)["user"]["name"]	

if __name__ == "__main__":    
    print("Flask server running on {}".format( PORT))
    print("public access on {}".format( serverURL))
    try :
        app.run(port = PORT)
    finally:
        for i,j in convs.items():
            convs[i].cancel()
        mood.cancel()
        