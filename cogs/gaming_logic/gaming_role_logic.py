import disnake
from disnake.ext import commands
from .games_roles import games_roles

special_role_name = "⌦━━━━━━━━ Games ━━━━━━━━━━⌫"
message_ids = [1260503979541008386, 1260504056607150172, 1260504139666821173]

class GameRoleHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_special_role(self, member, guild):
        special_role = disnake.utils.get(guild.roles, name=special_role_name)
        if special_role is None:
            print(f"Special role {special_role_name} does not exist.")
            return

        game_roles_count = sum(1 for role in member.roles if role.name in games_roles.values())

        if game_roles_count > 0 and special_role not in member.roles:
            await member.add_roles(special_role)
        elif game_roles_count == 0 and special_role in member.roles:
            await member.remove_roles(special_role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: disnake.RawReactionActionEvent):
        if payload.guild_id is None:
            return

        if payload.message_id not in message_ids:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        role_name = games_roles.get(payload.emoji.name)
        if role_name is None:
            return

        role = disnake.utils.get(guild.roles, name=role_name)
        if role is None:
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            return

        try:
            await member.add_roles(role)
            await self.update_special_role(member, guild)
        except disnake.HTTPException as e:
            print(f"Failed to add role {role_name} to {member.display_name}: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: disnake.RawReactionActionEvent):
        if payload.guild_id is None:
            return

        if payload.message_id not in message_ids:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        role_name = games_roles.get(payload.emoji.name)
        if role_name is None:
            return

        role = disnake.utils.get(guild.roles, name=role_name)
        if role is None:
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            return

        try:
            await member.remove_roles(role)
            await self.update_special_role(member, guild)
        except disnake.HTTPException as e:
            print(f"Failed to remove role {role_name} from {member.display_name}: {e}")

def setup(bot):
    bot.add_cog(GameRoleHandler(bot))
