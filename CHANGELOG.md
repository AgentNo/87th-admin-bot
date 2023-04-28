# Changelog for 87th Admin Bot
Note: This file was started on 2023-04-22. Any changes before then are not captured.

## 2023-04-29
- Added functionality to automatically add reactions to announcement posts

## 2023-04-24
- Changed permission commands to a more reliable method of validation
- Tidied the enums.py util

## 2023-04-23
- Improvements to logging - logs will now record user names as well as IDs

## 2023-04-22
- Updated !hb to include uptime
- Moved logging logic into a seperate util file
- Added a case for MissingRequiredArguement to !enlist
- Merged both !merc and !rep into a single command - !grantrole. This could be expanded in future to include other roles
- !enlist - will now automatically format a user's name with Recruit tags if it is less than 32 - 13 = 19 characters
- !grantrole will now check for and remove the Unassigned role if present
- There is now a 5% chance the bot will respond to a user if they mention 'femboy' in the discord