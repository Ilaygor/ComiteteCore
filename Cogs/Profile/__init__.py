import discord
from discord.ext import commands
from . import PictureCreator,SQLWorker
import os

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
                PictureCreator.SetBG(ctx.guild.id,ctx.author.id,urltoPic)
                path=PictureCreator.CreateProfile(ctx.author)
                file=discord.File(path,filename="profile.png")
                await ctx.send(file=file)
                os.remove(path)
            except:
                await ctx.send('Некорректная ссылка на изображение.')
        else:
            await ctx.send('Отсутсвует ссылка на изображение.')

    @commands.command(name="settext", help="Задаёт подпись профиля.",usage="[Информация]",brief="Информация пользователя")
    async def settext(self,ctx,*args):
        SQLWorker.SetInfo(ctx.author.id,ctx.guild.id," ".join(args))
        path=PictureCreator.CreateProfile(ctx.author)
        file=discord.File(path,filename="profile.png")
        await ctx.send(file=file)
        os.remove(path)


def setup(client):
    client.add_cog(Profile(client))