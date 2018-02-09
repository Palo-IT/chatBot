# SLACK_BOT_TOKEN = xoxb-294373068482-1wMQ7fBxfCRqGPZJYUpILObH
#https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
import os
import time
import re
import random as rd
from slackclient import SlackClient
import pandas as pd

#With our dependencies imported we can use them to obtain the environment variable values and then instantiate the Slack client.

# instantiate Slack client
#slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN
slack_client = SlackClient("xoxb-294373068482-1wMQ7fBxfCRqGPZJYUpILObH")
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
USER_CMD_DELAY = 5 # gives 5 seconds to user to give commands to the bot
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+)>(.*)"
MENTION_REGEX2 = "[a-zA-Z]"
PAPA = "U8M8S71FB"



#The Slack client connects to the Slack RTM API. Once it's connected, it calls a Web API method (auth.test) to find Starter Bot's user ID.

#Each bot user has a user ID for each workspace the Slack App is installed within. Storing this user ID will help the program understand if someone has mentioned the bot in a message.

#Next, the program enters an infinite loop, where each time the loop runs the client recieves any events that arrived from Slack's RTM API. Notice that before the loop ends, the program pauses for one second so that it doesn't loop too fast and waste your CPU time.

#For each event that is read, the parse_bot_commands() function determines if the event contains a command for Starter Bot. If it does, then command will contain a value and the handle_command() function determines what to do with the command.

#We've laid the groundwork for processing Slack events and calling Slack methods in the program. Next, add three new functions above the previous snippet to complete handling commands:


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:        
            message = parse_direct_mention(event["text"])
            #print(user_id)
            return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    return message_text



def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    #default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)
    default_response = command

	
    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


#The parse_bot_commands() function takes events from Slack and determines if they are commands directed at Starter Bot. There are many event types that our bot will encounter, but to find commands we only want to consider message events. Message events also have subtypes, but the commands we want to find won't have any subtype defined. The function filters out uninteresting events by checking these properties. Now we know the event represents a message with some text, but we want to find out if Starter Bot is being mentioned in the text. The parse_direct_mention() function will figure out of the message text starts with a mention, and then we compare that to the user ID we stored earlier for Starter Bot. If they are the same, then we know this is a bot command, and return the command text with the channel ID.

#The parse_direct_mentions() function uses a regular expression to determine if a user is being mentioned at the beginning of the message. It returns the user ID and the remaining message (and None, None if no mention was found).


#find channel
def find_channel():
    channels = slack_client.api_call("channels.list")["channels"]
    for channel in channels:
        #if channel["name"] == "starterbot-test":
        if channel["name"] == "test":		
            print("channel found:" + channel["id"])
            return channel["id"]
		


#start sequence 0
def seq_start(channel):
        slack_client.api_call("chat.postMessage", channel = channel, text="Bonjour tout le monde! :robot_face:")
        slack_client.api_call("chat.postMessage", channel = channel, text="J'ai très envie de parler :smile:")		
        slack_client.api_call("chat.postMessage", channel = channel, text="Parlez moi en commancant votre message par @starterbot :smile:")	

def find_activ_members(channel, starterbot_id):
        slack_client.api_call("chat.postMessage", channel = channel, text="Est ce que quelqu'un est là ???")
        print(members = slack_client.api_call("conversations.members", channel = channel)["members"])
        members.remove(str(starterbot_id))
        liste = ''
        for member in members:
            name = findMemberName(member)
            liste += "@"+ name + " ? "
        slack_client.api_call("chat.postMessage", channel = channel, text=liste)
        return 1

def findMemberName(id):

    return slack_client.api_call("users.info", user = id)["user"]["name"]		

def start_log():
        #log_channel = slack_client.api_call("im.open", user = PAPA, return_im = "true")
        slack_client.api_call("chat.postMessage", channel = PAPA, text = "hey Papa! Watch me working :upside_down_face:")

def textProcessing(text):
	text =  text.lower().replace("!" ," !").replace("?" ," ?")
	
	text = text.replace("é","e").replace("è","e").replace("ë","e").replace("ê","e").replace("à",
        "a").replace("â" , "a").replace("ô","o").replace("î","i").replace("ï","i").replace("ù","u")
	
	return text

def say(channel , text):
	return slack_client.api_call("chat.postMessage", channel = channel, text = text )
	
def chooseScenario(dicoScenar, *args):
    nbRandom = rd.random()
    print(nbRandom, dicoScenar)
    weightCum = 0
    for scenar, weight in dicoScenar.items():
        weightCum += weight
        if nbRandom < weightCum:
              return  scenar  #(*args)
		
def waitAnswer(channel):
    while True:
        command, channel = parse_bot_commands(slack_client.rtm_read())
        if command and channel == channel:
            return command
        print("waiting")	
        time.sleep(RTM_READ_DELAY)
		
def scenarioCava(channel):
    say(channel , "Ca va ?")
    command = waitAnswer(channel)
    command = textProcessing(command)
    if  "oui" in command:
        say(channel , "Génial, continue commme ça :grinning:")

    elif  "non" in command:
        say(channel , "Ne t'inquiètes pas, ca va aller :smile:")

    else:
        say(channel , ":robot_face: hum...je n'ai pas compris :face_with_rolling_eyes:")
        scenarioCava(channel)



def humeurDuJour(channel):

    slack_client.api_call("chat.postMessage", channel = channel, text =	"Comment décrirais tu ton humeur du jour?")
    slack_client.api_call("chat.postMessage", channel = channel, text =	"Disons: Super, génial, moyen, ok, pas terrible, pas bien")
    command = waitAnswer(channel).split()
    user_name = findMemberName(slack_client.api_call("channels.info", channel = channel)["channel"]["latest"]["user"])
    user_id = slack_client.api_call("channels.info", channel = channel)["channel"]["latest"]['user']
    print(user_id)
    print(user_name)
    ligne = [user_id , user_name]
    humeur = 1.5
	
    if  "super" in command or  "génial" in command:
        slack_client.api_call("chat.postMessage", channel = channel, 
        text =	"Ok, c'est parti pour une super journée alors :joy:")
        humeur = 4
        ligne.append(humeur)
    elif "moyen" in command or  'ok' in command:
        slack_client.api_call("chat.postMessage", channel = channel,
        text =	"Courage! Ca va bien se passer :grinning:")
        humeur = 3
        ligne.append(humeur)    
    elif "pas terrible" in command:
        slack_client.api_call("chat.postMessage", channel = channel,
        text =	"Courage! Ca va bien se passer :relieved:")
        humeur = 2
        ligne.append(humeur)
    elif  "mal" in command or  "pas bien" in command:
        slack_client.api_call("chat.postMessage", channel = channel,
        text =	"Je suis là si tu as besoin de parler :hushed:")
        humeur = 1
        ligne.append(humeur)
    else: 
        slack_client.api_call("chat.postMessage", channel = channel,
        text =	":robot_face: hum...je n'ai pas compris :face_with_rolling_eyes:")		
        humeurDuJour(channel)        
        
    slack_client.api_call("chat.postMessage", channel = channel, text =	"Quelle est l'intensité de ton humeur ?")
    slack_client.api_call("chat.postMessage", channel = channel, text =	"Disons: grande, moyenne, faible")
    command = waitAnswer(channel).split()
    user = findMemberName(slack_client.api_call("channels.info", channel = channel)["channel"]["latest"]["user"])
    print(slack_client.api_call("channels.info", channel = channel)["channel"]["latest"])
    intensite = 1.5
	
    if  "grande" in command:
        slack_client.api_call("chat.postMessage", channel = channel, 
        text =	"Merci pour ta réponse")
        intensite = 3
        ligne.append(intensite)

    elif "moyenne" in command:
        slack_client.api_call("chat.postMessage", channel = channel,
        text =	"Merci pour ta réponse  :grinning:")
        intensite = 2
        ligne.append(intensite)

    elif "faible" in command:
        slack_client.api_call("chat.postMessage", channel = channel,
        text =	"merci pour ta réponse")
        intensite = 1
        ligne.append(intensite)


    else: 
        slack_client.api_call("chat.postMessage", channel = channel,
        text =	":robot_face: hum...je n'ai pas compris :face_with_rolling_eyes:")		
        humeurDuJour(channel)
        
    
    slack_client.api_call("chat.postMessage", channel = channel, text =	"Peux-tu m'expliquer pourquoi ?")
    command = waitAnswer(channel).split()
    ligne.append(command)   
    say(channel , "ok compris :grinning:")
        #print(user,humeur)
    if len(ligne) == 5 :
         df_humeur = pd.read_csv('data_humeur.csv' , sep=';')
         print(list(df_humeur))
         df_tmp = pd.DataFrame([ligne] , columns = list(df_humeur))
         df_humeur = df_humeur.append(df_tmp)
         df_humeur.to_csv('data_humeur.csv' , sep = ';' , index = False)
         print(df_humeur)

def find_last(channel):
    print(slack_client.api_call("channels.info", channel = channel)["channel"]["latest"])
    return findMemberName(slack_client.api_call("channels.info", channel = channel)["channel"]["latest"]["user"])

	
def devinette(channel):
    data = pd.read_csv('devinettes.csv' , sep=';')
    ligneRandom = rd.randint(0, data.shape[0]-1)
    devinette = data.iloc[ligneRandom]['Devinettes']
    reponse = data.iloc[ligneRandom]['Reponses']
    say(channel , 'Une petite devinette pour te mettre en jambe aujourd''hui ?' )
    command = waitAnswer(channel)
    command = textProcessing(command)
    if 'oui' in command:
        say (channel , 'Tres bien, je te propose celle-ci :' + devinette + ':/!\ réfléchis bien tu as le droit qu''à un seul essai !' )
        command = waitAnswer(channel)
        if reponse in command:
            say(channel , 'Well done !, tu es très fort ')
        else:
            say(channel , 'Dommage, la réponse était:' + reponse )
    elif  "non" in command:
        say(channel , "Très bien on se reparle bientôt alors")
    else:
        say(channel , ":robot_face: hum...je n'ai pas compris :face_with_rolling_eyes:")   
        devinette(channel)
    
		
#The code instantiates the SlackClient client with our SLACK_BOT_TOKEN exported as an environment variable. It also declares a variable we can use to store the Slack user ID of our Starter Bot. A few constants are also declared, and each of them will be explained as they are used in the code that follows.

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")	
		
		#write log:
        start_log() 
		
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
		
		#find the channel
        channel = find_channel()
        #Start conversation
        #seq_start(channel)
        #find_activ_members(channel, starterbot_id)		
       # humeurDuJour(channel)
        #scenarios = {devinette(channel) :0 ,  scenarioCava(channel) :0.15 , humeurDuJour(channel) :0 }
        #while True:
        {humeurDuJour(channel) :15 , devinette(channel) : 0 }
        
        
        
        #        nnel = parse_bot_commands(slack_client.rtm_read())
        #    if command:
        #        handle_command(command, channel)
        #    time.sleep(RTM_USER_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")