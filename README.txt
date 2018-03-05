1 Start Ngrok.exe
  ngrok http 3000 (3000 is number of port)

2 Get the second forwarding url, starting with https 

3 in https://api.slack.com/apps:
- Event Subscriptions:
	_ Enable Events (ON)
	_ Request URL = url/slack/events

- OAuth & Permission: 
	_ redirect URL = url/slack/events
	_ Add Bot User Event:
		_ message.channels (listen to channels)
		_ reaction_added (listen to reaction)
		_ message.im (listen to private msg)

- Interactive Components:
	- Request url: url/slack/message_actions
	- Options Load URL: url/slack/message_options (for Message Menus)


Completer le doc sur le multi-threading.
Gérer plusieurs users sur un meme channel.
Push git
