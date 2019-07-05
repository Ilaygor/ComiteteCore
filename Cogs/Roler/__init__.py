import discord
from discord.ext import commands
import datetime
from . import SQLWorker

class Roler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        if not member.bot:        
            for i in SQLWorker.GetRoles(member.guild.id,member.id):
                await member.add_roles(member.guild.get_role(int(i[0])))

    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        if len(before.roles)< len(after.roles):
            for i in after.roles:
                if not i in before.roles and not SQLWorker.CheckRole(after.guild.id,after.id,i.id):
                    SQLWorker.AddRoles(after.guild.id,after.id,i.id)
        
        if len(before.roles)> len(after.roles):
            for i in before.roles:
                if not i in after.roles:
                    SQLWorker.DelRole(i.id)

def setup(client):
    client.add_cog(Roler(client))