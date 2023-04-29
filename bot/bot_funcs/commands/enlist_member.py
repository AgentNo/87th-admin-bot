# enlist_member.py
# Enlists a member in the 87th - gives them the basic 'Recruit' role set. Will fail on enlisted members.

import discord
import utility.enums as enums

async def enlist_member(ctx, user: discord.Member, log):
    log.info(f'Enlist command triggered by user {ctx.author.name} ({ctx.author.id}) for {user.display_name}({user.id}). Attempting to enlist...')
    if None != ctx.guild.get_member(user.id).get_role(enums.GRANTABLE_ROLES["regiment"]):
        log.info(f'Error running command - user {user.display_name}({user.id}) is already enlisted.')
        await ctx.channel.send(f':x: I can\'t do that <@{ctx.author.id}> - it looks like <@{user.id}> is already enlisted!')
    else: 
        if None != ctx.guild.get_member(user.id).get_role(enums.GRANTABLE_ROLES["unassigned"]):
            await ctx.guild.get_member(user.id).remove_roles(ctx.guild.get_role(enums.GRANTABLE_ROLES["unassigned"])) # Remove the 'Unassigned' role
            await ctx.channel.send(f"Enlisting this user, sit tight...")
        for id in enums.GRANTABLE_ROLES["enlistment"]:
            try:
                role = ctx.guild.get_role(id)
                await ctx.guild.get_member(user.id).add_roles(role)
                log.info(f'Added enlistment role {id} to user {user.display_name} ({user.id})')
            except Exception as e:
                await ctx.channel.send(f'Error running command !enlist - {e}. Command failed on role {role}, id = {id}')
                log.info(f"Error running command !enlist - {e}. Command failed on role {role}, id = {id}")
        if len(user.display_name) < 19:
            await user.edit(nick=f'[87th] Rec. | {user.display_name}')
            await ctx.channel.send(f'<@{user.id}> has been enlisted successfully. Welcome! :crossed_swords:')
        else:
            await ctx.channel.send(f'<@{user.id}> has been enlisted successfully. Welcome! :crossed_swords:')
            await ctx.channel.send(f'Sorry <@{ctx.author.id}>, I could not change this user\'s name as it is longer than 19 characters :pensive:.')
        log.info(f'{user.display_name}({user.id}) has been enlisted successfully!')
