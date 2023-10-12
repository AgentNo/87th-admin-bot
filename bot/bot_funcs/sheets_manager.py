# sheets_manager.py
# Contains functionality related to Google Sheets and associated bot commands such as !attend

import gspread
import os
from dotenv import load_dotenv
from datetime import datetime


# Get and return a dictionary of all secrets for the sheets integration
async def get_master_doc_secrets():
    load_dotenv()
    __secrets = dict()
    __secrets["SHEETS_KEY_TEST"] = os.getenv('SHEETS_MASTER_DOC_KEY_TEST')
    __secrets["MEMBERS_SHEET_TEST"] = os.getenv('SHEETS_MASTER_DOC_MEMBERS_SHEET_NAME_TEST')
    __secrets["SHEETS_KEY"] = os.getenv('SHEETS_MASTER_DOC_KEY')
    __secrets["MEMBERS_SHEET"] = os.getenv('SHEETS_MASTER_DOC_MEMBERS_SHEET_NAME')
    return __secrets


# Get and return the connection object for the master doc
# TO RUN LOCALLY: replace the filename arg with 'bot/sheets_keys.json'
async def get_master_doc_connection(SHEETS_KEY):
    gc = gspread.service_account(filename='bot/sheets_keys.json')
    gdoc = gc.open_by_key(SHEETS_KEY)
    return gdoc


# Helper function to determine if the member exists in the master doc 'Members' sheet. Return the INDEX (row number) if found, otherwise -1.
async def search_for_member_in_sheet(worksheet, member):
    members_column = worksheet.col_values(3)
    try:
        print(member.id)
        index = members_column.index(str(member.id))
        return index + 1
    except ValueError:
        return -1


# Update last seen date for a single member - takes today's date as the target data
async def update_last_seen_for_member(worksheet, index):
    new_date = datetime.today().strftime("%d/%m/%Y")
    worksheet.update(f'I{index}', new_date)
