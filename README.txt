---l'équipe TAM-EISTI proudly presents TAM -------------

**** Notice d'utilisation     **************************
1. A installer depuis internet:
nodejs
mysql (pour mac uniquement)

2. pip install (a partir du cmd ou terminal)
slackclient
flask
pyee
mysql_connector
datetime
pandas
tkinter

3. npm install
npm install -g localtunnel

4. pour generer l'url (dans le cmd ou terminal):
lt --port 3000 --subdomain chatbot


5. remplacer les urls sur https://api.slack.com/apps (normalement c'est deja fait) 
(pour pouvoir changer les urls il faut faire parti des collaborateurs de l'app)

Dans les rubriques :
_ Interactive Components > Request URL
_ OAuth & Permissions > Redirect URLs
_ Event Subscriptions > Request URL
Remplacer les urls par:
https://chatbot.localtunnel.me/slack/events



*******  Pour utiliser avec Ngrok (serveur en local) *************
0 Clone repository
1 Start Ngrok.exe
  ngrok http 3000 (3000 is number of port)
  Get the second forwarding url, starting with https (let's call it Url)

2 Start serverSlack.py (sur cmd : python serverSlack.py )

3 in https://api.slack.com/apps:
- Event Subscriptions:
	_ Enable Events (ON)
	_ Request URL = Url/slack/events (ex: https/sfsdf46.ngrok.io/slack/events)

- OAuth & Permission: 
	_ redirect URL = Url/slack/events
	_ Add Bot User Event:
		_ message.channels (listen to channels)
		_ reaction_added (listen to reaction)
		_ message.im (listen to private msg)

- Interactive Components:
	- Request url: Url/slack/message_actions
	- Options Load URL: Url/slack/message_options (for Message Menus)

