# bot.py
# Main entrypoint for the admin bot.

import os
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, errors
import logging
from dotenv import load_dotenv

import utility.strings as strings
import utility.roles as roles_enums

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
    log.info(member.name + " has joined the 87th. Sending welcome message...")
    await member.create_dm()
    await member.dm_channel.send(strings.DM_WELCOME_MESSAGE.format(member.name))
    log.info("Welcome message sent to " + member.name + " successfully.")


@bot.event
async def on_message(message):
    await bot.process_commands(message)


# !ping - Health command to ensure bot is responsive to commands and currently operational
@bot.command(
        name="hb",
        help="Simple heartbeat command to ensure bot is up and running",
        brief="Prints a message back to the channel"
        )
async def ping(ctx):
    try:
        log.info("Heartbeat command triggered, sending response...")
        await ctx.channel.send("87th Admin Bot is up and running! :heartpulse:")
    except Exception as e:
        log.info(f'Error thrown in !hb - {e}')


# !enlist <user> - Will give the user basic Recruit roles.
@bot.command(name="enlist",
        help="Enlist a user. Accepts a single mention of a user as an argument. Can only be successfully invoked by a user with manage roles permission.",
        brief="Enlists a user to the 87th."
        )
@has_permissions(manage_roles=True)
async def enlist_member(ctx, user: discord.User):
    log.info(f'Enlist command triggered by user {ctx.author.id} for {user.id}. Attempting to enlist...')
    if None != ctx.guild.get_member(user.id).get_role(roles_enums.REGIMENT_ROLE_ID):
            log.info(f'Error running command - user {user.id} is already enlisted.')
            await ctx.channel.send(f':x: I can\'t do that <@{ctx.author.id}> - it looks like <@{user.id}> is already enlisted!')
    else: 
        await ctx.guild.get_member(user.id).remove_roles(ctx.guild.get_role(roles_enums.UNASSIGNED_ROLE_ID)) # Remove the 'Unassigned' role
        for id in roles_enums.ENLISTMENT_ROLES_IDs:
            try:
                role = ctx.guild.get_role(id)
                await ctx.guild.get_member(user.id).add_roles(role)
                log.info(f'Added role {id} to user {user.id}')
            except Exception as e:
                await ctx.channel.send(f'Error running command !enlist - {e}. Command failed on role {role}, id = {id}')
                log.info(f"Error running command !enlist - {e}. Command failed on role {role}, id = {id}")
        await ctx.channel.send(f'<@{user.id}> has been enlisted successfully. Welcome! :crossed_swords:')
        log.info(f'{user.id} has been enlisted successfully!')


# Error handling for !enlist
@enlist_member.error
async def enlist_error(ctx, error):
    if isinstance(error, errors.MissingPermissions):
        await ctx.channel.send(f'Oi <@{ctx.author.id}>! You don\'t have permission to do that! :angry:')


# Run the bot
bot.run(TOKEN)
