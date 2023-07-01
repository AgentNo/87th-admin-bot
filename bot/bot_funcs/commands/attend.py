# attend.py
# Updates the 'Last Seen' column for all users in a voice call. Must be used in a voice call or command will fail
from bot_funcs import sheets_manager


async def attend(log, ctx):
    log.info(f"!attend triggered by user {ctx.author.name} ({ctx.author.id}) in channel {ctx.author.voice.channel.id}. Starting attendance updates...")
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
            log.info(f"Updated Last Seen for member {member.name} ({member.id}) in row {member_row}")
            processed_members += 1
        else:
            log.info(f"Error - user {member.name} does not exist in the master doc. Probably not enlisted with us...")
            errored_users.append(member)
    
    message = f":white_check_mark: Last seen updated for {processed_members} succesfully!"
    if len(errored_users) > 0:
        message += f"\n {len(errored_users)} couldn't be updated:\n"
        for member in errored_users:
            message += f"\n {member.display_name} ({member.name})"
    await ctx.channel.send(message)
