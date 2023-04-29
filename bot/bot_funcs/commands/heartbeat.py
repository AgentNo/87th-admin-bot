# heartbeat.py
# Returns the uptime of the bot in hh:mm:ss

import time
import datetime


async def heartbeat(ctx, startTime, log):
    try:
        currentTime = time.time()
        log.info(f"Heartbeat command triggered by user {ctx.author.name}, sending response.")
        await ctx.channel.send(f"87th Admin Bot is up and running! :heartpulse:\nThis instance has been alive for {datetime.timedelta(seconds=int(currentTime-startTime))}!")
    except Exception as e:
        await ctx.channel.send(f"<@221717120310968322>, looks like something is wrong with the admin bot - {e}")
        log.info(f'Error thrown in !hb - {e}')
