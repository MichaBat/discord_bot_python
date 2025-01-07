import disnake
from disnake.ext import commands
from config import COOL_CLUBS_IDS

class CoolClubs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_button_click")
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id.startswith("cool_club_"):
            club_id_parts = inter.component.custom_id.split("_")
            new_club_id = int(club_id_parts[2])
            new_role = inter.guild.get_role(new_club_id)
            
            if new_role is None:
                await inter.response.send_message(f"Error: Role with ID {new_club_id} not found.", ephemeral=True)
                return

            # Remove user from all other cool clubs
            roles_to_remove = [inter.guild.get_role(club_id) for club_id in set(COOL_CLUBS_IDS) if club_id != new_club_id]
            roles_to_remove = [role for role in roles_to_remove if role is not None and role in inter.author.roles]
            
            if roles_to_remove:
                await inter.author.remove_roles(*roles_to_remove)
                removed_roles = ", ".join([role.name for role in roles_to_remove])
                await inter.response.send_message(f"You left {removed_roles}.", ephemeral=True)

            # Add user to the new club
            if new_role not in inter.author.roles:
                await inter.author.add_roles(new_role)
                await inter.followup.send(f"You joined {new_role.name}!", ephemeral=True)
            else:
                await inter.followup.send(f"You're already in {new_role.name}!", ephemeral=True)
                
def setup(bot):
    bot.add_cog(CoolClubs(bot))