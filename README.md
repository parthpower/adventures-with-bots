# Adventures with Bots!

This is a tale of adventures writing bots. There is lots of text ahead because it's a story/blog. Maybe not the best tutorial or example out there. 

Do you have suggestions? Did I miss something? Do you have better ideas? open an [issue](https://github.com/parthpower/adventures-with-bots/issues)!

## Why? Why not!

I needed a way to boot up my home server remotely. Expose `ssh` on an always on raspberry pi? nah that sounds too simple. I also wanted some of my friends to start the server without sharing an ssh user or hacking up an [lshell(1)](https://linux.die.net/man/1/lshell) like thing. We already have a `discord` and a `slack` channel so, How about a **BOT**!?

## Plan

- run a bot server on Raspberry Pi (probably in future, something even more tiny like an ESP8266)
- The user sends a message with a secret token aka password.
- The bot reads and checks the token.
- if token matches, send [WOL](https://en.wikipedia.org/wiki/Wake-on-LAN) to the server

## Discord bot [bot-discord.py](./bot-discord.py)

Discord bot is extremely simple! Actually easier than a [flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) server! Well, maybe not.

Googled for ["discord bot python"](https://lmgtfy.com/?q=discord+bot+python) because python is fast to write and I don't care production/extensibility/robustness/speed etc. One can surely achieve those features with python, just that I didn't take those factors into consideration. Looked up here [devdungeon](https://www.devdungeon.com/content/make-discord-bot-python) (which is a bit outdated), and then more at [realpython](https://realpython.com/how-to-make-a-discord-bot-python/), then some [docs](https://discordpy.readthedocs.io/en/latest/) and I wrote this [./bot-discord.py](./bot-discord.py). Not production ready but it works.

## Slack bot [bot-slack.py](./bot-slack.py)

well, this one was a bit tricky. I found a way to send messages which I really didn't care about but reading a message from slack wasn't that simple. They needed me to sping up an HTTP POST handler! on the Internet! A webserver that accessible to the internet! **Woah** right there! 

They deprecated their WebSocket based [RTM API](https://api.slack.com/rtm). They say they still support it with the "classic" type app but I couldn't get the [RTM example](https://github.com/slackapi/python-slackclient#basic-usage-of-the-rtm-client) connecting, it was just stuck and I was in a hurry! I mean, I just need this hack working! How hard can it be? *The famous last words.*

I went to try out classic *Are there any free web services that allow me to tunnel my local server to the internet?* and good old [ngrok](https://ngrok.com/) comes to mind. `ngrok` is no more an independent small project, probably bought by a company or something and now is a fancy looking thing, the good thing is, it's still simple and it just works. I didn't notice this earlier but official slack docs recommend `ngrok` to experiment with apps.

Side Note: In the meantime, I also tried to build an ssh tunnel on a GCP instance which should have just worked but then the monthly 2Gig ingress traffic limit on the free tier. Which should be sufficient but I really didn't want to dedicate my GCP instance for that! Since I already have a legit server at home, I was considering running (Cloudflare DDNS)[https://github.com/parthpower/CloudFlare-DDNS-Client], with [cert-manager](https://cert-manager.io/) on my home [`k3s`](https://k3s.io) cluster. Which was too much for this project, maybe for another project?

Back to slack, Since slack has this `/slash` commands, I didn't bother creating a `message` event listener. Created a POST handler to check for slash command and secret which triggers WOL to my server. Thanks to this [doc](https://api.slack.com/interactivity/slash-commands) it was pretty straight forward. Also, DigitalOcean had this [example](https://www.digitalocean.com/community/tutorials/how-to-write-a-slash-command-with-flask-and-python-3-on-ubuntu-16-04)

It took `ngrok` + `flask` for the slack slash command handler. Except for the complexity of exposing a local webserver, the slack bot isn't any harder than the discord bot. Actually, easier since it doesn't require a slack specific library, and is literally an HTTP POST handler that responds with some JSON.

Exposing a webserver to public internet **safely** isn't free or simple or easy. I am not a professional on edge deployment or whatever it is called, let me know if I'm wrong! [issues](https://github.com/parthpower/adventures-with-bots/issues) or [@parthpower](https://twitter.com/parthpower)

Free options are,
1. Open port 80, 443 on your router, add some DDNS, get certs from LetsEncrypt, try to add some security, and hope nobody attacks.
2. Run-on free tier instances. e.g. GCP/OpenShift/Heroku etc
3. Trust `ngrok` with your "secret" slack data.

Having said that, since the `discord` bot didn't require any open ports, it feels a lot easier than slack bots! I mean, I can even run that form my non-rooted phone!  


## How to run?

### Get Tokens

Get the bot token from Discord and/or verification token from the slack bot.

For discord, check out [realpython](https://realpython.com/how-to-make-a-discord-bot-python/) for step by step guide.

For slack, check out [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-write-a-slash-command-with-flask-and-python-3-on-ubuntu-16-04) for step by step guide

### Create `.env` file

```
DISCORD_TOKEN="<discord bot token>"
SLACK_VERIFICATION_TOKEN="<slack app verfication token>"

BOT_SECRET="<secret message to trigger WOL>"
SERVER_MAC="<mac address to send WOL magic to>"
```

### Install requirements, hopefully in a `virtualenv`

```bash
virtualenv venv
pip install requirements.txt
```

### Discord Bot

```bash
./bot-discord.py
```

### Slack Bot

Install/Setup `ngrok` https://ngrok.com/download

```bash
ngrok http 8080
./bot-slack.py
```

## LICENSE

```
Copyright © 2020 Parth Parikh <parthpower@gmail.com>
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See the COPYING.WTFPL file for more details.
```
