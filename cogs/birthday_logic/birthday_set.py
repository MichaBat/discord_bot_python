import disnake
from disnake.ext import commands
import os
import calendar

class SetBirthdayCog(commands.Cog):
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

    def save_birthdays(self):
        with open(self.birthday_file, 'w') as f:
            for user_id, date in self.birthdays.items():
                f.write(f'{user_id},{date}\n')

    @commands.slash_command(description="Set your birthday. Use the format DD-MM")
    async def set_birthday(self, inter: disnake.ApplicationCommandInteraction, date: str):
        """Set your birthday in the format DD-MM."""
        # Basic validation to check if date is in DD-MM format
        try:
            day, month = map(int, date.split('-'))
            if not (1 <= day <= 31 and 1 <= month <= 12):
                raise ValueError
        except ValueError:
            await inter.response.send_message('Invalid date format. Please use DD-MM.')
            return

        # Convert month number to month name
        month_name = calendar.month_name[month]
        self.birthdays[inter.author.id] = date
        self.save_birthdays()
        
        await inter.response.send_message(f'Your birthday has been set to {day} {month_name}.')

def setup(bot):
    bot.add_cog(SetBirthdayCog(bot))
