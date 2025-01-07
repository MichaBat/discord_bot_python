import disnake
from disnake.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta

class PaulNotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_notification.start()

    def cog_unload(self):
        self.daily_notification.cancel()
    
    #Sending the message to the correct thread
    @tasks.loop(hours=24)
    async def daily_notification(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(1297138414621032518)
        if channel:
            await channel.send("This is your daily reminder to check on <@1120590404140683325> !")

    #firing the loop event at the specified time
    @daily_notification.before_loop
    async def before_daily_notification(self):
        await self.bot.wait_until_ready()
        seconds_until = self.get_time_until(13)
        await asyncio.sleep(seconds_until)
    
    #calculates the amount of time until the provided time
    def get_time_until(self, hour):
        now = datetime.now()
        target_time = datetime.combine(now.date(), datetime.strptime(f"{hour:02}:00", "%H:%M").time())
        if now.hour >= hour:
            target_time += timedelta(days=1)
        time_until = target_time - now
        return time_until.total_seconds()

def setup(bot):
    bot.add_cog(PaulNotification(bot))
