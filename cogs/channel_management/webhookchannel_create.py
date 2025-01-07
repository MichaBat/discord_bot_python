import disnake
from disnake.ext import commands

class WebhookManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category_id = 1285634397520924814  # Set your category ID here

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user}!')

    # Command to create a channel with an emoji and set up webhook
    @commands.command(name="create_webhook_channel")
    @commands.has_permissions(manage_channels=True)
    async def create_webhook_channel(self, ctx, channel_name: str, emoji: str = ""):
        # Fetch the category object
        category = disnake.utils.get(ctx.guild.categories, id=self.category_id)

        if category is None:
            await ctx.send("Category not found.")
            return

        # Create the channel with the emoji (Unicode emojis will work)
        if emoji:
            channel_name = f"{emoji} {channel_name}"

        # Ensure the channel name is valid (replace spaces and handle emoji limitations)
        channel_name = channel_name.replace(" ", "-")  # Discord doesn't allow spaces in channel names
        channel = await ctx.guild.create_text_channel(name=channel_name, category=category)

        # Create the webhook for the newly created channel
        webhook = await channel.create_webhook(name=f"{channel_name}_webhook")

        # Send the webhook URL in the newly created channel
        await channel.send(f"Webhook URL: {webhook.url}")

        # Optionally, send a confirmation message in the channel where the command was called
        await ctx.send(f"Channel '{channel_name}' created with a webhook.")

# Setup function to add this cog to the bot
def setup(bot):
    bot.add_cog(WebhookManager(bot))
