import disnake
from disnake.ext import commands
from datetime import datetime, timedelta
import time

class TimePoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
    name="timepoll",
    description="Create a time-based poll with a question and time options"
    )
    async def timepoll(
        self,
        inter: disnake.ApplicationCommandInteraction,
        message: str = commands.Param(description="The poll question"),
        date: str = commands.Param(description="Date in DD-MM-YYYY format"),
        options: str = commands.Param(description="Comma-separated list of time options in HH:MM format")
    ):
        try:
            poll_date = datetime.strptime(date, "%d-%m-%Y").date()
        except ValueError:
            await inter.response.send_message("Invalid date format. Please use DD-MM-YYYY for date.", ephemeral=True)
            return

        if poll_date < datetime.now().date():
            await inter.response.send_message("The poll date must be in the future.", ephemeral=True)
            return

        # Split the options by comma and strip any extra whitespace
        poll_options = [opt.strip() for opt in options.split(",")]
        if len(poll_options) < 2:
            await inter.response.send_message("Please provide at least two time options for the poll.", ephemeral=True)
            return
        if len(poll_options) > 10:
            await inter.response.send_message("Please provide no more than ten time options for the poll.", ephemeral=True)
            return

        # Construct the poll question
        poll_question = f"**Time Poll for {poll_date.strftime('%d-%m-%Y')}**\n{message}\n\n"
        poll_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        valid_options = []

        # Add each option to the poll question        
        for i, option in enumerate(poll_options):
            try:
                # Parse the option as HH:MM
                option_time = datetime.strptime(option, "%H:%M").time()
                
                # Combine the poll date with the option time
                option_datetime = datetime.combine(poll_date, option_time)
                
                unix_time = int(time.mktime(option_datetime.timetuple()))
                formatted_time = f"<t:{unix_time}:t>  <t:{unix_time}:R>"  # Use 't' for short time format
                poll_question += f"{poll_emojis[i]} {formatted_time}\n"
                valid_options.append(option)
            except ValueError:
                await inter.response.send_message(f"Invalid time format for option: {option}. Please use HH:MM format.", ephemeral=True)
                return

        # Send the poll question
        await inter.response.send_message(poll_question, ephemeral=False)
        poll_message = await inter.original_message()

        # Add reactions for each option
        for i in range(len(valid_options)):
            await poll_message.add_reaction(poll_emojis[i])

def setup(bot):
    bot.add_cog(TimePoll(bot))