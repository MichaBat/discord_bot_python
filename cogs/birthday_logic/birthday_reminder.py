import disnake
from disnake.ext import commands, tasks
import os
import datetime

class BirthdayReminderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthday_file = os.path.join(os.path.dirname(__file__), 'birthdays.txt')
        self.birthdays = self.load_birthdays()
        self.reminder_channel_id = 1237750636418699294
        self.birthday_reminder.start()

    def load_birthdays(self):
        if not os.path.exists(self.birthday_file):
            return {}

        with open(self.birthday_file, 'r') as f:
            lines = f.readlines()
            birthdays = {}
            for line in lines:
                user_id, date = line.strip().split(',')
                birthdays[int(user_id)] = date
            return birthdays

    @tasks.loop(hours=24)
    async def birthday_reminder(self):
        current_date = datetime.datetime.now().strftime('%d-%m')
        for user_id, date in self.birthdays.items():
            if date == current_date:
                user = await self.bot.fetch_user(user_id)
                if user:
                    channel = self.bot.get_channel(self.reminder_channel_id)
                    await channel.send(f'Happy Birthday, {user.mention}! 🎉')

    @birthday_reminder.before_loop
    async def before_birthday_reminder(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(BirthdayReminderCog(bot))
