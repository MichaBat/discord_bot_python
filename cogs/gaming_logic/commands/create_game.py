import disnake
from disnake.ext import commands


class AddGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="hello", description="Says hello to you")
    async def hello(self, ctx: commands.SlashContext):
        await ctx.send(f"Hello {ctx.author.mention}!")
def setup(bot):
    bot.add_cog(AddGame(bot))