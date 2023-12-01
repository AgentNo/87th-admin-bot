# utils.py

import os
import discord

def getProdGuild(bot):
    return discord.utils.get(bot.guilds, name=os.getenv('DISCORD_PROD_GUILD'))
