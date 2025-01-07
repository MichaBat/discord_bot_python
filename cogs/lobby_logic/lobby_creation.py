import disnake
from disnake.ext import commands

class LobbyLogic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lobby_number = 1

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel and before.channel.name.startswith("Lobby"):
            if len(before.channel.members) == 0:
                await before.channel.delete()
                self.lobby_number -= 1

        if after.channel and after.channel.name.startswith("New lobby"):
            desired_limit = int(after.channel.name.split()[-1])
            guild = member.guild
            category = after.channel.category
            new_channel_name = f"Lobby {self.lobby_number}"
            new_channel = await guild.create_voice_channel(name=new_channel_name, category=category, user_limit=desired_limit)
            
            await member.move_to(new_channel)
            self.lobby_number += 1

def setup(bot):
    bot.add_cog(LobbyLogic(bot))