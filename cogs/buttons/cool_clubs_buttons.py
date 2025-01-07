import disnake
from disnake.ext import commands
from config import COOL_CLUBS_IDS

class CoolClubsButtons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cool_clubs(self, ctx):
        intro_message = (
            "Welcome to the ultimate role selection!:star2: Are you excited to find your perfect fit among these awesome options? "
            "Check out what each role has to offer!:\n\n"
            "<@&1238859816907178065> — Keeping everything running smoothly and ensuring a great community experience! :shield:\n\n"
            "<@&1264667275747922031> — We just like blue, not much else, definitely not these ones below! :blue_heart:\n"
            "<@&1264667222215753738> — We're all about anything! :purple_heart: \n"
            "<@&1264667276800426005> — We're all about the mind! :brain:\n"
            "<@&1264667493805588630> — We are energized and determined to reach our goals! :yellow_heart:\n"
            "<@&1264667562856288317> — We embrace energy and strength with a focus on fitness and well-being! :muscle:\n"
            "<@&1264667600894427276> — We dive into epic adventures and level up our skills! :video_game:\n"
            "<@&1264667670465478786> — We're all about feeling the rhythm and explore diverse sounds! :musical_note: \n"
            "<@&1264667860039630848> — We're all about the latest and greatest gadgets and innovations! :computer:\n"
            "<@&1264667903664324678> — Explore the world of movies, TV shows, and viral content with us! :clapper:\n"
            "<@&1264667940213493858> — Join us for exciting gatherings and unforgettable moments! :calendar:\n\n"
            "Are you ready to choose your role and make an impact! Each role might be put to the test during events, "
            "where they'll team up and showcase my skills. Let's make some magic happen! :rocket:\n\n"
            "Join a Role! (You can only be in one at a time)\n\n"
        )
        
        await ctx.send(intro_message, components=self.create_buttons(ctx.guild))

    def create_buttons(self, guild):
        buttons = []
        for club_id in COOL_CLUBS_IDS:
            role = guild.get_role(club_id)
            if role:
                button = disnake.ui.Button(
                    style=disnake.ButtonStyle.success,
                    label=role.name,
                    custom_id=f"cool_club_{club_id}",
                )
                
                # Set button color based on role color
                if role.color != disnake.Color.default():
                    button.style = disnake.ButtonStyle.primary
                    button.custom_id = f"cool_club_{club_id}_{role.color.value:06x}"
                
                buttons.append(button)
        
        # Create rows of buttons, 5 buttons per row
        rows = [disnake.ui.ActionRow(*buttons[i:i+5]) for i in range(0, len(buttons), 5)]
        return rows

def setup(bot):
    bot.add_cog(CoolClubsButtons(bot))