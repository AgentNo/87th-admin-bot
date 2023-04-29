# grant_role.py
# Adds or removes the merc, rep, and/or visitor tag depending on whether the user has them or not

import utility.enums as enums
import discord

async def grant_role(ctx, roleType, user: discord.User, log):
    log.info(f'grantrole command triggered by user {ctx.author.name} ({ctx.author.id}) for {user.display_name} ({user.id}) to change {roleType} tags. Checking status of user...')
    if None != ctx.guild.get_member(user.id).get_role(enums.GRANTABLE_ROLES["regiment"]):
        log.info(f'Error running !grantrole command - user {user.display_name} ({user.id}) is already enlisted in the 87th.')
        await ctx.channel.send(f':x: I can\'t do that <@{ctx.author.id}> - it looks like <@{user.id}> is already enlisted!')
        return
    else:
        if str(roleType).lower() not in ['merc', 'rep', 'visitor']:
            await ctx.channel.send(f"Hmm <@{ctx.author.id}>, I don't recognise that role :face_with_monocle:. You can use **merc**, **rep**, or **visitor** as valid options.")
            return
        
        if None != ctx.guild.get_member(user.id).get_role(enums.GRANTABLE_ROLES["unassigned"]):
            log.info('User has Unassigned role, removing now...')
            await ctx.guild.get_member(user.id).remove_roles(ctx.guild.get_role(enums.GRANTABLE_ROLES["unassigned"])) # Remove the 'Unassigned' role

        roleToManage = enums.GRANTABLE_ROLES[str(roleType).lower()]
        if None != ctx.guild.get_member(user.id).get_role(roleToManage):
            log.info(f' {user.display_name}({user.id}) already has {roleType} tags. Will remove them now...')
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
                log.info(f'Added {roleType} tags to user {user.display_name} ({user.id}) successfully')
                if roleType == "merc" or roleType == "rep":
                    visitor_role = ctx.guild.get_role(enums.GRANTABLE_ROLES["visitor"])
                    await ctx.guild.get_member(user.id).add_roles(visitor_role)
                    log.info(f'Added visitor tags to user  {user.display_name}({user.id}) successfully')
                await ctx.channel.send(f'<@{user.id}> has been enlisted as a {roleType} successfully. Welcome! :crossed_swords:')
            except Exception as e:
                await ctx.channel.send(f'Error running command !grantrole - {e}.')
                log.info(f"Error running command !grantrole - {e}.")