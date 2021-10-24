import os
import re

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_choice, create_option

import PictureCreator
import SQLWorker
from PictureCreator.utils import ConvrterToCI
from . import XpSys


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        XpSys.init()

    @cog_ext.cog_slash(
        name='profile',
        description="Выводит профиль пользователя.",
        options=[
            create_option(
                name="member",
                description="@Пинг пользователя чей профиль вывести",
                required=False,
                option_type=SlashCommandOptionType.MENTIONABLE
            )
        ]
    )
    async def profile(self, ctx: SlashContext, member=None):
        if member:
            author = await commands.MemberConverter().convert(ctx, member)
        else:
            author = ctx.author

        path = "Temp/{}.png".format(author.id)
        PictureCreator.CreateProfile(author).save(path)

        file = discord.File(path, filename="profile.png")
        await ctx.send(file=file)

        os.remove(path)

    @cog_ext.cog_slash(
        name='setbg',
        description="Устанавливает задний фон для профиля. Приложить изображение или ссылку на изображение.",
        options=[
            create_option(
                name="url",
                description="Ссылка на задний фон",
                required=False,
                option_type=SlashCommandOptionType.STRING
            )
        ]
    )
    async def setBg(self, ctx: SlashContext, url=None):
        if url:
            try:
                urlToPic = url
                PictureCreator.SetBG(ctx.guild.id, ctx.author.id, urlToPic)
            except:
                await ctx.send('Некорректная ссылка на изображение.')
                return
        else:
            try:
                os.remove("src/Images/Usr/{}/{}/profile.png".format(ctx.guild.id, ctx.author.id))
            except:
                return

        path = "Temp/{}.png".format(ctx.author.id)
        PictureCreator.CreateProfile(ctx.author).save(path)

        file = discord.File(path, filename="profile.png")
        await ctx.send(file=file)
        os.remove(path)

    @cog_ext.cog_slash(
        name='settext',
        description="Задаёт подпись профиля.",
        options=[
            create_option(
                name="text",
                description="Информация",
                required=False,
                option_type=SlashCommandOptionType.STRING
            )
        ]
    )
    async def setText(self, ctx: SlashContext, text=""):
        SQLWorker.SetInfoProfile(ctx.author.id, ctx.guild.id, text)
        path = "Temp/{}.png".format(ctx.author.id)
        PictureCreator.CreateProfile(ctx.author).save(path)
        file = discord.File(path, filename="profile.png")
        await ctx.send(file=file)
        os.remove(path)

    @cog_ext.cog_slash(
        name='avatar',
        description="Выводит аватар пользователя.",
        options=[
            create_option(
                name="member",
                description="Пинг пользователя",
                required=False,
                option_type=SlashCommandOptionType.MENTIONABLE
            )
        ]
    )
    async def avatar(self, ctx, member=None):
        if member:
            author = await commands.MemberConverter().convert(ctx, member)
        else:
            author = ctx.author

        path = PictureCreator.utils.GetAvatarFromUrl(author.avatar_url_as(size=4096))
        file = discord.File(path, filename="avatar.gif")
        await ctx.send("Avatar " + author.name, file=file)

    @cog_ext.cog_slash(
        name='rank',
        description="Выводит ранг пользователя.",
        options=[
            create_option(
                name="member",
                description="Пинг пользователя",
                required=False,
                option_type=SlashCommandOptionType.MENTIONABLE
            )
        ]
    )
    async def rank(self, ctx, member=None):
        if member:
            author = await commands.MemberConverter().convert(ctx, member)
        else:
            author = ctx.author
        path = "Temp/{}.png".format(author.id)
        PictureCreator.CreateRank(author).save(path)
        file = discord.File(path, filename="profile.png")
        await ctx.send(file=file)
        os.remove(path)

    @cog_ext.cog_slash(
        name='top',
        description="Выводит рейтинг сервера.",
        options=[
            create_option(
                name="cat",
                description="Категория рейтинга",
                required=False,
                option_type=SlashCommandOptionType.STRING,
                choices=[
                    create_choice(
                        name='Опыт',
                        value='exp'
                    ),
                    create_choice(
                        name='Упоминания',
                        value='men',
                    ),
                    create_choice(
                        name='Эмоджи',
                        value='emoji',
                    )
                ]
            ),
            create_option(
                name="page",
                description="Страница рейтинга",
                required=False,
                option_type=SlashCommandOptionType.INTEGER,
            )
        ]
    )
    async def top(self, ctx, cat: str = "exp", page: int = 1):

        members = []
        page = int(page)
        if cat.isnumeric():
            page = int(cat)
            cat = "exp"

        if cat == 'exp':
            for i in SQLWorker.GetTopMembers(page - 1, ctx.guild.id):
                mem = ctx.guild.get_member(i[0])
                members.append({
                    "mem": mem,
                    "data": ConvrterToCI(round(i[1], 2)) + "xp",
                    "url": mem.avatar_url_as(size=64)
                })
        elif cat == "men":
            for i in SQLWorker.GetTopMenMembers(page - 1, ctx.guild.id):
                mem = ctx.guild.get_member(i[0])
                members.append({
                    "mem": mem,
                    "url": mem.avatar_url_as(size=64),
                    "data": str(i[1]) + " mentions"
                })
        elif cat == "emoji":
            for i in SQLWorker.GetTopEmoji(page - 1, ctx.guild.id):
                emoji = await ctx.guild.fetch_emoji(i[0])
                members.append({
                    "mem": emoji,
                    "url": emoji.url,
                    "data": str(i[1]) + " detected"
                })
        else:
            await ctx.send("Параметр не найден!")
            return

        path = "Temp/top{}.png".format(page)
        PictureCreator.GetTop(members, page - 1).save(path)

        file = discord.File(path, filename="top.png")
        await ctx.send(file=file)

        os.remove(path)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot:
            XpSys.AddMem(member.id, member.guild.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not member.bot:
            XpSys.DelMem(member.id, member.guild.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        # await self.bot.process_commands(message)
        if not message.author.bot and not SQLWorker.checkChannel(message.guild.id, message.channel.id):
            if len(message.mentions):
                for i in list(set(message.mentions)):
                    if not i.bot and not message.author.bot and not i.id == message.author.id:
                        XpSys.AddMention(i.id, message.guild.id)
            await XpSys.AddExp(message.author.id, message.guild.id, len(message.content) / 10, message.channel)

            ctx = await self.bot.get_context(message)

            for emoji in list(set(re.findall("<\D+\d+>", message.content))):
                try:
                    emj = await commands.EmojiConverter().convert(ctx, emoji)
                    SQLWorker.IncEmoji(message.guild.id, emj.id)
                except commands.errors.BadArgument:
                    pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for mem in guild.members:
            XpSys.AddMem(mem.id, guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        for mem in guild.members:
            XpSys.DelMem(mem.id, guild.id)


def setup(client):
    client.add_cog(Profile(client))
