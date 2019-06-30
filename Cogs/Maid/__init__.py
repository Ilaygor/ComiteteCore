import discord
from discord.ext import commands
from . import ExpSys,PictureCreator,SQLWorker
import os

class Maid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        ExpSys.init()

    @commands.command(name="clear",help="Чистит канал от сообщений бота. Требует пинг (#канал) и число последних сообщений.",usage="#Канал Число",brief="Чистка канала от бота")
    async def clear(self,ctx,channel,count):
        channel=await commands.TextChannelConverter().convert(ctx,channel)
        async for i in channel.history(limit=int(count)):
            if i.author.id==self.bot.user.id:
                await i.delete()

    @commands.command(name="profile", help="Выводит профиль пользователя. Можно сделать пинг (@Пользовтель) чтобы получить информацию о профиле пользователя.",usage="[@Пользователь]",brief="Профиль")
    async def profile(self,ctx,member=None):
        if (member):
            author=await commands.MemberConverter().convert(ctx,member)
        else:
            author=ctx.author
        path=PictureCreator.CreateProfile(author)
        file=discord.File(path,filename="profile.png")
        await ctx.send(file=file)
        os.remove(path)

    @commands.command(name="setbg", help="Устанавливает задний фон для профиля. Требуется приложить изображение или рабочую ссылку на изображение. Можно вместо ссылки указать **clear**, чтобы удалить фон.",usage="[Ссылка]",brief="Задник профиля")
    async def setbg(self,ctx,url=None):
        if url=="clear":
            os.remove("src/Images/Usr/"+str(ctx.author.id)+"/profile.png")
            await ctx.send('Задний фон удалён.')
        elif url or ctx.message.attachments[0].height:
            try:
                if url:
                    urltoPic=url
                else:
                    urltoPic=ctx.message.attachments[0].url
                PictureCreator.SetBG(ctx.author.id,urltoPic)
                path=PictureCreator.CreateProfile(ctx.author)
                file=discord.File(path,filename="profile.png")
                await ctx.send(file=file)
                os.remove(path)
            except:
                await ctx.send('Некорректная ссылка на изображение.')
        else:
            await ctx.send('Отсутсвует ссылка на изображение.')

    @commands.command(name="top", help="Выводит рейтинг пользователя.\nТипы:\n> exp - выводит рейтинг пользователей основываясь на опыте получнном пользователями.\n> men - выводит рейтинг пользователей основываясь на количестве упоминаня пользователей.",usage="[Тип == exp]",brief="Рейтинг пользователей")
    async def top(self,ctx,cat:str="exp", page:int="1"):
        members=[]
        page=int(page)
        if cat == 'exp':
            for i in SQLWorker.GetTopMembers(page-1):
                members.append({
                    "mem":ctx.guild.get_member(i[0]),
                    "data":str(round(i[1],2))+" xp"
                })
        elif cat=="men":
            for i in SQLWorker.GetTopMenMembers(page-1):
                members.append({
                    "mem":ctx.guild.get_member(i[0]),
                    "data":str(round(i[1],2))+" mentions"
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
            ExpSys.AddMem(member.id)
    
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        if not member.bot:
            ExpSys.DelMem(member.id)

    @commands.Cog.listener()
    async def on_message(self,message):
        #await self.bot.process_commands(message)
        if not message.author.bot and not message.channel.id==572807088787554304:
            if (len(message.mentions)):
                for i in list(set(message.mentions)):
                    if not i.bot and not message.author.bot and not i.id==message.author.id:
                        ExpSys.AddMention(i.id)
            await ExpSys.AddExp(message.author.id,len(message.content)/10,message.channel)


def setup(client):
    client.add_cog(Maid(client))