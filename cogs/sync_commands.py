import disnake
from disnake.ext import commands

class SyncCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = 186419431893630976

    @commands.command(name="sync")
    async def sync(self, ctx):
        if ctx.author.id != self.owner_id:
            await ctx.send("You do not have permission to use this command.")
            return
            
        synced = await self.bot.sync_commands()
        await ctx.send(f"Slash commands synced. {len(synced)} commands registered.")

def setup(bot):
    bot.add_cog(SyncCommandsCog(bot))
