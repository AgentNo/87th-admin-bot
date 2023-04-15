# bot.py
# Main entrypoint for the admin bot.

import os
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv

import utility.strings as strings
import utility.utils as utils

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')


# Start logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)


@bot.event
async def on_ready():
    log.info(f'{bot.user} has connected to the following guilds: ' + ', '.join(guild.name for guild in bot.guilds))


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(strings.DM_WELCOME_MESSAGE.format(member.name))


# !ping - Health command to ensure bot is responsive to commands and currently operational
@bot.command(name="heartbeat")
async def ping(ctx):
    await ctx.channel.send("87th Admin Bot is up and running!")


# !enlist <user> - Will give the user basic Recruit roles,
@bot.command(name="enlist")
async def enlist_member(ctx, *args):
    response = ""
    for arg in args:
        response = response + " " + arg

    await ctx.channel.send(response)


# Run the bot
bot.run(TOKEN)
