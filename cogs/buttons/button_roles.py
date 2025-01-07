import disnake
from disnake.ext import commands

class ButtonInteractionHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: disnake.MessageInteraction):
        if interaction.type == disnake.InteractionType.component:
            custom_id = interaction.component.custom_id

            if custom_id.startswith("region_"):
                await self.handle_region_button(interaction)
            elif custom_id.startswith("event_"):
                await self.handle_event_button(interaction)
            elif custom_id == "voice_chat_nerds":
                await self.handle_voice_chat_nerds(interaction)

    async def handle_region_button(self, interaction):
        role_names = {
            'region_Africa': 'Africa',
            'region_Asia': 'Asia',
            'region_Europe': 'Europe',
            'region_North_America': 'North America',
            'region_South_America': 'South America',
            'region_Australia': 'Australia'
        }

        custom_id = interaction.component.custom_id
        role_name = role_names.get(custom_id)
        if role_name:
            member = interaction.user
            guild = self.bot.get_guild(1237748265345355848)
            role = disnake.utils.get(guild.roles, name=role_name)
            regions_role = guild.get_role(1240213903036649534)

            if role in member.roles:
                await member.remove_roles(role)
                await interaction.response.send_message(f"Role {role_name} removed successfully!", ephemeral=True)

                if all(disnake.utils.get(guild.roles, name=role) not in member.roles for role in role_names.values()):
                    await member.remove_roles(regions_role)
            else:
                current_region_roles = [disnake.utils.get(guild.roles, name=role) for role in role_names.values() if disnake.utils.get(guild.roles, name=role) in member.roles]

                if current_region_roles:
                    await interaction.response.send_message("You already have a region role. Please remove it before assigning a new one.", ephemeral=True)
                else:
                    if regions_role not in member.roles:
                        await member.add_roles(regions_role)

                    await member.add_roles(role)
                    await interaction.response.send_message(f"Role {role_name} assigned successfully!", ephemeral=True)

    async def handle_event_button(self, interaction):
        guild = interaction.guild
        member = interaction.author

        role_dict = {
            "event_movie_show_night": "Movie / Show Nights",
            "event_game_night": "Game Nights",
            "event_quiz_night": "Quiz Nights",
            "event_music_night": "Music Nights",
            "event_art_night": "Art Nights",
        }

        events_role_name = "⌦━━━━━━━━ Events ━━━━━━━━━━⌫"
        role_name = role_dict.get(interaction.data.custom_id)

        if role_name:
            role = disnake.utils.get(guild.roles, name=role_name)
            events_role = disnake.utils.get(guild.roles, name=events_role_name)

            if not role:
                await interaction.response.send_message(f"Role '{role_name}' not found!", ephemeral=True)
                return

            if role in member.roles:
                await member.remove_roles(role)
                await interaction.response.send_message(f"Removed {role_name} role!", ephemeral=True)

                user_event_roles = [r for r in member.roles if r.name in role_dict.values()]
                if len(user_event_roles) == 0 and events_role in member.roles:
                    await member.remove_roles(events_role)
            else:
                await member.add_roles(role)
                await interaction.response.send_message(f"Added {role_name} role!", ephemeral=True)

                user_event_roles = [r for r in member.roles if r.name in role_dict.values()]
                if len(user_event_roles) == 1 and events_role not in member.roles:
                    await member.add_roles(events_role)

    async def handle_voice_chat_nerds(self, interaction):
        role = interaction.guild.get_role(1254414248436826123)
        if role:
            if role in interaction.author.roles:
                await interaction.author.remove_roles(role)
                await interaction.send(f"The {role.name.lower()} role has been removed from you!", ephemeral=True)
            else:
                await interaction.author.add_roles(role)
                await interaction.send(f"You have been given the {role.name} role!", ephemeral=True)
        else:
            await interaction.send("Role not found!", ephemeral=True)

def setup(bot):
    bot.add_cog(ButtonInteractionHandler(bot))