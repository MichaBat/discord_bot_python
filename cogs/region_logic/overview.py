import os
import disnake
from disnake.ext import commands, tasks
from config import GUILD_ID, REGION_ROLES_IDS, REGION_OVERVIEW_CHANNEL_ID

ROLE_IDS =  REGION_ROLES_IDS
CHANNEL_ID = REGION_OVERVIEW_CHANNEL_ID 

class Region(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.previous_message_id = None
        self.member_list_file = os.path.join(os.path.dirname(__file__), "members_roles.txt")
        self.update_member_list.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user}')

    def get_role_members(self, guild):
        role_members = {}
        for role_id in ROLE_IDS:
            role = guild.get_role(role_id)
            if role:
                role_members[role.name] = [member for member in role.members]
        return role_members

    def save_members_to_file(self, role_members):
        with open(self.member_list_file, 'w') as file:
            for role, members in role_members.items():
                file.write(f"{role}:\n")
                for member in members:
                    file.write(f"- {member.display_name} ({member.id})\n")

    def load_members_from_file(self):
        if not os.path.exists(self.member_list_file):
            return {}
        with open(self.member_list_file, 'r') as file:
            data = file.read().strip().split('\n')
            role_members = {}
            current_role = None
        for line in data:
            if line.endswith(':'):
                current_role = line[:-1]
                role_members[current_role] = []
            elif current_role:
                member_info = line.split('(')
                member_name = member_info[0].strip()[2:]
                # Strip whitespace and the closing parenthesis, then convert to int
                member_id_str = member_info[1].strip().rstrip(')')
                member_id = int(member_id_str)
                role_members[current_role].append((member_name, member_id))
        return role_members


    def has_member_list_changed(self, old_list, new_list):
        if old_list.keys() != new_list.keys():
            return True
        for role in old_list:
            if sorted(old_list[role]) != sorted([(m.display_name, m.id) for m in new_list[role]]):
                return True
        return False

    def create_embed(self, role_members):
        embed = disnake.Embed(title="Role Members", color=disnake.Color.blue())
        for role, members in role_members.items():
            member_mentions = "\n".join([member.mention for member in members])
            embed.add_field(name=role, value=member_mentions or "No members", inline=False)
        return embed

    @tasks.loop(hours=1)
    async def update_member_list(self):
        guild = self.bot.get_guild(GUILD_ID)
        if not guild:
            return

        role_members = self.get_role_members(guild)
        old_role_members = self.load_members_from_file()

        if self.has_member_list_changed(old_role_members, role_members):
            channel = guild.get_channel(CHANNEL_ID)
            if not channel:
                return
            
            await channel.purge(limit=None)

            embed = self.create_embed(role_members)
            if self.previous_message_id:
                try:
                    previous_message = await channel.fetch_message(self.previous_message_id)
                    await previous_message.delete()
                except disnake.NotFound:
                    pass

            message = await channel.send(embed=embed)
            self.previous_message_id = message.id
            self.save_members_to_file(role_members)

def setup(bot):
    bot.add_cog(Region(bot))
