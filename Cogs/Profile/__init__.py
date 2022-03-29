import os
import re

import discord
from discord import MessageType
from discord.commands import slash_command, Option, message_command
from discord.ext import commands
from sqlalchemy import desc
from . import XpSys
import PictureCreator
from PictureCreator.utils import ConvrterToCI
from models.Emojies import Emojie
from models.IgnorLists import IgnoreList
from models.Members import Member
from models.database import Session

session = Session()


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        XpSys.init()

    @message_command(name="Получить профиль")
    async def getProfile(self, ctx, message: discord.Message):
        author = message.author
        path = "Temp/{}.png".format(author.id)
        info = session.query(Member)\
            .filter(Member.MemberId == author.id)\
            .filter(Member.ServerId == author.guild.id).first()
        PictureCreator.CreateProfile(author, info).save(path)

        file = discord.File(path, filename="profile.png")
        await ctx.send(file=file)

        os.remove(path)

    @slash_command(
        name='profile',
        description="Выводит профиль пользователя."
    )
    async def profile(self, ctx,
                      member: Option(discord.Member, description="Выберите пользователя, чей профиль вывести",
                                     required=False, default=None)):
        if member:
            author = member
        else:
            author = ctx.author

        path = "Temp/{}.png".format(author.id)
        info = session.query(Member)\
            .filter(Member.MemberId == author.id)\
            .filter(Member.ServerId == author.guild.id).first()
        PictureCreator.CreateProfile(author, info).save(path)

        file = discord.File(path, filename="profile.png")
        await ctx.send(file=file)

        os.remove(path)

    @slash_command(
        name='setbg',
        description="Устанавливает задний фон для профиля. Приложить изображение или ссылку на изображение.",
    )
    async def setbg(self, ctx,
                    img: Option(discord.Attachment, "Изображение для заднего фона", required=False, default=None),
                    url: Option(str, "Ссылка на задний фон", required=False, default=None)):
        if url:
            try:
                PictureCreator.SetBG(ctx.guild.id, ctx.author.id, url)
            except:
                await ctx.send('Некорректная ссылка на изображение.')
                return
        elif img:
            if 'image' not in img.content_type:
                await ctx.send('Некорректное изображение.')
                return
            PictureCreator.SetBG(ctx.guild.id, ctx.author.id, img.url)
        else:
            try:
                os.remove("src/Images/Usr/{}/{}/profile.png".format(ctx.guild.id, ctx.author.id))
            except:
                pass

        path = "Temp/{}.png".format(ctx.author.id)

        info = session.query(Member) \
            .filter(Member.MemberId == ctx.author.id) \
            .filter(Member.ServerId == ctx.author.guild.id).first()
        PictureCreator.CreateProfile(ctx.author, info).save(path)

        file = discord.File(path, filename="profile.png")
        await ctx.send(file=file)
        os.remove(path)

    @slash_command(
        name='settext',
        description="Задаёт подпись профиля."
    )
    async def settext(self, ctx, text: Option(str, description="Подпись профиля.", required=False, default="")):
        member = session.query(Member) \
            .filter(Member.MemberId == ctx.author.id) \
            .filter(Member.ServerId == ctx.guild.id).first()
        member.Info = text

        path = "Temp/{}.png".format(ctx.author.id)
        info = session.query(Member) \
            .filter(Member.MemberId == ctx.author.id) \
            .filter(Member.ServerId == ctx.author.guild.id).first()
        PictureCreator.CreateProfile(ctx.author, info).save(path)
        file = discord.File(path, filename="profile.png")
        await ctx.send(file=file)
        os.remove(path)

    @message_command(name="Получить аватар")
    async def getAvatar(self, ctx, message: discord.Message):
        path = PictureCreator.utils.GetAvatarFromUrl(PictureCreator.GetAvatar(message.author, size=4096))
        file = discord.File(path, filename="avatar.gif")
        await ctx.send("Avatar " + message.author.name, file=file)

    @slash_command(
        name='avatar',
        description="Выводит аватар пользователя."
    )
    async def avatar(self, ctx, member: Option(discord.Member, "Пользователь", required=False, default=None)):
        if member:
            author = member
        else:
            author = ctx.author

        path = PictureCreator.utils.GetAvatarFromUrl(PictureCreator.GetAvatar(author, size=4096))
        file = discord.File(path, filename="avatar.gif")
        await ctx.send("Avatar " + author.name, file=file)

    @message_command(name="Получить ранг")
    async def getRank(self, ctx, message: discord.Message):
        author = message.author
        path = "Temp/{}.png".format(author.id)
        info = session.query(Member)\
            .filter(Member.MemberId == author.id)\
            .filter(Member.ServerId == author.guild.id).first()
        PictureCreator.CreateRank(author, info).save(path)
        file = discord.File(path, filename="profile.png")
        await ctx.send(file=file)
        os.remove(path)

    @slash_command(
        name='rank',
        description="Выводит ранг пользователя.",
    )
    async def rank(self, ctx, member: Option(discord.Member, "Пользователь", required=False, default=None)):
        if member:
            author = member
        else:
            author = ctx.author

        path = "Temp/{}.png".format(author.id)
        info = session.query(Member)\
            .filter(Member.MemberId == author.id)\
            .filter(Member.ServerId == author.guild.id).first()
        PictureCreator.CreateRank(author, info).save(path)
        file = discord.File(path, filename="profile.png")
        await ctx.send(file=file)
        os.remove(path)

    @slash_command(
        name='top',
        description="Выводит рейтинг сервера."
    )
    async def top(self, ctx,
                  cat: Option(str, "Категория рейтинга", default='Опыт', choices=["Опыт", "Упоминания", "Эмоджи"],
                              required=False),
                  page: Option(int, 'Страница рейтинга', min_value=1, default=1, required=True)):

        members = []
        page = int(page)
        if cat.isnumeric():
            page = int(cat)
            cat = "Опыт"

        page -= 1
        if cat == 'Опыт':
            for member in session.query(Member)\
                    .filter(Member.IsAlive)\
                    .filter(Member.ServerId == ctx.guild.id)\
                    .order_by(desc(Member.TotalXp)).limit(5).offset(5 * page):
                mem = ctx.guild.get_member(member.MemberId)
                members.append({
                    "mem": mem,
                    "data": ConvrterToCI(round(member.TotalXp, 2)) + "xp",
                    "url": PictureCreator.GetAvatar(mem, size=64)
                })
        elif cat == "Упоминания":
            for member in session.query(Member)\
                    .filter(Member.IsAlive)\
                    .filter(Member.ServerId == ctx.guild.id)\
                    .order_by(desc(Member.Mentions)).limit(5).offset(5 * page):
                mem = ctx.guild.get_member(member.MemberId)
                members.append({
                    "mem": mem,
                    "url": PictureCreator.GetAvatar(mem, size=64),
                    "data": str(member.Mentions) + " mentions"
                })
        elif cat == "Эмоджи":
            for emojie in session.query(Emojie)\
                    .filter(Emojie.ServerId == ctx.guild.id)\
                    .order_by(desc(Emojie.CountUsage)).limit(5).offset(5 * page):
                emoji = await ctx.guild.fetch_emoji(emojie.Id)
                members.append({
                    "mem": emoji,
                    "url": emoji.url,
                    "data": str(emojie.CountUsage) + " detected"
                })
        else:
            await ctx.send("Параметр не найден!")
            return

        path = "Temp/top{}.png".format(page)
        PictureCreator.GetTop(members, page).save(path)

        file = discord.File(path, filename="top.png")
        await ctx.send(file=file)

        os.remove(path)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.type == MessageType.new_member:
            return
        ignoreList = session.query(IgnoreList)\
            .filter(IgnoreList.ServerId == message.guild.id)\
            .filter(IgnoreList.ChannelId == message.channel.id).first()
        if not ignoreList:
            if len(message.mentions):
                for i in list(set(message.mentions)):
                    if not i.bot and not message.author.bot and not i.id == message.author.id:
                        XpSys.AddMention(memberId=i.id, serverId=message.guild.id)

            await XpSys.AddExp(memberId=message.author.id, ServerID=message.guild.id, count=len(message.content) / 10, channel=message.channel)

            ctx = await self.bot.get_context(message)
            for emoji in list(set(re.findall("<\D+\d+>", message.content))):
                try:
                    emj = await commands.EmojiConverter().convert(ctx, emoji)
                    emojie = session.query(Emojie)\
                        .filter(Emojie.ServerId == emj.guild.id)\
                        .filter(Emojie.Id == emj.id).first()
                    if emojie:
                        emojie.IncrementUsage()
                    else:
                        emojie = Emojie(serverId=emj.guild.id, id=emj.id)
                        session.add(emojie)
                    session.commit()
                except commands.errors.BadArgument:
                    pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        for mem in guild.members:
            if not mem.bot:
                XpSys.DelMem(mem.id, guild.id)


def setup(client):
    client.add_cog(Profile(client))
