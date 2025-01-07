import disnake
from disnake.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta

class DailyStandupReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_notification.start()

    def cog_unload(self):
        self.daily_notification.cancel()

    @tasks.loop(hours=24)
    async def daily_notification(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(1285620049872158720) 
        if channel:
            current_date = datetime.now().strftime("%d-%m-%Y")
            await channel.send(f'## This is your reminder on 📅 {current_date}  to do your daily standup in {channel.mention}')

    @daily_notification.before_loop
    async def before_daily_notification(self):
        await self.bot.wait_until_ready()
        seconds_until = self.get_time_until(8)  
        await asyncio.sleep(seconds_until)

    def get_time_until(self, hour):
        now = datetime.now()
        target_time = datetime.combine(now.date(), datetime.strptime(f"{hour:02}:00", "%H:%M").time())
        if now.hour >= hour:
            target_time += timedelta(days=1)
        time_until = target_time - now
        return time_until.total_seconds()

def setup(bot):
    bot.add_cog(DailyStandupReminder(bot))
