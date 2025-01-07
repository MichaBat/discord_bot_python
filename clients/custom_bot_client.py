import disnake
from disnake.ext import commands


class CustomBotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         

    async def on_ready(self):
        await self.change_presence(activity=disnake.Game(name="Is that a bone you threw?"))
        print(f'{self.user.name} has connected to Discord!')
        
        print(f"Number of slash commands: {len(self.slash_commands)}")
        
        try:
            synced = await self.sync_all_commands()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(f"Failed to sync commands: {e}")
        
    async def load_extension(self, name):
        try:
            super().load_extension(name)
            print(f'Loaded extension: {name}')
        except Exception as e:
            print(f'Failed to load extension {name}: {e}')
            raise  

        return True
                
    async def async_cleanup(self): 
        print("Cleaning up!")

    async def close(self):

        await self.async_cleanup()
        
        await super().close() 