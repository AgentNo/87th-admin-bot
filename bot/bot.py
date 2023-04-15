# bot.py
# Main entrypoint for the admin bot.

import os
import discord
import logging
from dotenv import load_dotenv

import utility.strings as strings
import utility.utils as utils

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


# Start logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)


@client.event
async def on_ready():
    log.info(f'{client.user} has connected to the following guilds: ' + ', '.join(guild.name for guild in client.guilds))
    for guild in client.guilds:
        log.info(guild.name)


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(strings.DM_WELCOME_MESSAGE.format(member.name))


# Run the bot
client.run(TOKEN)
