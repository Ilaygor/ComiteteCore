import discord
from discord.ext import commands

class Cleaner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="clear",help="Чистит канал от сообщений бота. Требует пинг (#канал) и число последних сообщений.",usage="#Канал Число",brief="Чистка канала от бота")
    async def clear(self,ctx,channel,count):
        channel=await commands.TextChannelConverter().convert(ctx,channel)
        async for i in channel.history(limit=int(count)):
            if i.author.id==self.bot.user.id:
                await i.delete()

def setup(client):
    client.add_cog(Cleaner(client))