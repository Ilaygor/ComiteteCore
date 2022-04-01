import datetime
import logging

import discord
from discord import Client
from discord.commands import slash_command, Option, permissions, SlashCommandGroup, CommandPermission
from discord.ext import commands, tasks
from discord.ext.pages import Paginator, Page
from sqlalchemy import desc

from models.Emojies import Emojie
from models.Members import Member
from models.Servers import Server
from models.Votums import Votum
from models.database import Session
from . import common, ignorChannels, boostChannels

logging.basicConfig(filename="admin.log", level=logging.INFO)

session = Session()


def is_owner():
    async def predicate(ctx):
        return ctx.author.id == ctx.guild.owner_id or ctx.author.id == 269860812355665921

    return commands.check(predicate)


votumList = {}
guilds = []


class Admin(commands.Cog):
    def __init__(self, bot: Client):
        self.bot = bot
        self.init()
        self.votumTask.start()

        for server in session.query(Server):
            guilds.append(server.Id)

    settings = SlashCommandGroup("setting", "Настройки бота. Admin only!",
                                 permissions=[CommandPermission("owner", 2, True)], )

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
        votum = session.query(Votum) \
            .filter(Votum.ServerId == ctx.guild.id) \
            .filter(Votum.MemberId == member.id).first()
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
    @settings.command(name="info", guild_id=guilds, default_permission=False,
                      description="Задаёт канал для вывода сообщений об приходе/уходе/возвращение пользователей.")
    async def setInfo(self, ctx,
                      channel: Option(discord.TextChannel, "Выбрите текстовый канал", required=False, default=None)):
        server = session.query(Server).filter(Server.Id == ctx.guild.id).first()
        if channel:
            server.InfoChannel = channel.id
        else:
            server.InfoChannel = ""
        session.commit()
        await ctx.send("InfoChannel: {}".format(channel.name))

    # Устанавливает роль новичков
    @settings.command(name="joinrole", guild_id=guilds, default_permission=False,
                      description="Задаёт роль для пользовтелей который только-что присоединились.")
    async def setJoinRole(self, ctx,
                          role: Option(discord.Role, "Выберите роль для новичков", required=False, default=None)):
        server = session.query(Server).filter(Server.Id == ctx.guild.id).first()
        if role:
            server.JoinRole = role.id
            await ctx.send("Join role changed to: {}".format(role.name))
        else:
            server.JoinRole = ""
            await ctx.send("Join role cleared")
        session.commit()

    # Устанавливает название участника сервера
    @settings.command(name="memname", guild_id=guilds, default_permission=False,
                      description="Устанавливает называние при приходе/уходе/возвращение пользователей на сервер.")
    async def setMemName(self, ctx, name: Option(str, "Строка обозначающее имя участника канала",
                                                 default="Member", required=False)):
        server = session.query(Server).filter(Server.Id == ctx.guild.id).first()
        server.MemberName = name
        session.commit()
        await ctx.send("Member name changed to: {}".format(name))

    # Устанавливает текст при бане пользователя на сервере
    @slash_command(name="setbantext", guild_id=guilds, default_permission=False,
                   description="Устанавливает текст при бане пользователя на сервере.")
    @permissions.is_owner()
    async def setBanText(self, ctx, bantext: Option(str, "Сроки обозначающие, что пользовтатель был забанен",
                                                    default="has been banned.", required=False)):
        server = session.query(Server).filter(Server.Id == ctx.guild.id).first()
        server.BanText = bantext
        session.commit()
        await ctx.send("Ban text changed for: {}".format(bantext))

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
            guilds.append(guild.id)
        else:
            common.checkMembersOnServer(guild)
        common.addRoles(guild)
        common.addEmojies(guild)

    # аudit
    @settings.command(name="audit", guild_id=guilds, default_permission=False,
                      description="Производит аудит пользователей сервера и синхронизирует с бд бота.")

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

    @settings.command(name="ignor", guild_id=guilds, default_permission=False,
                      description="Игнор-лист, для того чтобы бот не защитывал XP, упоминания или эмодзи в каналах.")
    async def ignor(self, ctx,
                    action: Option(str, "Выберите раздел", required=True, choices=["Список", "Добавить", "Удалить"],
                                   default="Список"),
                    channel: Option(discord.TextChannel, "Канал который добавить/удалить из списка", required=False,
                                    default=None)):
        if action == "Список":
            embed = await ignorChannels.list(ctx)
            await ctx.send(embed=embed)
        elif action == "Добавить":
            if channel:
                embed = await ignorChannels.add(ctx, channel)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Не указан канал!")
        elif action == "Удалить":
            if channel:
                embed = await ignorChannels.remove(ctx, channel)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Не указан канал!")
        else:
            await ctx.send("Неизвестное действие.")

    @settings.command(name="boost", guild_id=guilds, default_permission=False,
                      description="Boost-лист каналов где присваивается х2 опыт.")
    async def boost(self, ctx,
                    action: Option(str, "Выберите раздел", required=True, choices=["Список", "Добавить", "Удалить"],
                                   default="Список"),
                    channel: Option(discord.TextChannel, "Канал который добавить/удалить из списка", required=False,
                                    default=None)):
        if action == "Список":
            embed = await boostChannels.list(ctx)
            await ctx.send(embed=embed)
        elif action == "Добавить":
            if channel:
                embed = await boostChannels.add(ctx, channel)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Не указан канал!")
        elif action == "Удалить":
            if channel:
                embed = await boostChannels.remove(ctx, channel)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Не указан канал!")
        else:
            await ctx.send("Неизвестное действие.")

    @slash_command(name="emojistat",
                   description="Выводит статистику использования серверных эмоджи.")
    async def emojiStat(self, ctx: discord.ApplicationContext):
        pages = []

        emojies = {}
        for i in ctx.guild.emojis:
            emojies.update({i.id: i})

        iter = 0

        for emojie in session.query(Emojie).filter(Emojie.ServerId == ctx.guild.id).order_by(desc(Emojie.CountUsage)):
            emoji = emojies.get(emojie.Id)
            if emoji:
                iter += 1
                embed = discord.Embed(title=emoji.name)
                embed.set_thumbnail(url=emoji.url)
                embed.add_field(name="Кол-во:",
                                value=emojie.CountUsage,
                                inline=True)
                embed.add_field(name="Последнее использование:",
                                value=str(emojie.LastUsage),
                                inline=True)
                if iter == 1:
                    page = Page(embeds=[embed])
                else:
                    page.embeds.append(embed)
                if iter == 5:
                    pages.append(page)
                    iter = 0
        try:
            if pages.count(page) == 0:
                pages.append(page)
        except UnboundLocalError:
            return

        if len(pages) == 0:
            return

        paginator = Paginator(pages=pages, loop_pages=True, disable_on_timeout=True, timeout=360)
        await paginator.respond(ctx.interaction)


def setup(client):
    client.add_cog(Admin(client))
