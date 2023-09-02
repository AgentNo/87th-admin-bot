# Bot Commands and Features

## Commands
### !hb
Heartbeat, returns the uptime of the bot. Just something I use for debug to ensure hosting is OK.

### !enlist <@user>
Will add all the Recruit roles to the @'d user. Will not work on users that are already enlisted.

### !grantrole <merc/rep/visitor> <@user>
Adds or removes the merc/rep/visitor role on a user, depending on whether or not they already have it.

### !attend
Updates the 'Last Seen' dates on the master doc for the users currently connected to the invoker's voice channel. Can only be used in a voice channel otherwise command will fail.

## Latent Features
### Signups Automation 
The bot will automatically add reactions to posts in #⁠📢event-announcements as long as it has one or more of the following emojis: :RegimentalColours:, :KingsColours:, or :UnionColours:.
The bot will currently not remove these reactions automatically.
### Femboys!
The bot has a 3% chance to respond to users who mention 'femboy' in the discord. Just a wee easter egg.
### Welcome DMs
The bot will automatically send a welcome message to any new members who join the discord.
