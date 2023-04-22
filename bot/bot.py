# bot.py
# Main entrypoint for the admin bot.

import os
import discord
import random
from discord.ext import commands
from discord.ext.commands import has_permissions, errors
from dotenv import load_dotenv
import time

import utility.strings as strings
import utility.roles as roles_enums
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
    log.info(member.name + " has joined the 87th. Sending welcome message...")
    await member.create_dm()
    await member.dm_channel.send(strings.DM_WELCOME_MESSAGE.format(member.name))
    log.info("Welcome message sent to " + member.name + " successfully.")


@bot.event
async def on_message(message):
    if 'femboy' in message.content and not message.author.bot:
        number = random.random(1,100)
        if number < 3:
            await message.channel.send(f'Spammy is not a femboy <@{message.author.id}>. Please stop spreading fake news.')
    await bot.process_commands(message)


# !hb - Health command to ensure bot is responsive to commands and currently operational
@bot.command(
        name="hb",
        help="Simple heartbeat command to ensure bot is up and running",
        brief="Prints a message back to the channel"
        )
async def heartbeat(ctx):
    try:
        currentTime = time.time()
        log.info("Heartbeat command triggered, sending response...")
        await ctx.channel.send(f"87th Admin Bot is up and running! :heartpulse:\nI have been up for {currentTime - startTime} seconds!")
    except Exception as e:
        log.info(f'Error thrown in !hb - {e}')


# !enlist <user> - Will give the user basic Recruit roles.
@bot.command(name="enlist",
        help="Enlist a user. Accepts a single mention of a user as an argument. Can only be successfully invoked by a user with manage roles permission.",
        brief="Enlists a user to the 87th."
        )
@has_permissions(manage_roles=True)
async def enlist_member(ctx, user: discord.Member):
    log.info(f'Enlist command triggered by user {ctx.author.id} for {user.id}. Attempting to enlist...')
    if None != ctx.guild.get_member(user.id).get_role(roles_enums.REGIMENT_ROLE_ID):
        log.info(f'Error running command - user {user.id} is already enlisted.')
        await ctx.channel.send(f':x: I can\'t do that <@{ctx.author.id}> - it looks like <@{user.id}> is already enlisted!')
    else: 
        if None != ctx.guild.get_member(user.id).get_role(roles_enums.UNASSIGNED_ROLE_ID):
            await ctx.guild.get_member(user.id).remove_roles(ctx.guild.get_role(roles_enums.UNASSIGNED_ROLE_ID)) # Remove the 'Unassigned' role
        for id in roles_enums.ENLISTMENT_ROLES_IDs:
            try:
                role = ctx.guild.get_role(id)
                await ctx.guild.get_member(user.id).add_roles(role)
                log.info(f'Added enlistment role {id} to user {user.id}')
            except Exception as e:
                await ctx.channel.send(f'Error running command !enlist - {e}. Command failed on role {role}, id = {id}')
                log.info(f"Error running command !enlist - {e}. Command failed on role {role}, id = {id}")
        if len(user.display_name) < 19:
            new_nick = f'[87th] Rec. | {user.display_name}'
            await user.edit(nick=new_nick)
            await ctx.channel.send(f'<@{user.id}> has been enlisted successfully. Welcome! :crossed_swords:')
        else:
            await ctx.channel.send(f'<@{user.id}> has been enlisted successfully. Welcome! :crossed_swords:')
            await ctx.channel.send(f'Sorry <@{ctx.author.id}>, I could not change this user\'s name as it is longer than 19 characters :pensive:.')
        log.info(f'{user.id} has been enlisted successfully!')


# Error handling for !enlist
@enlist_member.error
async def enlist_error(ctx, error):
    if isinstance(error, errors.MissingPermissions):
        await ctx.channel.send(f'Oi <@{ctx.author.id}>! You don\'t have permission to do that! :angry:')
    elif isinstance(error, errors.MissingRequiredArgument):
        await ctx.channel.send(f'<@{ctx.author.id}>, you need to specify a user to enlist, like this: \n**!enlist <@user>**')


# !grantrole <type> <user> - Add or remove Merc/Rep/Visitor tags from a user.
@bot.command(name="grantrole",
        help="Add or remove Merc/Rep/Visitor tags. Accepts a single mention of a user as an argument. Can only be successfully invoked by a user with manage roles permission. 'Rep', 'Merc', or 'Visitor' must be defined or else command will fail.",
        brief="Adds or removes Merc, Rep, or Visitor tags on a user."
        )
@has_permissions(manage_roles=True)
async def grant_role(ctx, roleType, user: discord.User):
    log.info(f'grantrole command triggered by user {ctx.author.id} for {user.id} to change {roleType} tags. Checking status of user...')
    if None != ctx.guild.get_member(user.id).get_role(roles_enums.REGIMENT_ROLE_ID):
        log.info(f'Error running !grantrole command - user {user.id} is already enlisted in the 87th.')
        await ctx.channel.send(f':x: I can\'t do that <@{ctx.author.id}> - it looks like <@{user.id}> is already enlisted!')
        return
    else:
        if str(roleType).lower() not in roles_enums.GRANTROLES_DICT.keys():
            await ctx.channel.send(f"<@{ctx.author.id}>, I don't recognise that role :face_with_monocle:. You can use **merc**, **rep**, or **visitor** as valid options.")
            return
        
        if None != ctx.guild.get_member(user.id).get_role(roles_enums.UNASSIGNED_ROLE_ID):
            log.info('User has Unassigned role, removing now...')
            await ctx.guild.get_member(user.id).remove_roles(ctx.guild.get_role(roles_enums.UNASSIGNED_ROLE_ID)) # Remove the 'Unassigned' role

        roleToManage = roles_enums.GRANTROLES_DICT[str(roleType).lower()]
        if None != ctx.guild.get_member(user.id).get_role(roleToManage):
            log.info(f'{user.id} already has {roleType} tags. Will remove them now...')
            try:
                await ctx.guild.get_member(user.id).remove_roles(ctx.guild.get_role(roleToManage))
                await ctx.channel.send(f'<@{user.id}> no longer has {roleType} tags. Big sadge :frowning:')
            except Exception as e:
                log.info(f'Encountered error when removing {roleType} role - {e}')
                await ctx.channel.send(f':x: Something went wrong - {e}')
        else:
            try:
                # If a user is registering as a merc or rep, we'll also give them the visitor tag for access.
                role = ctx.guild.get_role(roleToManage)
                await ctx.guild.get_member(user.id).add_roles(role)
                log.info(f'Added {roleType} tags to user {user.id} successfully')
                if roleType == "merc" or roleType == "rep":
                    visitor_role = ctx.guild.get_role(roles_enums.VISITOR_ROLE_ID)
                    await ctx.guild.get_member(user.id).add_roles(visitor_role)
                    log.info(f'Added visitor tags to user {user.id} successfully')
                await ctx.channel.send(f'<@{user.id}> has been enlisted as a {roleType} successfully. Welcome! :crossed_swords:')
            except Exception as e:
                await ctx.channel.send(f'Error running command !grantrole - {e}.')
                log.info(f"Error running command !grantrole - {e}.")



# Error handling for !grantrole
@grant_role.error
async def grant_role_error(ctx, error):
    if isinstance(error, errors.MissingPermissions):
        await ctx.channel.send(f'Oi <@{ctx.author.id}>! You don\'t have permission to do that! :angry:')
    elif isinstance(error, errors.MissingRequiredArgument):
        await ctx.channel.send(f'<@{ctx.author.id}>, you need to specify both a role type and user, like this: \n**!grantrole <merc/rep/visitor> <@user>**')


# Run the bot
bot.run(TOKEN)
