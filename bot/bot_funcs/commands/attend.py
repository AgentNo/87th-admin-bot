# attend.py
# Updates the 'Last Seen' column for all users in a voice call. Must be used in a voice call or command will fail
from bot_funcs import sheets_manager
from utility.setup_logger import logger


async def attend(ctx):
    logger.info(f"!attend triggered by {ctx.author.name} ({ctx.author.id}) in channel {ctx.author.voice.channel.id}")
    await ctx.channel.send(f"Taking attendance for {len(ctx.author.voice.channel.members)} members, sit tight...")
    __secrets = await sheets_manager.get_master_doc_secrets()
    gdoc = await sheets_manager.get_master_doc_connection(__secrets["SHEETS_KEY"])
    worksheet = gdoc.worksheet(__secrets["MEMBERS_SHEET"])

    processed_members = 0
    errored_users = []
    for member in ctx.author.voice.channel.members:
        member_row = await sheets_manager.search_for_member_in_sheet(worksheet, member)
        if member_row != -1:
            await sheets_manager.update_last_seen_for_member(worksheet, member_row)
            processed_members += 1
        else:
            errored_users.append(member)
    
    if processed_members > 0:
        message = f":white_check_mark: Last seen updated for {processed_members} members succesfully!"
    else:
        message = f":x: No members were processed successfully in this execution"

    if len(errored_users) > 0:
        message += f"\n {len(errored_users)} members couldn't be updated:\n"
        for member in errored_users:
            message += f"\n {member.display_name} ({member.name})"
            
    await ctx.channel.send(message)
