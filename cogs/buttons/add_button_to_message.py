import disnake
from disnake.ext import commands
from disnake.ui import Button, View
from disnake import ButtonStyle

class ButtonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_button(self, ctx, button_text: str, button_color: str, role_name: str):
        role = disnake.utils.get(ctx.guild.roles, name="Master Minds")
        if role not in ctx.author.roles:
            await ctx.send("You do not have the required role to use this command.")
            return

        # Map the color input to Disnake ButtonStyle
        color_map = {
            "green": ButtonStyle.green,
            "grey": ButtonStyle.grey,
            "blurple": ButtonStyle.blurple,
            "red": ButtonStyle.red,
            "url": ButtonStyle.link,
        }

        button_color = color_map.get(button_color.lower(), ButtonStyle.blurple)

        # Find the role by name
        role_to_toggle = disnake.utils.get(ctx.guild.roles, name=role_name)
        if not role_to_toggle:
            await ctx.send(f"Role `{role_name}` not found.")
            return

        # Define the button
        button = Button(label=button_text, style=button_color)

        # Define the View
        view = View()

        # Create a callback function for the button interaction (toggle role)
        async def button_callback(interaction):
            if role_to_toggle in interaction.user.roles:
                # Remove the role if the user already has it
                await interaction.user.remove_roles(role_to_toggle)
                await interaction.response.send_message(f"The `{role_to_toggle.name}` role has been removed from you.", ephemeral=True)
            else:
                # Add the role if the user doesn't have it
                await interaction.user.add_roles(role_to_toggle)
                await interaction.response.send_message(f"You've been given the `{role_to_toggle.name}` role!", ephemeral=True)

        # Attach the callback to the button
        button.callback = button_callback

        # Add the button to the view
        view.add_item(button)

        # Send the message with the button
        await ctx.send("Click the button to toggle the role!", view=view)

# Setup the cog
def setup(bot):
    bot.add_cog(ButtonCog(bot))
