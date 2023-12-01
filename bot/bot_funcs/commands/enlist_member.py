# enlist_member.py
# Enlists a member in the 87th - gives them the basic 'Recruit' role set. Will fail on enlisted members.

import discord
import utility.enums as enums
import utility.strings as strings
from utility.setup_logger import logger

async def enlist_member(ctx, user: discord.Member):
    logger.info(f'Enlist command triggered by user {ctx.author.name} ({ctx.author.id}) for {user.display_name} ({user.id})')
    if None != ctx.guild.get_member(user.id).get_role(enums.GRANTABLE_ROLES["regiment"]):
        await ctx.channel.send(f':x: I can\'t do that <@{ctx.author.id}> - it looks like <@{user.id}> is already enlisted!')
    else: 
        await ctx.channel.send(f"Enlisting user, sit tight...")
        if None != ctx.guild.get_member(user.id).get_role(enums.GRANTABLE_ROLES["unassigned"]):
            await ctx.guild.get_member(user.id).remove_roles(ctx.guild.get_role(enums.GRANTABLE_ROLES["unassigned"])) # Remove the 'Unassigned' role
        for id in enums.GRANTABLE_ROLES["enlistment"]:
            try:
                role = ctx.guild.get_role(id)
                await ctx.guild.get_member(user.id).add_roles(role)
            except Exception as e:
                await ctx.channel.send(f'Error running command !enlist - {e}. Command failed on role {role}, id = {id}')
        if len(user.display_name) < 19:
            await user.edit(nick=f'[87th] Rec. | {user.display_name}')
            await ctx.channel.send(strings.ENLIST_SUCCESS_MESSAGE.format(user.id))
        else:
            await ctx.channel.send(strings.ENLIST_SUCCESS_MESSAGE.format(user.id))
            await ctx.channel.send(f'Sorry <@{ctx.author.id}>, I could not change this user\'s name as it is longer than 19 characters :pensive:.')
