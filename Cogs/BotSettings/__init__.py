import discord
from discord.ext.commands import TextChannelConverter
from discord.ext import commands
from . import SQLWorker

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == ctx.guild.owner_id or ctx.author.id == 269860812355665921
    return commands.check(predicate)

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="audit",help="Производит аудит пользователей сервера, т.е. смотрит какие пользователи присутсвуют, а какие отсутсвуют и производит учёт.\n Полезно, когда пришёл новый пользователь, а бот был в отключке.",usage="",brief="Аудит сервера")
    @is_owner()
    async def audit(self,ctx):
        memlist={}
        for mem in SQLWorker.GetMembers(ctx.guild.id):
            memlist.update({mem[0]:mem[1]})

        for mem in ctx.guild.members:
            if memlist.get(mem.id):
                if memlist[mem.id]==1:
                    memlist.pop(mem.id)
                else:
                    SQLWorker.SetAlive(mem.id)
            else:
                SQLWorker.AddNewmem(ctx.guild.id,mem.id)

        for mem in memlist.keys():
            if memlist[mem]==1:
                SQLWorker.SetDead(mem)
        
        await ctx.send("Audit completed!")
       

    @commands.command(name="setinfo", help="Задаёт канал для вывода сообщений об приходе/уходе/возвращение пользователей.",usage="ПингКанала",brief="Устанавливает информационный канал")
    @is_owner()
    async def setinfo(self,ctx,channel):
        ch=await TextChannelConverter().convert(ctx,channel)
        SQLWorker.SetInfoChan(ctx.guild.id,ch.id)
        await ctx.send("InfoChan changed for {}".format(channel))


def setup(client):
    client.add_cog(Settings(client))