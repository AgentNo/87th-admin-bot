# Bot Commands and Features

## Commands
### !hb
Heartbeat, returns the uptime of the bot. Just something I use for debug to ensure hosting is OK.

### !enlist <@user>
Will add all the Recruit roles to the @'d user. Will not work on users that are already enlisted.

### !role <merc/rep/visitor> <@user>
Adds the merc/rep/visitor role to a user.

### !attend
Updates the 'Last Seen' dates on the master doc for the users currently connected to the invoker's voice channel. Can only be used in a voice channel otherwise command will fail.

## Latent Features
### Signups Automation 
The bot will automatically send announcements every morning at 8am and add reactions in #⁠📢event-announcements as long as it has one or more of the following emojis: :RegimentalColours:, :KingsColours:, or :UnionColours:.
Replying to a message with 'unreact' will remove the bot's reactions. Note reactions will only be removed if at least one other user has also reacted with that emoji.
### Welcome DMs
The bot will automatically send a welcome message to any new members who join the discord.
### Gaming Reactions
The bot will grant or remove gaming reactions based on the user's reactions
