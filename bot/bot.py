# bot.py
# Main entrypoint for the admin bot.

from discord.ext.commands import has_role
from discord.ext import commands
from discord.ext.commands import errors
from dotenv import load_dotenv
import discord
import time
import datetime
import os

import bot_funcs as funcs
import utility.enums as enums
from utility.setup_logger import logger 


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')
startTime = time.time()

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to the following guilds: ' + ', '.join(guild.name for guild in bot.guilds))


@bot.event
async def on_member_join(member):
    await funcs.send_dm_to_new_member(member)


@bot.event
async def on_message(message):
    if message.channel.id == 744708888250810459:
        bot_user = await bot.fetch_user(bot.application_id)
        await funcs.add_or_remove_signup_reactions(message, bot_user)
    await bot.process_commands(message)


@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 1172649217567768606:
        await funcs.add_or_remove_gaming_role(bot, payload)


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id == 1172649217567768606:
        await funcs.add_or_remove_gaming_role(bot, payload, remove_unrelated=False)  


# !hb - Health command to ensure bot is responsive to commands and currently operational
@bot.command(name="hb",
        help="Heartbeat command to ensure bot is up and running. Returns the bot's current uptime.",
        brief="Show the bot's uptime"
        )
async def heartbeat_handler(ctx):
    try:
        currentTime = time.time()
        await ctx.channel.send(f"87th Admin Bot is up and running! :heartpulse:\nThis instance has been alive for {datetime.timedelta(seconds=int(currentTime-startTime))}!")
    except Exception as e:
        await ctx.channel.send(f"Error in heartbeat invocation - {e}")


# !enlist <user> - Will give the user basic Recruit roles.
@bot.command(name="enlist",
        help="Enlist a member and grant basic recruit roles. Accepts a single member mention as an argument. Will fail when attempting to enlist a member with the 87th Regiment of Foot role.\nUsage: !enlist @<member>",
        brief="Enlist a member and grant basic recruit roles"
        )
@has_role(enums.BOT_USER_ROLE)
async def enlist_member_handler(ctx, user: discord.Member):
    await funcs.enlist_member(ctx, user)


# Error handling for !enlist
@enlist_member_handler.error
async def enlist_error(ctx, error):
    logger.info(f'Encountered error in !enlist invocation by user {ctx.author.name} ({ctx.author.id}) - {error}')
    if isinstance(error, errors.MissingPermissions) or isinstance(error, errors.MissingRole):
        await ctx.channel.send(f'Oi <@{ctx.author.id}>! You don\'t have permission to do that! :angry:')
    elif isinstance(error, errors.MissingRequiredArgument):
        await ctx.channel.send(f'<@{ctx.author.id}>, you need to specify a user to enlist, like this: \n**!enlist <@user>**')


# !role <type> <user> - Add or remove Merc/Rep/Visitor tags from a user.
@bot.command(name="role",
        help="Add or remove Merc/Rep/Visitor roles. Accepts a single member mention as an argument. Role type ('rep', 'merc', or 'visitor') must be defined or else command will fail. If the user already has the specific role, it will be removed.\nUsage: !grantrole merc/rep/visitor @<member>",
        brief="Adds or removes Merc, Rep, or Visitor roles on a member"
        )
@has_role(enums.BOT_USER_ROLE)
async def grant_role_handler(ctx, roleType, user: discord.User):
    await funcs.grant_role(ctx, roleType, user)


# Error handling for !role
@grant_role_handler.error
async def grant_role_error(ctx, error):
    logger.info(f'Encountered error in !role invocation by user {ctx.author.name} ({ctx.author.id}) - {error}')
    if isinstance(error, errors.MissingPermissions) or isinstance(error, errors.MissingRole):
        await ctx.channel.send(f'Oi <@{ctx.author.id}>! You don\'t have permission to do that! :angry:')
    elif isinstance(error, errors.MissingRequiredArgument):
        await ctx.channel.send(f'<@{ctx.author.id}>, you need to specify both a role type and user, like this: \n**!role <merc/rep/visitor> <@user>**')


# !attendance - Take an attendance count and update the Master Doc. User needs to be in a voice channel for this command to work.
@bot.command(name="attend",
        help="Update the master document's 'Last Seen' column with users currently in the voice channel. Can be used in any text channel the bot has scope to, but the invoker must be present in the voice call.",
        brief="Take an attendance count"
        )
@has_role(enums.BOT_USER_ROLE)
async def attend_handler(ctx):
    await funcs.attend(ctx)


# Error handling for !attend
@attend_handler.error
async def attend_error(ctx, error):
    logger.info(f'Encountered error in !attend invocation by user {ctx.author.name} ({ctx.author.id}) - {error}')
    if isinstance(error, errors.MissingPermissions) or isinstance(error, errors.MissingRole):
        await ctx.channel.send(f'Oi <@{ctx.author.id}>! You don\'t have permission to do that! :angry:')
    if isinstance(error, errors.CommandInvokeError):
        await ctx.channel.send(f'<@{ctx.author.id}>, there was an error with that invocation: {error}')
    if isinstance(error, FileNotFoundError):
        await ctx.channel.send(f'<@{ctx.author.id}>, I cannot get the authentication keys for the sheet. Please check the logs or contact Spammy!')


# Run the bot
bot.run(TOKEN)
