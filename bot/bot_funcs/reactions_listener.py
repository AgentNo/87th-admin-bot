# reactions_listener.py
# Functions related to reactions on messages

import utility.configs as configs


# Handle gaming role reactions
async def add_or_remove_gaming_role(bot, payload, remove_unrelated = True):
    if payload.emoji.name in configs.GAME_ROLE_REACTIONS:
        role_id = configs.GAME_ROLE_REACTIONS[payload.emoji.name]
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(role_id)
        if payload.event_type == "REACTION_ADD":
            if payload.member.get_role(role_id) == None:
                await payload.member.add_roles(role)
        if payload.event_type == "REACTION_REMOVE":
            member = guild.get_member(payload.user_id)
            if member.get_role(role_id) != None:
                await member.remove_roles(role)
    else:
        if remove_unrelated:
            await remove_reaction_from_message(payload)


# Remove unrelated reactions from the message
# This only fires if remove_unrelated is TRUE. This is set to FALSE when the on_reaction_remove handler is called
# to prevent unwanted looping. 
async def remove_reaction_from_message(payload):
    channel = await payload.member.guild.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    for reaction in message.reactions:
        if (payload.emoji.is_custom_emoji and reaction.emoji == payload.emoji) or reaction.emoji == payload.emoji.name:
            await reaction.remove(payload.member)
