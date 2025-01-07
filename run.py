#!/usr/bin/env python3
import disnake
from disnake.ext import commands
from clients.custom_bot_client import CustomBotClient
from config import TOKEN, PREFIX
import asyncio

async def main():
    
    command_sync_flags = commands.CommandSyncFlags.default()
    command_sync_flags.sync_commands_debug = True
    
    intents = disnake.Intents.all()

    bot = CustomBotClient(
        command_prefix=PREFIX,
        intents=intents,
        command_sync_flags=command_sync_flags,
    )
    
    tasks = [
        asyncio.create_task(bot.load_extension('cogs.command_err_handler')),
        asyncio.create_task(bot.load_extension('cogs.sync_commands')),
        asyncio.create_task(bot.load_extension('cogs.lobby_logic.lobby_creation')),
        
        
        asyncio.create_task(bot.load_extension('cogs.daily_messages.meditation_notification')),
        asyncio.create_task(bot.load_extension('cogs.daily_messages.daily_question')),
        asyncio.create_task(bot.load_extension('cogs.daily_messages.DailyStandupReminder')),
        asyncio.create_task(bot.load_extension('cogs.daily_messages.Paul')),
        
        
        asyncio.create_task(bot.load_extension('cogs.buttons.button_roles')),
        asyncio.create_task(bot.load_extension('cogs.buttons.add_button_to_message')),
        
        asyncio.create_task(bot.load_extension('cogs.gaming_logic.gaming_role_logic')), 
        asyncio.create_task(bot.load_extension('cogs.role_logic.cool_clubs')),
        
        asyncio.create_task(bot.load_extension('cogs.gaming_logic.create_game')),
        
        asyncio.create_task(bot.load_extension('cogs.birthday_logic.birthday_set')),
        asyncio.create_task(bot.load_extension('cogs.birthday_logic.birthday_get')),
        asyncio.create_task(bot.load_extension('cogs.birthday_logic.birthday_reminder')),
        asyncio.create_task(bot.load_extension('cogs.moderation.moderation_logic')),
        asyncio.create_task(bot.load_extension('cogs.coffee_corner.give_access')),
        asyncio.create_task(bot.load_extension('cogs.region_logic.overview')),
        #asyncio.create_task(bot.load_extension('cogs.polls.time_poll')),
        asyncio.create_task(bot.load_extension('cogs.timestamp_logic.timestamp')),
        
        #/cogs/channel_management
        asyncio.create_task(bot.load_extension('cogs.channel_management.empty_text_channel')),
        asyncio.create_task(bot.load_extension('cogs.channel_management.webhookchannel_create')),
        asyncio.create_task(bot.load_extension('cogs.Gitlab.verifynotification'))
        
        #,asyncio.create_task(bot.load_extension('cogs.buttons.cool_clubs_buttons')),           
        #asyncio.create_task(bot.load_extension('cogs.buttons.send_buttons')),
        #asyncio.create_task(bot.load_extension('cogs.gaming_logic.roles.gaming_role_message')),
    ]
    
    await asyncio.gather(*tasks)
    
    
    try:  
        await bot.start(TOKEN)
    finally:
        await bot.close()
        print("bot closed")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting gracefully...")

