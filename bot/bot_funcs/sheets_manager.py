# sheets_manager.py
# Contains functionality related to Google Sheets and associated bot commands such as !attend

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


# Updates the 'Last Seen' column for all users in a voice call
async def attend(log, ctx, SHEETS_KEY, MEMBERS_SHEET):
    log.info(f"!attend triggered by user {ctx.author.name} ({ctx.author.id}) in channel {ctx.author.voice.channel.id}. Starting attendance updates...")
    await ctx.channel.send(f"Taking attendance for {len(ctx.author.voice.channel.members)} members, sit tight...")
    gc = gspread.service_account(filename='bot/sheets_keys_test.json')
    gdoc = gc.open_by_key(SHEETS_KEY)
    worksheet = gdoc.worksheet(MEMBERS_SHEET)

    processed_members = 0
    errored_users = []
    for member in ctx.author.voice.channel.members:
        member_row = await search_for_member_in_sheet(worksheet, member)
        if member_row != -1:
            await update_last_seen_for_member(worksheet, member_row)
            log.info(f"Updated Last Seen for member {member.name} ({member.id}) in row {member_row}")
            processed_members += 1
        else:
            log.info(f"Error - user {member.name} does not exist in the master doc. Probably not enlisted with us...")
            errored_users.append(member)
    
    message = f":white_check_mark: Last seen updated for {processed_members} succesfully!"
    if len(errored_users) > 0:
        message += f"\n {len(errored_users)} couldn't be updated:\n"
        for member in errored_users:
            message += f"\n {member.name}"
    await ctx.channel.send(message)


# Helper function to determine if the member exists in the master doc 'Members' sheet. Return the INDEX (row number) if found, otherwise -1.
async def search_for_member_in_sheet(worksheet, member):
    members_column = worksheet.col_values(3)
    try:
        index = members_column.index(member.name)
        return index+1
    except ValueError:
        return -1


# Update last seen date for a single member
async def update_last_seen_for_member(worksheet, index):
    new_date = datetime.today().strftime('%d/%m/%Y')
    worksheet.update(f'H{index}', new_date)
