import disnake
from disnake.ext import commands
import asyncio

class DeleteAll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delete_all(self, ctx):
        # Confirm with the user before proceeding
        await ctx.send("Are you sure you want to delete all messages in this channel? Type `yes` to confirm.")
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == 'yes'
        
        try:
            # Wait for the user's confirmation
            await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Confirmation timed out. Operation canceled.")
        else:
            # Delete all messages in the channel
            await ctx.channel.purge(limit=None)
            await ctx.send("All messages in this channel have been deleted.")

    @delete_all.error
    async def delete_all_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to manage messages.")

def setup(bot):
    bot.add_cog(DeleteAll(bot))