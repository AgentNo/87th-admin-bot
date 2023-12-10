# message_listener.py
# Contains functionality based on listening to and reacting to text mesasges sent in the discord

import utility.configs as configs
import utility.strings as strings
import os
from datetime import datetime as date
from dotenv import load_dotenv


async def send_event_announcement(bot):
    load_dotenv()
    guild_id = os.getenv('DISCORD_PROD_GUILD_ID')
    guild = await bot.fetch_guild(guild_id)
    channel = await guild.fetch_channel(configs.EVENT_ANNOUNCEMENT_CHANNEL_ID)
    day = date.today().strftime("%A")

    if configs.EVENT_ANNOUNCEMENT_CONFIG[day]["numEvents"] == 0:
        await channel.send(strings.NO_EVENTS_MESSAGE)
        return
    
    daily_config = configs.EVENT_ANNOUNCEMENT_CONFIG[day]
    formatted_message = strings.EVENT_ANNOUNCEMENT_MESSAGE.format(daily_config["numEvents"], daily_config["eventBody"], daily_config["reactions"])
    await channel.send(formatted_message)


# Checks if a message in #event-announcements needs signup emojis, and will add them if needed
async def add_or_remove_signup_reactions(message, bot): 
    if 'RegimentalColours' in message.content:
        for reaction in configs.PRIMARY_SIGNUP_REACTIONS:
            await message.add_reaction(reaction)
    if 'KingsColours' in message.content:
        for reaction in configs.SECONDARY_SIGNUP_REACTIONS:
            await message.add_reaction(reaction)
    if 'UnionColours' in message.content:
        for reaction in configs.TERTIARY_SIGNUP_REACTIONS:
            await message.add_reaction(reaction)

    if 'unreact' in message.content and message.reference is not None:
        original_message = await message.channel.fetch_message(message.reference.message_id)
        reactions = original_message.reactions
        for reaction in reactions:
            if reaction.me and reaction.count >= 2:
                await reaction.remove(bot)
        await message.delete()

