import discord
from discord.ext.commands import TextChannelConverter
from discord.ext import commands
from . import SQLWorker
from datetime import datetime

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

    @commands.command(name="ignor" , help="Игнор-лист, для того чтобы бот не защитывал XP или упоминания в каналах админа сервера.\nНапример добавьте в игнор-лист каналы в которых предназначенные для флуда или каналы предназначенные для ботов.\nДействия:\n> list - выводит список игнорируемых каналов.\n> add - добавляет канал в список игнорируемых каналов, требует пинг канала.\n> rem - девушка с голубыми волосами, близнец ram... Не та Информация, т.е. данное действие отвечает за удаление канала из игнор листа, требует пинг канала.",usage="[Действие == list] [Канал]",brief="Игнор-лист")
    @is_owner()
    async def ignor(self,ctx,action:str="list", channel=None):
        if action=="list":
            IgnorList=SQLWorker.GetIgnorList(ctx.guild.id)
            embed=discord.Embed(title="Cписок игнорируемых каналов:", description="Каналы в которых бот не учитывает XP.")
            for i in IgnorList:
                embed.add_field(name=ctx.guild.get_channel(i[0]).name,inline=False,value="Добавлен: "+str(datetime.fromtimestamp(i[1]).date()))
            await ctx.send(embed=embed)
        elif action == "add":
            if channel:
                ch=await TextChannelConverter().convert(ctx,channel)
                if not SQLWorker.checkChennel(ctx.guild.id,ch.id):
                    SQLWorker.AddIgnorList(ch.id,ctx.guild.id)
                    embed=discord.Embed(title="Канал {} успешно добавлен в список игнора.".format(ch.name))
                    await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title="Канал {} уже добавлен в список игнора.".format(ch.name))
                    await ctx.send(embed=embed)
            else:
                await ctx.send("Не указан канал!")
        elif action == "rem":
            if channel:
                ch=await TextChannelConverter().convert(ctx,channel)
                if SQLWorker.checkChennel(ctx.guild.id,ch.id):
                    SQLWorker.DelIgnorList(ch.id,ctx.guild.id)
                    embed=discord.Embed(title="Канал {} успешно удалён из списока игнора.".format(ch.name))
                    await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title="Канал {} отсутсвует в списоке игнора.".format(ch.name))
                    await ctx.send(embed=embed)
            else:
                await ctx.send("Не указан канал!")
        else:
            await ctx.send("Неизвестное действие.")

def setup(client):
    client.add_cog(Settings(client))