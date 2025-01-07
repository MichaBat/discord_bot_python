import disnake
from disnake.ext import commands

class SendButtons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def send_buttons(self, ctx):
        button_Africa = disnake.ui.Button(label='Africa\u200b\u200b\u200b\u200b', style=disnake.ButtonStyle.primary, custom_id='region_Africa')
        button_Asia = disnake.ui.Button(label='Asia\u200b\u200b\u200b\u200b\u200b\u200b\u200b', style=disnake.ButtonStyle.primary, custom_id='region_Asia')
        button_Europe = disnake.ui.Button(label='Europe\u200b\u200b\u200b\u200b\u200b', style=disnake.ButtonStyle.primary, custom_id='region_Europe')
        button_North_America = disnake.ui.Button(label='North America', style=disnake.ButtonStyle.primary, custom_id='region_North_America')
        button_South_America = disnake.ui.Button(label='South America', style=disnake.ButtonStyle.primary, custom_id='region_South_America')
        button_Australia = disnake.ui.Button(label='Australia', style=disnake.ButtonStyle.primary, custom_id='region_Australia')
        view = disnake.ui.View()
        view.add_item(button_Africa)
        view.add_item(button_Asia)
        view.add_item(button_Europe)
        view.add_item(button_North_America)
        view.add_item(button_South_America)
        view.add_item(button_Australia)
        await ctx.send(
            content=(
                "\n\nTo help us identify where you're from, please choose your region by clicking one of the buttons below. "
                "This will assign you a role indicating your region.\n\n"
                "🌎 **Regions:**\n"
                "- 🌍 Africa\n"
                "- 🌏 Asia\n"
                "- 🌍 Europe\n"
                "- 🌎 North America\n"
                "- 🌍 South America\n"
                "- 🌏 Australia\n\n"
            ), view=view)

    @commands.command()
    async def event_buttons(self, ctx):
        view = disnake.ui.View()
        
        buttons = [
            disnake.ui.Button(style=disnake.ButtonStyle.primary, label="Movie/Show Night", custom_id="event_movie_show_night"),
            disnake.ui.Button(style=disnake.ButtonStyle.primary, label="Game Night", custom_id="event_game_night"),
            disnake.ui.Button(style=disnake.ButtonStyle.primary, label="Quiz Night", custom_id="event_quiz_night"),
            disnake.ui.Button(style=disnake.ButtonStyle.primary, label="Music Night", custom_id="event_music_night"),
            disnake.ui.Button(style=disnake.ButtonStyle.primary, label="Art Night", custom_id="event_art_night"),
        ]
        
        for button in buttons:
            view.add_item(button)

        await ctx.send(
            content=(
                "To be notified about events click the corresponding button to be notified for these events!. This will assign you a role indicating your preferred event night.\n\n"
                "🎉 Event Nights:\n"
                "🎥 Movie/Show Night\n"
                "🎮 Game Night\n"
                "🧠 Quiz Night\n"
                "🎵 Music Night\n"
                "🎨 Art Night\n\n"
            ),
            view=view
        )

    @commands.command()
    async def voice_chat_button(self, ctx):
        view = disnake.ui.View()
        
        button = disnake.ui.Button(
            style=disnake.ButtonStyle.secondary,
            label="Voice Chat Role",
            custom_id="voice_chat_nerds"
        )
        
        view.add_item(button)

        await ctx.send(
            content=(
                "\nClick the button below to toggle the Voice Chat role.\n\n"
                "🎙️ **Voice Chat**\n"
                "This role is for those who want to be pinged by people in voice chats.\n"
            ),
            view=view
        )

def setup(bot):
    bot.add_cog(SendButtons(bot))