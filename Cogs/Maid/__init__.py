import discord
from discord.ext import commands
from . import ExpSys,PictureCreator,SQLWorker
import os
import re

class Maid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        ExpSys.init()

    @commands.command(name="avatar", help="Выводит аватар пользователя. Можно сделать пинг (@Пользовтель) чтобы получить аватар другого пользователя.",usage="[@Пользователь]",brief="Аватар")
    async def avatar(self,ctx,member=None):
        if (member):
            author=await commands.MemberConverter().convert(ctx,member)
        else:
            author=ctx.author

        path=PictureCreator.GetAvatarFromUrl(author.avatar_url_as(size=4096))
        file=discord.File(path,filename="avatar.png")
        await ctx.send("Avatar "+author.name,file=file)

    @commands.command(name="rank", help="Выводит ранг пользователя. Можно сделать пинг (@Пользовтель) чтобы получить информацию о ранге пользователя.",usage="[@Пользователь]",brief="Ранг")
    async def rank(self,ctx,member=None):
        if (member):
            author=await commands.MemberConverter().convert(ctx,member)
        else:
            author=ctx.author
        path=PictureCreator.CreateRank(author)
        file=discord.File(path,filename="profile.png")
        await ctx.send(file=file)
        os.remove(path)

    @commands.command(name="top", help="Выводит рейтинг сервера.\nТипы:\n> exp - выводит рейтинг пользователей основываясь на опыте получнном пользователями.\n> men - выводит рейтинг пользователей основываясь на количестве упоминания пользователей.\n> emoji - выводит рейтинг основываясь на количестве сообщений с эмоджи.",usage="[Тип == exp]",brief="Рейтинг пользователей")
    async def top(self,ctx,cat:str="exp", page:int=1):
        members=[]
        page=int(page)
        if cat.isnumeric():
            page=int(cat)
            cat="exp"

        if cat == 'exp':
            for i in SQLWorker.GetTopMembers(page-1,ctx.guild.id):
                mem=ctx.guild.get_member(i[0])
                members.append({
                    "mem":mem,
                    "url":mem.avatar_url_as(size=64),
                    "data":PictureCreator.ConvrterToCI(round(i[1],2))+" xp"
                })
        elif cat=="men":
            for i in SQLWorker.GetTopMenMembers(page-1,ctx.guild.id):
                mem=ctx.guild.get_member(i[0])
                
                members.append({
                    "mem":mem,
                    "url":mem.avatar_url_as(size=64),
                    "data":str(i[1])+" mentions"
                })
        elif cat=="emoji":
            for i in SQLWorker.GetTopEmojiMembers(page-1,ctx.guild.id):
                emoji=await ctx.guild.fetch_emoji(i[0])
                
                members.append({
                    "mem":emoji,
                    "url":emoji.url,
                    "data":str(i[1])+" detected"
                })
        else:
            await ctx.send("Параметр не найден!")
            return

        path=PictureCreator.GetTop(members,page-1)
        file=discord.File(path,filename="top.png")
        await ctx.send(file=file)
        os.remove(path)


    @commands.Cog.listener()
    async def on_member_join(self,member):
        if not member.bot:        
            ExpSys.AddMem(member.id,member.guild.id)
 
    
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        if not member.bot:
            ExpSys.DelMem(member.id,member.guild.id)

    @commands.Cog.listener()
    async def on_message(self,message):
        #await self.bot.process_commands(message)
        if not message.author.bot and not ExpSys.checkChennel(message.guild.id,message.channel.id):
            if (len(message.mentions)):
                for i in list(set(message.mentions)):
                    if not i.bot and not message.author.bot and not i.id==message.author.id:
                        ExpSys.AddMention(i.id,message.guild.id)
            await ExpSys.AddExp(message.author.id,message.guild.id,len(message.content)/10,message.channel)
        
            ctx = await self.bot.get_context(message)
            for emoji in list(set(re.findall("<\D+\d+>",message.content))):
                try:
                    emj=await commands.EmojiConverter().convert(ctx,emoji)
                    SQLWorker.IncEmoji(message.guild.id,emj.id)
                except commands.errors.BadArgument:
                    pass

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        for mem in guild.members:
            ExpSys.AddMem(mem.id,guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        for mem in guild.members:
            ExpSys.DelMem(mem.id,guild.id)

def setup(client):
    client.add_cog(Maid(client))