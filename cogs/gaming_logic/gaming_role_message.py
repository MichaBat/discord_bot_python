import disnake
from disnake.ext import commands
from .games_roles import games_roles
from config import GUILD_ID, GAME_REACTIONROLES_CHANNEL_ID

class GameRoleMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(GUILD_ID)
    
    @commands.command()
    async def send_games(self, ctx):
        guild = GUILD_ID
        print(GUILD_ID)

        if guild is None:
            print("Guild not found!")
            return
        
        #channel = disnake.utils.get(guild.channels, name="🤼roles")
        #channel = disnake.utils.get(guild.channels, name="🤼game_roles")
        channel = self.bot.get_channel(GAME_REACTIONROLES_CHANNEL_ID)
        print(channel)
        if channel:
            games_per_page = 20
            games_list = list(games_roles.items())  # Assuming games_roles is a dictionary
            for page in range(0, len(games_list), games_per_page):
                message_content = "React with the corresponding emoji to get the respective role:\n"
                page_games = games_list[page:page+games_per_page]
                message_content += "\n".join([f"{emoji} - {game}" for emoji, game in page_games])
                message = await channel.send(message_content)
                for emoji, game in page_games:
                    try:
                        print(f"Adding reaction {emoji} for game {game}")
                        await message.add_reaction(emoji)
                    except disnake.HTTPException as e:
                        print(f"Failed to add reaction: {emoji} for game {game}. Error: {e}")

def setup(bot):
    bot.add_cog(GameRoleMessage(bot))
