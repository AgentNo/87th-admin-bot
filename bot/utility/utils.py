# utils.py

import os
import discord

def getDevGuild(bot):
    return discord.utils.get(bot.guilds, name=os.getenv('DISCORD_DEV_GUILD'))


def getProdGuild(bot):
    return discord.utils.get(bot.guilds, name=os.getenv('DISCORD_PROD_GUILD'))
