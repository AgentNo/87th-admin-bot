# dm_manager.py
# Contains functionality related to the bot's capability to send and respond to DMs

import utility.strings as strings


# Send a welcome DM to new members that joins the server
async def send_dm_to_new_member(log, member):
    log.info(member.name + " has joined the 87th. Sending welcome message...")
    await member.create_dm()
    await member.dm_channel.send(strings.DM_WELCOME_MESSAGE.format(member.name))
    log.info("Welcome message sent to " + member.name + " successfully.")
