# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 01:41:43 2018

@author: Administrator
"""

from flask import Flask, request, make_response  #,Response
import json
from slackclient import SlackClient
from pyee import EventEmitter
import sys
import platform
import dialogFlow
import datetime


#VARS
#get the tokens to get access to Slack
for line in open("tokens.txt", "r").readlines():
    if "SLACK_VERIFICATION_TOKEN =" in line:
        SLACK_VERIFICATION_TOKEN = line[line.index('='):][1:].replace("\n","")
    if "SLACK_BOT_TOKEN =" in line:
        SLACK_BOT_TOKEN = line[line.index('='):][1:].replace("\n","")
        
PORT = 3000
app = Flask(__name__)    

#Functions
#RTM client to send msgs, ie Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)

def sendMSG(channel, text, attachments = None):
    if attachments == None:
        slack_client.api_call("chat.postMessage", channel = channel, text=text)
    else:
        slack_client.api_call("chat.postMessage", channel = channel, text=text, attachments=attachments)

"""
#For rolling menu, precise options in menu_options (format dict or JSON)
@app.route("/slack/message_options", methods=["POST"])
def message_options(menu_options):
    # Parse the request payload
    form_json = json.loads(request.form["payload"])
    return Response(json.dumps(menu_options), mimetype='application/json')
"""

#For handling buttons clicked
@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])
    handle_action(form_json)
    return None


def handle_action(action_data):
    # Check to see what the user's selection was and update the message
    print(action_data)
    #idButton = action_data['actions'][0]["name"]
    choice = action_data["actions"][0]["value"]
    author = action_data['user']['id']
    channel = action_data['channel']['id']
    time =  action_data['message_ts']   
    (answer, attachments) = convs[channel].newMSG(choice, processTime(time), findMemberName(author))
    print(answer, attachments)
    sendMSG(channel, answer, attachments)    

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
        if event_data["event"]["type"] == "message":
            if event_data["event"].get("subtype") is None:
                handle_event(event_data)
    return "OK"

def handle_event(event_data):
    #print(event_data)
    author = event_data['event']['user']
    message = event_data['event']['text']
    channel = event_data['event']['channel']
    time = event_data['event']['ts']
    """"""
    
    if channel not in convs.keys():
        isPublic = int(privateOrNot(channel))
        convs[channel] = dialogFlow.Dialog(channel, isPublic)
    (answer, attachments) = convs[channel].newMSG(message, processTime(time), findMemberName(author))
    #print(answer, attachments)
    #(answer, attachments) = convs[channel].chooseAnswer()
    sendMSG(channel, answer, attachments)    
    return 1


#Donne la liste de tout les channels utilisé par le user exepté ceux qui sont dans l onglet app
def privateOrNot(channel):
    listeChannel = [channel["id"] for channel in slack_client.api_call("channels.list")["channels"]]
    if channel in listeChannel:
        return True
    return False

def findMemberName(id):
    return slack_client.api_call("users.info", user = id)["user"]["name"]	

def processTime(ts):
    return datetime.datetime.fromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    print("Flask server running on {}".format(PORT))
    app.run(port = PORT)
    convs = {}
    #print(datetime.datetime.now)