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
                log.info(f'Added enlistment role {id} to user {user.id}')
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


# !merc <user> - Will give the user the merc role if they do not have it, otherwise will remove it from them.
@bot.command(name="merc",
        help="Add or remove Merc tags. Accepts a single mention of a user as an argument. Can only be successfully invoked by a user with manage roles permission.",
        brief="Adds or removes the Merc tag on a user."
        )
@has_permissions(manage_roles=True)
async def manage_merc_role(ctx, user: discord.User):
    log.info(f'Merc command triggered by user {ctx.author.id} for {user.id}. Getting merc status...')
    if None != ctx.guild.get_member(user.id).get_role(roles_enums.REGIMENT_ROLE_ID):
        log.info(f'Error running !merc command - user {user.id} is already enlisted in the 87th.')
        await ctx.channel.send(f':x: I can\'t do that <@{ctx.author.id}> - it looks like <@{user.id}> is already enlisted!')
    elif None != ctx.guild.get_member(user.id).get_role(roles_enums.MERC_ROLE_ID):
        log.info(f'{user.id} already has merc tags. Will remove them now...')
        try:
            await ctx.guild.get_member(user.id).remove_roles(ctx.guild.get_role(roles_enums.MERC_ROLE_ID))
            await ctx.channel.send(f'<@{user.id}> no longer has merc tags. Big sadge :frowning:')
        except Exception as e:
            log.info(f'Encountered error when removing merc role - {e}')
            await ctx.channel.send(f':x: Something went wrong - {e}')
    else:
        try:
            # If a user is registering as a merc, we'll also give them the visitor tag for access.
            merc_role = ctx.guild.get_role(roles_enums.MERC_ROLE_ID)
            await ctx.guild.get_member(user.id).add_roles(merc_role)
            log.info(f'Added merc tags to user {user.id} successfully')
            visitor_role = ctx.guild.get_role(roles_enums.VISITOR_ROLE_ID)
            await ctx.guild.get_member(user.id).add_roles(visitor_role)
            log.info(f'Added visitor tags to user {user.id} successfully')
            await ctx.channel.send(f'<@{user.id}> has been enlisted as a mercenary successfully. Welcome! :crossed_swords:')
        except Exception as e:
            await ctx.channel.send(f'Error running command !merc - {e}.')
            log.info(f"Error running command !merc - {e}.")


# Error handling for !merc
@manage_merc_role.error
async def merc_error(ctx, error):
    if isinstance(error, errors.MissingPermissions):
        await ctx.channel.send(f'Oi <@{ctx.author.id}>! You don\'t have permission to do that! :angry:')


# !rep <user> - Will give the user the rep role if they do not have it, otherwise will remove it from them.
@bot.command(name="rep",
        help="Add or remove rep tags. Accepts a single mention of a user as an argument. Can only be successfully invoked by a user with manage roles permission.",
        brief="Adds or removes the Representative tag on a user."
        )
@has_permissions(manage_roles=True)
async def manage_rep_role(ctx, user: discord.User):
    log.info(f'Rep command triggered by user {ctx.author.id} for {user.id}. Getting merc status...')
    if None != ctx.guild.get_member(user.id).get_role(roles_enums.REGIMENT_ROLE_ID):
        log.info(f'Error running !rep command - user {user.id} is already enlisted in the 87th.')
        await ctx.channel.send(f':x: I can\'t do that <@{ctx.author.id}> - it looks like <@{user.id}> is already enlisted!')
    elif None != ctx.guild.get_member(user.id).get_role(roles_enums.REP_ROLE_ID):
        log.info(f'{user.id} already has rep tags. Will remove them now...')
        try:
            await ctx.guild.get_member(user.id).remove_roles(ctx.guild.get_role(roles_enums.REP_ROLE_ID))
            await ctx.channel.send(f'<@{user.id}> no longer has rep tags. Big sadge :frowning:')
        except Exception as e:
            log.info(f'Encountered error when removing rep role - {e}')
            await ctx.channel.send(f':x: Something went wrong - {e}')
    else:
        try:
            # If a user is registering as a rep, we'll also give them the visitor tag for access.
            rep_role = ctx.guild.get_role(roles_enums.REP_ROLE_ID)
            await ctx.guild.get_member(user.id).add_roles(rep_role)
            log.info(f'Added merc tags to user {user.id} successfully')
            visitor_role = ctx.guild.get_role(roles_enums.VISITOR_ROLE_ID)
            await ctx.guild.get_member(user.id).add_roles(visitor_role)
            log.info(f'Added visitor tags to user {user.id} successfully')
            await ctx.channel.send(f'<@{user.id}> is on a diplomatic mission to Alderaan. Welcome! :crossed_swords:')
        except Exception as e:
            await ctx.channel.send(f'Error running command !rep - {e}.')
            log.info(f"Error running command !rep - {e}.")


# Error handling for !merc
@manage_rep_role.error
async def rep_error(ctx, error):
    if isinstance(error, errors.MissingPermissions):
        await ctx.channel.send(f'Oi <@{ctx.author.id}>! You don\'t have permission to do that! :angry:')



# Run the bot
bot.run(TOKEN)
