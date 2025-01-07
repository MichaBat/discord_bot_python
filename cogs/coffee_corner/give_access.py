import disnake
from disnake.ext import commands
from config import COFFEE_CLUB_ID
from typing import Union

class GiveAccess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_id = COFFEE_CLUB_ID
        self.authorized_users = [359052462579253261, 186419431893630976]
        self.category_name = "☕Coffee Corner☕"
        self.protected_channel_id = 1265619448325476474

    async def cog_check(self, ctx):
        return (ctx.author.id in self.authorized_users and 
            ctx.channel.id == self.protected_channel_id)


    async def find_member(self, ctx, member_name: str):
        # Remove '@' if it's at the start of the name
        if member_name.startswith('@'):
            member_name = member_name[1:]
        
        # Try to find the member by name or nickname
        member = disnake.utils.find(lambda m: member_name.lower() in (m.name.lower(), m.display_name.lower()), ctx.guild.members)
        
        if member is None:
            # If not found, try using the MemberConverter as a fallback
            try:
                member = await commands.MemberConverter().convert(ctx, member_name)
            except commands.MemberNotFound:
                member = None
        
        return member

    @commands.command()
    async def give_coffee(self, ctx, *, member_name: str):
        member = await self.find_member(ctx, member_name)
        if member is None:
            await ctx.send(f"Could not find a member named {member_name}")
            return

        print(member.id)
        role = ctx.guild.get_role(self.role_id)
        if role is None:
            await ctx.send("The specified role doesn't exist.")
            return
        
        if role in member.roles:
            await ctx.send(f"{member.mention} already has the role.")
        else:
            await member.add_roles(role)
            await ctx.send(f"The role has been given to {member.mention}. \nThey now have access to the coffee corner!")

    @commands.command()
    async def remove_coffee(self, ctx, *, member_name: str):
        member = await self.find_member(ctx, member_name)
        if member is None:
            await ctx.send(f"Could not find a member named {member_name}")
            return

        role = ctx.guild.get_role(self.role_id)
        if role is None:
            await ctx.send("The specified role doesn't exist.")
            return
        
        if role not in member.roles:
            await ctx.send(f"{member.mention} doesn't have the role.")
        else:
            await member.remove_roles(role)
            await ctx.send(f"The role has been removed from {member.mention}. \nThey no longer have access to the coffee corner!")



    async def get_or_create_category(self, ctx):
        category = disnake.utils.get(ctx.guild.categories, name=self.category_name)
        if category is None:
            category = await ctx.guild.create_category(self.category_name)
        return category

    @commands.command()
    async def coffee_create_text(self, ctx, channel_name: str):
        category = await self.get_or_create_category(ctx)
        text_channel = await ctx.guild.create_text_channel(channel_name, category=category)
        await ctx.send(f"Created text channel {text_channel.mention} in the {category.name} category")

    @commands.command()
    async def coffee_create_voice(self, ctx, channel_name: str):
        category = await self.get_or_create_category(ctx)
        voice_channel = await ctx.guild.create_voice_channel(channel_name, category=category)
        await ctx.send(f"Created voice channel {voice_channel.name} in the {category.name} category")

    @commands.command()
    async def coffee_remove_channel(self, ctx, channel: Union[disnake.TextChannel, disnake.VoiceChannel]):
        category = await self.get_or_create_category(ctx)
        
        if channel.category != category:
            await ctx.send(f"This channel is not in the {self.category_name} category.")
            return
        
        if channel.id == self.protected_channel_id:
            await ctx.send("This channel is protected and cannot be removed.")
            return
        
        await channel.delete()
        await ctx.send(f"The channel {channel.name} has been removed from the {self.category_name} category.")

def setup(bot):
    bot.add_cog(GiveAccess(bot))