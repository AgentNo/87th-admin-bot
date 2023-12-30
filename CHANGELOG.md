# Changelog for 87th Admin Bot
Note: This file was started on 2023-04-22. Any changes before then are not captured.

## 2023-12-29
- Added Lethal Company as an option to community roles

## 2023-12-20
- Temporarily turning off event announcements for Christmas break

## 2023-12-15
- Updated event announcement text
- Changed event time from 8am to 7.30am GMT

## 2023-12-10
- Updated README
- Renamed `enums.py` to `configs.py` to better represent content of file
- Added automated event announcements and assorted strings etc.

## 2023-12-09
- Changed name of signup function to better reflect its purpose (`check_and_put_signup_reactions` -> `add_or_remove_signup_reactions`)
- Removed the femboy easter egg. Was a joke that overstayed its welcome
- Removed some pointless conditions from the the community roles functionality
- Tidied up the `!enlist` function
- Updated frontend messaging to replace 'users' with 'members'
- Tidied up `!role` functionality
- `!role` will no longer remove roles if the user already has them
- Fixed error where !attend did not correctly report instances of AttributeError when used outside a voice call

## 2023-12-01
- Introduced error handling into dm_message listener and improved logging
- Removed `getDevGuild()` since it is no longer used
- Re-worked logging to be less stupid that it was previously
- Reduced the amount of useless logging across the whole application.

## 2023-11-24
- Cut down logging and moved `!hb` command logic back into the handler

## 2023-11-15
- Updated DM welcome message and enlistment message 
- Fixed the order of events in `on_message` so commands are processed last
- Improved help command text on commands
- Renamed `!grantole` to `!role`. Functionality is unaffected.

## 2023-11-11
- Added functionality to react for gaming roles.

## 2023-11-10
- The Among Us role is no longer granted as part of enlistment.

## 2023-10-27
- Moved the channel check for event announcements to the handler method, which prevents invocation on every message sent in the discord
- Upped the femboy chance from 3 to 6 percent
- Added unreact funcionality - replying to an event announcement with 'unreact' will remove all bot reactions on the message provided there is a least one other reaction per reaction.

## 2023-10-25
- Removed unused LEADERSHIP_ROLES enum
- Fixed !attend error handing method being incorrectly named.

## 2023-10-12
- Improved error logging in !attend
- !attend will no longer print out the ID of a user while searching the sheet
- Fixed file path to sheets keys to comply with new hosting restrictions.

## 2023-09-09
- Fixed a bug around reporting failed users in the `!attend` command (failed users should now report correctly).

## 2023-09-02
- Added secrets and functionality for PROD release of `!attend`
- Improved logging and error handling in `!attend`

## 2023-07-01
- Removed an unneeded newline character in the enlistment message
- Tidied up sheets_manager and the attend command handler.

## 2023-06-24
- Removed 'Medal Automation' as a planned feature in README.md
- Updated README.md with additional contact information
- Added base structure for accessing Google Docs through the !attend command
- Added first implementation of `!attend`.

## 2023-06-14
- Updated discord.py version to fix issues with the latest discord update
- Removed .vscode directory

## 2023-05-20
- !enlist now contains the instructions to join the registry etc. in the confirmation message

## 2023-05-15
- Fixed an error message in !grantrole

## 2023-05-12 (v. 1.1)
- Added whitespace to enlist logs
- Fixed an issue where authentication broke with library update - the bot now users has_role() to check for the presence of the Bot User role.

## 2023-04-30 (v. 1.0.3)
- Updated README.md
- Added COMMANDS.md (documentation)
- !hb now formats the time into a more sensible hh:mm:ss format
- Re-organised the project to reduce the amount of clutter in bot.py
- !enlist now sends a confirmation message on invoke
- Fixed a logging grammar issue in !enlist
- Fixed several whitespace inconsistencies in !grantrole

## 2023-04-29 (v. 1.0.3)
- Added functionality to automatically add reactions to announcement posts

## 2023-04-24 (v. 1.0.2)
- Changed permission commands to a more reliable method of validation
- Tidied the enums.py util

## 2023-04-23 (v. 1.0.1)
- Improvements to logging - logs will now record user names as well as IDs

## 2023-04-22 (v. 1.0)
- Updated !hb to include uptime
- Moved logging logic into a seperate util file
- Added a case for MissingRequiredArguement to !enlist
- Merged both !merc and !rep into a single command - !grantrole. This could be expanded in future to include other roles
- !enlist - will now automatically format a user's name with Recruit tags if it is less than 32 - 13 = 19 characters
- !grantrole will now check for and remove the Unassigned role if present
- There is now a 5% chance the bot will respond to a user if they mention 'femboy' in the discord