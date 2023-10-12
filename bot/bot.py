# bot.py
# Main entrypoint for the admin bot.

from discord.ext.commands import has_role
from discord.ext import commands
from discord.ext.commands import errors
from dotenv import load_dotenv
import discord
import time
import os

import bot_funcs as funcs
import utility.enums as enums
import utility.utils as utility


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')

# Start logger
startTime = time.time()
log = utility.start_logging()

@bot.event
async def on_ready():
    log.info(f'{bot.user} has connected to the following guilds: ' + ', '.join(guild.name for guild in bot.guilds))


@bot.event
async def on_member_join(member):
    await funcs.send_dm_to_new_member(log, member)


@bot.event
async def on_message(message):
    await funcs.check_if_message_has_femboy(message)
    await funcs.check_and_put_signup_reactions(message)
    await bot.process_commands(message)


# !hb - Health command to ensure bot is responsive to commands and currently operational
@bot.command(name="hb",
        help="Simple heartbeat command to ensure bot is up and running",
        brief="Prints bot uptime to the channel"
        )
async def heartbeat_handler(ctx):
    await funcs.heartbeat(ctx, startTime, log)


# !enlist <user> - Will give the user basic Recruit roles.
@bot.command(name="enlist",
        help="Enlist a user. Accepts a single mention of a user as an argument. Can only be successfully invoked by a user with manage roles permission.",
        brief="Enlists a user to the 87th."
        )
@has_role(enums.BOT_USER_ROLE)
async def enlist_member_handler(ctx, user: discord.Member):
    await funcs.enlist_member(ctx, user, log)


# Error handling for !enlist
@enlist_member_handler.error
async def enlist_error(ctx, error):
    log.info(f'Encountered error in !enlist invocation by user {ctx.author.name} ({ctx.author.id}) - {error}')
    if isinstance(error, errors.MissingPermissions) or isinstance(error, errors.MissingRole):
        await ctx.channel.send(f'Oi <@{ctx.author.id}>! You don\'t have permission to do that! :angry:')
    elif isinstance(error, errors.MissingRequiredArgument):
        await ctx.channel.send(f'<@{ctx.author.id}>, you need to specify a user to enlist, like this: \n**!enlist <@user>**')


# !grantrole <type> <user> - Add or remove Merc/Rep/Visitor tags from a user.
@bot.command(name="grantrole",
        help="Add or remove Merc/Rep/Visitor tags. Accepts a single mention of a user as an argument. Can only be successfully invoked by a user with manage roles permission. 'Rep', 'Merc', or 'Visitor' must be defined or else command will fail.",
        brief="Adds or removes Merc, Rep, or Visitor tags on a user."
        )
@has_role(enums.BOT_USER_ROLE)
async def grant_role_handler(ctx, roleType, user: discord.User):
    await funcs.grant_role(ctx, roleType, user, log)


# Error handling for !grantrole
@grant_role_handler.error
async def grant_role_error(ctx, error):
    log.info(f'Encountered error in !grantrole invocation by user {ctx.author.name} ({ctx.author.id}) - {error}')
    if isinstance(error, errors.MissingPermissions) or isinstance(error, errors.MissingRole):
        await ctx.channel.send(f'Oi <@{ctx.author.id}>! You don\'t have permission to do that! :angry:')
    elif isinstance(error, errors.MissingRequiredArgument):
        await ctx.channel.send(f'<@{ctx.author.id}>, you need to specify both a role type and user, like this: \n**!grantrole <merc/rep/visitor> <@user>**')


# !attendance - Take an attendance count and update the Master Doc. User needs to be in a voice channel for this command to work.
@bot.command(name="attend",
        help="Updates the Master Doc's Last Seen column with users currently in the voice channel.",
        brief="Takes an attendance count. Must be used in a voice channel."
        )
@has_role(enums.BOT_USER_ROLE)
async def attend_handler(ctx):
    await funcs.attend(log, ctx)


# Error handling for !attend
@attend_handler.error
async def grant_role_error(ctx, error):
    log.info(f'Encountered error in !attend invocation by user {ctx.author.name} ({ctx.author.id}) - {error}')
    if isinstance(error, errors.MissingPermissions) or isinstance(error, errors.MissingRole):
        await ctx.channel.send(f'Oi <@{ctx.author.id}>! You don\'t have permission to do that! :angry:')
    if isinstance(error, errors.CommandInvokeError):
        await ctx.channel.send(f'<@{ctx.author.id}>, there was an error with that invocation: {error}')
    if isinstance(error, FileNotFoundError):
        await ctx.channel.send(f'<@{ctx.author.id}>, I cannot get the authentication keys for the sheet. Please check the logs or contact Spammy!')


# Run the bot
bot.run(TOKEN)
