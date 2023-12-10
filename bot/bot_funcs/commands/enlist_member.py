# enlist_member.py
# Enlists a member in the 87th - gives them the basic 'Recruit' role set. Will fail on enlisted members.

import discord
import utility.configs as configs
import utility.strings as strings
from utility.setup_logger import logger


async def enlist_member(ctx, user: discord.Member):
    logger.info(f'Enlist command triggered by user {ctx.author.name} ({ctx.author.id}) for {user.display_name} ({user.id})')
    if None != ctx.guild.get_member(user.id).get_role(configs.GRANTABLE_ROLES["regiment"]):
        await ctx.channel.send(f':x: I can\'t do that <@{ctx.author.id}> - it looks like this member is already enlisted!')
    else: 
        await ctx.channel.send(f"Enlisting member, sit tight...")

        if None != ctx.guild.get_member(user.id).get_role(configs.GRANTABLE_ROLES["unassigned"]):
            await ctx.guild.get_member(user.id).remove_roles(ctx.guild.get_role(configs.GRANTABLE_ROLES["unassigned"]))

        for id in configs.GRANTABLE_ROLES["enlistment"]:
            try:
                role = ctx.guild.get_role(id)
                await ctx.guild.get_member(user.id).add_roles(role)
            except Exception as e:
                await ctx.channel.send(f'Error running command !enlist - {e}. Command failed on role {role}, id = {id}')
        await update_recruit_nick(ctx, user)


async def update_recruit_nick(ctx, user):
    await ctx.channel.send(strings.ENLIST_SUCCESS_MESSAGE.format(user.id))
    if len(user.display_name) < 19:
        await user.edit(nick=f'[87th] Rec. | {user.display_name}')
    else:
        await ctx.channel.send(f':pensive: Sorry <@{ctx.author.id}>, I could not change this member\'s name as it is longer than 19 characters.')
