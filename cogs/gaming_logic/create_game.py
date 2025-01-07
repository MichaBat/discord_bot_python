import disnake
from disnake.ext import commands
import os
import datetime
from .games_roles import games_roles

class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games_roles_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gaming_logic", "games_roles.py")
        self.allowed_channel_id = 1239558257882828892
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "gaming")

    def log_game_addition(self, emoji, game_name, user):
        os.makedirs(self.log_dir, exist_ok=True)
        log_file = os.path.join(self.log_dir, "game_additions.log")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - User {user} added game: {emoji} {game_name}\n"
        
        with open(log_file, "a") as f:
            f.write(log_entry)

    @commands.slash_command()
    async def add_game(
        self,
        inter: disnake.ApplicationCommandInteraction,
        emoji: str,
        game_name: str
    ):
        """
        Add a new game and its corresponding emoji to the list.
        Parameters
        ----------
        emoji: The emoji for the game
        game_name: The name of the game
        """
        if inter.channel.id != self.allowed_channel_id:
            await inter.response.send_message("This command can only be used in the designated channel.", ephemeral=True)
            return

        if len(emoji) != 1 and not emoji.startswith('<') and not emoji.endswith('>'):
            await inter.response.send_message("Please provide a valid emoji.", ephemeral=True)
            return
        if emoji in games_roles or game_name in games_roles.values():
            await inter.response.send_message("This emoji or game name already exists in the list.", ephemeral=True)
            return
        
        games_roles[emoji] = game_name
        sorted_games = dict(sorted(games_roles.items(), key=lambda x: x[1].lower()))
        
        os.makedirs(os.path.dirname(self.games_roles_path), exist_ok=True)
        
        with open(self.games_roles_path, "w") as f:
            f.write("games_roles = {\n")
            for emoji, game in sorted_games.items():
                f.write(f'    "{emoji}": "{game}",\n')
            f.write("}")
        
        # Log the game addition
        self.log_game_addition(emoji, game_name, inter.author)
        
        await inter.response.send_message(f"Added {emoji} for {game_name} to the list and sorted it.", ephemeral=True)

def setup(bot):
    bot.add_cog(GamesCog(bot))