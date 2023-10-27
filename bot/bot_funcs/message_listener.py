# message_listener.py
# Contains functionality based on listening to and reacting to text mesasges send in the discord

import utility.enums as enums
import random


async def check_if_message_has_femboy(message):
    if 'femboy' in message.content and not message.author.bot:
        number = random.uniform(1,100)
        if number < 6:
            await message.channel.send(f'Spammy is not a femboy <@{message.author.id}>. Please stop spreading fake news.')


# Checks if a message in #event-announcements needs signup emojis, and will add them if needed
async def check_and_put_signup_reactions(message, bot): 
    if 'RegimentalColours' in message.content:
        for reaction in enums.PRIMARY_SIGNUP_REACTIONS:
            await message.add_reaction(reaction)
    if 'KingsColours' in message.content:
        for reaction in enums.SECONDARY_SIGNUP_REACTIONS:
            await message.add_reaction(reaction)
    if 'UnionColours' in message.content:
        for reaction in enums.TERTIARY_SIGNUP_REACTIONS:
            await message.add_reaction(reaction)

    if 'unreact' in message.content and message.reference is not None:
        original_message = await message.channel.fetch_message(message.reference.message_id)
        reactions = original_message.reactions
        for reaction in reactions:
            if reaction.me and reaction.count >= 2:
                await reaction.remove(bot)
        await message.delete()

