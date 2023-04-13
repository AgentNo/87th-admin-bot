# utils.py

import os
import discord

def getDevGuild(client):
    return discord.utils.get(client.guilds, name=os.getenv('DISCORD_DEV_GUILD'))


def getProdGuild(client):
    return discord.utils.get(client.guilds, name=os.getenv('DISCORD_PROD_GUILD'))
