import disnake
from disnake.ext import commands
import pytz
from dateutil import parser

class TimePoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='timepoll', description='Creates a time poll with provided time slots.')
    async def timepoll(self, inter: disnake.AppCmdInter, timezone: str, options: str):
        """Creates a time poll with provided time slots in the specified timezone."""
        try:
            # Validate the timezone
            try:
                user_tz = pytz.timezone(timezone)
            except pytz.UnknownTimeZoneError:
                await inter.send(f"Unknown timezone: {timezone}. Defaulting to UTC.", ephemeral=True)
                user_tz = pytz.UTC

            # Split the options by commas or spaces
            time_options = options.split(",")
            time_options = [opt.strip() for opt in time_options if opt.strip()]

            # Handle the case where no options are provided
            if not time_options:
                await inter.send("Please provide at least one time slot option.", ephemeral=True)
                return

            # Convert provided options to UTC
            option_times = []
            for option in time_options:
                try:
                    # Parse the time slot and convert it to UTC
                    local_time = parser.parse(option)
                    local_time = user_tz.localize(local_time)
                    utc_time = local_time.astimezone(pytz.utc)
                    option_times.append((option, utc_time))
                except Exception as e:
                    await inter.send(f"Error parsing time option '{option}': {str(e)}", ephemeral=True)
                    return

            # Create the poll message
            poll_message = await inter.send(
                f"**Time Poll:**\n"
                f"React with the corresponding number to vote for a time slot.\n\n"
                + "\n".join([f"{i+1}. {opt[0]} (UTC: {opt[1].isoformat()})" for i, opt in enumerate(option_times)])
            )

            # Add reactions to the poll message
            for i in range(len(option_times)):
                await poll_message.add_reaction(str(i + 1))

        except Exception as e:
            await inter.send(f"An error occurred: {str(e)}", ephemeral=True)


def setup(bot):
    bot.add_cog(TimePoll(bot))
