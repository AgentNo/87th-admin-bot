# utils.py

import os
import discord
import logging


def getProdGuild(bot):
    return discord.utils.get(bot.guilds, name=os.getenv('DISCORD_PROD_GUILD'))

# Sets up and returns a logging object
def start_logging():
    log = logging.getLogger()
    log.setLevel('INFO')
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    log.addHandler(handler)
    return log
