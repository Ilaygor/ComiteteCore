import discord
from discord.ext.commands import TextChannelConverter,RoleConverter
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
                    SQLWorker.SetAlive(mem.id,ctx.guild.id)
            else:
                SQLWorker.AddNewmem(ctx.guild.id,mem.id)

        for mem in memlist.keys():
            if memlist[mem]==1:
                SQLWorker.SetDead(mem,ctx.guild.id)
        

        for mem in ctx.guild.members:
            for role in mem.roles:
                if not SQLWorker.CheckRole(ctx.guild.id,mem.id,role.id) and not role.is_default():
                    SQLWorker.AddRoles(ctx.guild.id,mem.id,role.id)                    

        for emoji in ctx.guild.emojis:
            if not SQLWorker.CheckEmoji(ctx.guild.id,emoji.id):
                SQLWorker.AddEmoji(ctx.guild.id,emoji.id)

        await ctx.send("Audit completed!")
       

    @commands.command(name="setinfo", help="Задаёт канал для вывода сообщений об приходе/уходе/возвращение пользователей.",usage="ПингКанала",brief="Устанавливает информационный канал")
    @is_owner()
    async def setinfo(self,ctx,channel):
        ch=await TextChannelConverter().convert(ctx,channel)
        SQLWorker.SetInfoChan(ctx.guild.id,ch.id)
        await ctx.send("InfoChan changed for: {}".format(channel))

    @commands.command(name="setjoinrole", help="Задаёт роль для пользовтелей который только-что присоединились.",usage="Название роли",brief="Устанавливает роль для новичков")
    @is_owner()
    async def setjoinrole(self,ctx,rolename=None):
        if rolename:
            role=await RoleConverter().convert(ctx,rolename)
            SQLWorker.SetJoinRole(ctx.guild.id,role.id)
            await ctx.send("Join role changed for: {}".format(rolename))
        else:
            SQLWorker.SetJoinRole(ctx.guild.id,rolename)
            await ctx.send("Join role cleared")

    @commands.command(name="setmemname", help="Устанавливает называние при приходе/уходе/возвращение пользователей на сервер.",usage="[Строка обозначающее имя участника канала == Member]",brief="Устанавливает имя участника сервера")
    @is_owner()
    async def setmemname(self,ctx,name="Member"):
        SQLWorker.SetMemName(ctx.guild.id,name)
        await ctx.send("Member name changed for: {}".format(name))
    
    @commands.command(name="setbantext", help="Устанавливает текст при бане пользователя на сервере.",usage="[Сроки обозначающие, что пользовтатель был забанен == has been banned.]",brief="Устанавливает текст при бане пользователя на сервере.")
    @is_owner()
    async def setbantext(self,ctx,*args):
        text=' '.join(args)
        if len (text)==0:
            text = 'has been banned.'
        SQLWorker.SetBanText(ctx.guild.id,text)
        await ctx.send("Ban text changed for: {}".format(text))

    @commands.command(name="ignor" , help="Игнор-лист, для того чтобы бот не защитывал XP, упоминания или эмодзи в каналах админа сервера.\nНапример добавьте в игнор-лист каналы в которых предназначенные для флуда или каналы предназначенные для ботов.\nДействия:\n> list - выводит список игнорируемых каналов.\n> add - добавляет канал в список игнорируемых каналов, требует пинг канала.\n> rem - девушка с голубыми волосами, близнец ram... Не та Информация, т.е. данное действие отвечает за удаление канала из игнор листа, требует пинг канала.",usage="[Действие == list] [Канал]",brief="Игнор-лист")
    @is_owner()
    async def ignor(self,ctx,action:str="list", channel=None):
        if action=="list":
            IgnorList=SQLWorker.GetIgnorList(ctx.guild.id)
            embed=discord.Embed(title="Cписок игнорируемых каналов:", description="Каналы в которых бот не учитывает XP.")
            for i in IgnorList:
                channel=ctx.guild.get_channel(i[0])
                if channel:
                    embed.add_field(name=channel.name,inline=False,value="Добавлен: "+str(datetime.fromtimestamp(i[1]).date()))
                else:
                    SQLWorker.DelIgnorList(i[0],ctx.guild.id)
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

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        if not SQLWorker.CheckServer(guild.id):
            import os
            os.mkdir("src/Images/Usr/"+str(guild.id))
            SQLWorker.AddServer(guild.id)
            for mem in guild.members:
                SQLWorker.AddNewmem(guild.id,mem.id)
        else:
            memlist={}
            for mem in SQLWorker.GetMembers(guild.id):
                memlist.update({mem[0]:mem[1]})
            for mem in guild.members:
                if memlist.get(mem.id):
                    if memlist[mem.id]==1:
                        memlist.pop(mem.id)
                    else:
                        SQLWorker.SetAlive(mem.id,guild.id)
                else:
                    SQLWorker.AddNewmem(guild.id,mem.id)
            for mem in memlist.keys():
                if memlist[mem]==1:
                    SQLWorker.SetDead(mem,guild.id)
        
        for mem in guild.members:
            for role in mem.roles:
                if not SQLWorker.CheckRole(guild.id,mem.id,role.id) and not role.is_default():
                    SQLWorker.AddRoles(guild.id,mem.id,role.id)                    

        for emoji in guild.emojis:
            if not SQLWorker.CheckEmoji(guild.id,emoji.id):
                SQLWorker.AddEmoji(guild.id,emoji.id)


def setup(client):
    client.add_cog(Settings(client))