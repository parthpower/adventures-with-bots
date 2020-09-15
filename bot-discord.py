#!/usr/bin/env python

import discord
import os
from dotenv import load_dotenv
from backend import do_secret_job

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
BOT_SECRET = os.getenv('BOT_SECRET')

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!mc'):
        if message.content == '!mc {}'.format(BOT_SECRET):
            print('got secret message from {0.author}'.format(message))
            await message.delete()
            do_secret_job()
            msg = '{0.author.mention} started the server!'.format(message)
            await message.channel.send(msg)
        msg = 'Hi! this is {0.author.mention}'.format(message)
        await message.channel.send(msg)

@client.event
async def on_ready():
    print("Logged in as ")
    print(client.user.name)
    print(client.user.id)

client.run(TOKEN)
