# sheets_manager.py
# Contains functionality related to Google Sheets and associated bot commands such as !attend

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os


# Updates the 'Last Seen' column for all users in a voice call
async def attend(log, ctx, SHEETS_KEY, MEMBERS_SHEET):
    log.info(f"!attend triggered by user {ctx.author.name} ({ctx.author.id}) in channel {ctx.author.voice.channel.id}. Starting attendance updates...")
    print(os.getcwd())
    gc = gspread.service_account(filename='bot/sheets_keys_test.json')
    gdoc = gc.open_by_key(SHEETS_KEY)
    worksheet = gdoc.worksheet(MEMBERS_SHEET)


# Updatse the 'Last Seen' column with a specific user
async def attend_one_user():
    pass

