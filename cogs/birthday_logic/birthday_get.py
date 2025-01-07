import disnake
from disnake.ext import commands
import os
import calendar

class GetBirthdayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthday_file = os.path.join(os.path.dirname(__file__), 'birthdays.txt')
        self.birthdays = self.load_birthdays()

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

    @commands.slash_command(description="Get a user's birthday.")
    async def get_birthday(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        """Get a user's birthday."""
        date = self.birthdays.get(user.id)
        if date:
            day, month = date.split('-')
            month_name = calendar.month_name[int(month)]
            await inter.response.send_message(f'{user.name}\'s birthday is on {day} {month_name}.')
        else:
            await inter.response.send_message(f'{user.name} has not set their birthday.')

def setup(bot):
    bot.add_cog(GetBirthdayCog(bot))
