# sheets_manager.py
# Contains functionality related to Google Sheets and associated bot commands such as !attend

import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Updates the 'Last Seen' column for all users in a voice call
async def attend(ctx, SHEETS_KEY, MEMBERS_SHEET):
    log.info(f"!attend triggered by user {ctx.author.id} in {ctx.author.voice.channel.id}. Starting attendance updates...")
    gc = gspread.service_account(filename='../sheets_keys_test.json')
    gdoc = gc.open_by_key(SHEETS_KEY)
    worksheet = gdoc.worksheet("SpammyTestingSheet")


# Updatse the 'Last Seen' column with a specific user
async def attend_one_user():
    pass

