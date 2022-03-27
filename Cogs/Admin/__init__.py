import datetime
import logging

import discord
from discord import Client
from discord.ext import commands, tasks
from discord.commands import slash_command, Option

from models.Votums import Votum
from models.Members import Member
from models.Servers import Server
from models.Emojies import Emojie
from models.database import Session

from . import common, ignorChannels

logging.basicConfig(filename="admin.log", level=logging.INFO)

session = Session()


def is_owner():
    async def predicate(ctx):
        return ctx.author.id == ctx.guild.owner_id or ctx.author.id == 269860812355665921

    return commands.check(predicate)


votumList = {}


class Admin(commands.Cog):
    def __init__(self, bot: Client):
        self.bot = bot
        self.init()
        self.votumTask.start()

    @staticmethod
    def init():
        for votum in session.query(Votum):
            votumList[votum.ServerId, votum.MessageId] = votum

    @tasks.loop(seconds=60, reconnect=True)
    async def votumTask(self):
        for i in votumList:
            votum = votumList[i]
            if datetime.datetime.utcnow() >= votum.EndTime:
                try:
                    channel = await self.bot.fetch_channel(votum.ChannelId)
                    message = await channel.fetch_message(votum.MessageId)
                    await message.delete()
                except discord.errors.NotFound:
                    pass
                session.delete(votum)
                session.commit()
                votumList.pop(i)

    @slash_command(
        name='votum',
        description="Начинает голосование по выдачи Вотума недовольства (Мута) пользователю.",
    )
    async def votum(self, ctx, member: Option(discord.Member, "Выберите пользователя, которому выдаём Вотум")):
        if member.bot:
            emb = discord.Embed(
                title="Некорректный вызов",
                description="Пользователь {0} - это Бот".format(member.name))
            return await ctx.send(embed=emb)

        # Проверяем не идёт ли уже голосование за мут
        votum = session.query(Votum).filter(Votum.ServerId == ctx.guild.id, Votum.MemberId == member.id).first()
        if votum:
            emb = discord.Embed(
                title="Некорректный вызов",
                description="{1}, голосование по выдачи Вотума пользователю {0} уже идёт".format(member.name,
                                                                                                 ctx.author.name))
            return await ctx.send(embed=emb)

        # Создаём голование
        emb = discord.Embed(
            title="Голосование за выдачу Вотума Недовольства пользователю {0}".format(member.name),
            description="Если это собщение наберёт 6 голосов (:thumbsup:) в течении 1 часа, тогда пользователю {0} "
                        "будет выдан мут на 24 часа".format(member.name))
        msg = await ctx.send(embed=emb)
        votum = Votum(channelId=ctx.channel.id, serverId=ctx.guild.id, memberId=member.id, messageId=msg.id)
        session.add(votum)
        session.commit()
        votumList[ctx.guild.id, msg.id] = votum
        await msg.add_reaction('\N{THUMBS UP SIGN}')
        return msg

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        if reaction.count >= 6:
            hours = 24
            message = reaction.message
            votum = votumList[reaction.message.guild.id, reaction.message.id]

            member = await message.guild.fetch_member(votum.MemberId)
            await member.timeout(datetime.datetime.now() + datetime.timedelta(days=1),
                                 reason="Большинство проголосовало за мут")
            votumList.pop((votum.ServerId, votum.MessageId))
            session.delete(votum)
            session.commit()
            await message.delete()
            return await message.channel.send(content="Пользователь {} заглушен на {} часа".format(member.name, hours))

    # Кол-во пришедших
    @slash_command(name='count', description='Выводит статистику посещения сервера, а сколько пришло или ушло')
    async def count(self, ctx):
        members = session.query(Member).filter(Member.ServerId == ctx.guild.id)
        all = members.count()
        alive = members.filter(Member.IsAlive).count()
        dead = members.filter(Member.IsAlive == False).count()

        embed = discord.Embed(title="Я запомнила " + str(all) + " чел.", description="На данный момент")
        embed.add_field(name="Ушло", value=str(dead) + " чел.")
        embed.add_field(name="Осталось", value=str(alive) + " чел.")
        await ctx.send(embed=embed)

    # Устанавливает информационный канал
    @is_owner()
    @commands.command(name="setinfo", help="Задаёт канал для вывода сообщений об приходе/уходе/возвращение "
                                           "пользователей.", usage="ПингКанала", brief="Устанавливает информационный "
                                                                                       "канал")
    async def setInfo(self, ctx, channel):
        ch = await commands.TextChannelConverter().convert(ctx, channel)
        server = session.query(Server).filter(Server.Id == ctx.guild.id).first()
        server.InfoChannel = ch.id
        session.commit()
        await ctx.send("InfoChannel: {}".format(channel))

    # Устанавливает роль новичков
    @is_owner()
    @commands.command(name="setjoinrole", help="Задаёт роль для пользовтелей который только-что присоединились.",
                      usage="Название роли", brief="Устанавливает роль для новичков")
    async def setJoinRole(self, ctx, roleName=None):
        server = session.query(Server).filter(Server.Id == ctx.guild.id).first()
        if roleName:
            role = await commands.RoleConverter().convert(ctx, roleName)
            server.JoinRole = role.id
            session.commit()
            await ctx.send("Join role changed to: {}".format(roleName))
        else:
            server.JoinRole = roleName
            session.commit()
            await ctx.send("Join role cleared")

    # Устанавливает название участника сервера
    @is_owner()
    @commands.command(name="setmemname",
                      help="Устанавливает называние при приходе/уходе/возвращение пользователей на сервер.",
                      usage="[Строка обозначающее имя участника канала == Member]",
                      brief="Устанавливает имя участника сервера")
    async def setMemName(self, ctx, name="Member"):
        server = session.query(Server).filter(Server.Id == ctx.guild.id).first()
        server.MemberName = name
        session.commit()
        await ctx.send("Member name changed to: {}".format(name))

    # Устанавливает текст при бане пользователя на сервере
    @is_owner()
    @commands.command(name="setbantext", help="Устанавливает текст при бане пользователя на сервере.",
                      usage="[Сроки обозначающие, что пользовтатель был забанен == has been banned.]",
                      brief="Устанавливает текст при бане пользователя на сервере.")
    async def setBanText(self, ctx, *args):
        server = session.query(Server).filter(Server.Id == ctx.guild.id).first()
        text = ' '.join(args)
        if len(text) == 0:
            text = 'has been banned.'
        server.BanText = text
        session.commit()
        await ctx.send("Ban text changed for: {}".format(text))

    # Подключение к серверу
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logging.info("Join to: {} {}".format(guild.id, guild.name))
        server = session.query(Server).filter(Server.Id == guild.id).first()
        if not server:
            common.createServerFolder(guild)
            server = Server(id=guild.id)
            session.add(server)
            session.commit()
            common.addMembersOnServer(guild)
        else:
            common.checkMembersOnServer(guild)
        common.addRoles(guild)
        common.addEmojies(guild)

    # аudit
    @is_owner()
    @commands.command(name="audit", help="Производит аудит пользователей сервера, т.е. смотрит какие пользователи "
                                         "присутсвуют, а какие отсутсвуют и производит учёт.\n Полезно, когда пришёл "
                                         "новый пользователь, а бот был в отключке.", usage="", brief="Аудит сервера")
    async def audit(self, ctx):
        server = session.query(Server).filter(Server.Id == ctx.guild.id).first()
        if not server:
            common.createServerFolder(ctx.guild)
            server = Server(id=ctx.guild.id)
            session.add(server)
            session.commit()
            common.addMembersOnServer(ctx.guild)
        else:
            common.checkMembersOnServer(ctx.guild)
        common.addRoles(ctx.guild)
        common.addEmojies(ctx.guild)
        await ctx.send("Audit completed!")

    @is_owner()
    @commands.command(name="ignor",
                      help="Игнор-лист, для того чтобы бот не защитывал XP, упоминания или эмодзи в каналах админа "
                           "сервера.\nНапример добавьте в игнор-лист каналы в которых предназначенные для флуда или "
                           "каналы предназначенные для ботов.\nДействия:\n> list - выводит список игнорируемых "
                           "каналов.\n> add - добавляет канал в список игнорируемых каналов, требует пинг канала.\n> "
                           "rem - девушка с голубыми волосами, близнец ram... Не та Информация, т.е. данное действие "
                           "отвечает за удаление канала из игнор листа, требует пинг канала.",
                      usage="[Действие == list] [Канал]", brief="Игнор-лист")
    async def ignor(self, ctx, action: str = "list", channel=None):
        if action == "list":
            embed = await ignorChannels.list(ctx)
            await ctx.send(embed=embed)
        elif action == "add":
            if channel:
                embed = await ignorChannels.add(ctx, channel)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Не указан канал!")
        elif action == "rem":
            if channel:
                embed = await ignorChannels.remove(ctx, channel)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Не указан канал!")
        else:
            await ctx.send("Неизвестное действие.")

    @is_owner()
    @commands.command(name="emojistat", help="Выводит статистику использования серверных эмоджи.", usage="",
                      brief="Выводит статистику использования серверных эмоджи.")
    async def emojiStat(self, ctx):
        emojies = {}
        for i in ctx.guild.emojis:
            emojies.update({i.id: i})

        for emojie in session.query(Emojie).filter(Emojie.ServerId == ctx.guild.id):
            emoji = emojies.get(emojie.Id)
            if emoji:
                embed = discord.Embed(title=emoji.name)
                embed.set_thumbnail(url=emoji.url)
                embed.add_field(name="Кол-во:",
                                value=emojie.CountUsage,
                                inline=True)
                import datetime
                embed.add_field(name="Последнее использование:",
                                value=str(emojie.LastUsage),
                                inline=True)
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Admin(client))
