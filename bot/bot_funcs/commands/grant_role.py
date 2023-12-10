# grant_role.py
# Adds or removes the merc, rep, and/or visitor tag depending on whether the user has them or not

import utility.configs as configs
import discord
from utility.setup_logger import logger

async def grant_role(ctx, roleType, user: discord.User):
    logger.info(f'!role command triggered by {ctx.author.name} ({ctx.author.id}) for {user.display_name} ({user.id}) to change {roleType} tags')

    if None != ctx.guild.get_member(user.id).get_role(configs.GRANTABLE_ROLES["regiment"]):
        await ctx.channel.send(f':x: I can\'t do that <@{ctx.author.id}> - this member is already enlisted!')
        return
    else:
        if str(roleType).lower() not in ['merc', 'rep', 'visitor']:
            await ctx.channel.send(f"Hmm <@{ctx.author.id}>, I don't recognise that role :face_with_monocle:. You can use **merc**, **rep**, or **visitor** as valid options.")
            return
        
    if None != ctx.guild.get_member(user.id).get_role(configs.GRANTABLE_ROLES["unassigned"]):
        await ctx.guild.get_member(user.id).remove_roles(ctx.guild.get_role(configs.GRANTABLE_ROLES["unassigned"]))

    roleId = configs.GRANTABLE_ROLES[str(roleType).lower()]
    if None != ctx.guild.get_member(user.id).get_role(roleId):
        await ctx.channel.send(f':x: <@{ctx.author.id}>, this member already has these tags.')
    else:
        try:
            # If a user is registering as a merc or rep, also give them the visitor tag
            role = ctx.guild.get_role(roleId)
            await ctx.guild.get_member(user.id).add_roles(role)

            if roleType == "merc" or roleType == "rep":
                visitor_role = ctx.guild.get_role(configs.GRANTABLE_ROLES["visitor"])
                await ctx.guild.get_member(user.id).add_roles(visitor_role)
            
            await ctx.channel.send(f'Member has been enlisted as a {roleType} successfully. Welcome! :crossed_swords:')
        except Exception as e:
            await ctx.channel.send(f'Error running command !role - {e}.')
