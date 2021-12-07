import datetime
import logging

import discord
from discord import Client
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

import SQLWorker
from . import common, ignorChannels


logging.basicConfig(filename="admin.log", level=logging.INFO)


def is_owner():
    async def predicate(ctx):
        return ctx.author.id == ctx.guild.owner_id or ctx.author.id == 269860812355665921

    return commands.check(predicate)


muteList = {}
votumList = {}


async def muteFunc(member, hours):
    muteRole = SQLWorker.GetMuteRole(member.guild.id)
    import datetime
    endTime = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)
    SQLWorker.MuteMember(muteRole, member.id, member.guild.id, endTime)

    await member.add_roles(member.guild.get_role(int(muteRole)))
    muteList[member.guild.id, member.id] = {
        'serverId': member.guild.id,
        'userId': member.id,
        'roleId': muteRole,
        'endTime': str(endTime),
    }
    return True


class Admin(commands.Cog):
    def __init__(self, bot: Client):
        self.bot = bot
        self.init()
        self.muteTask.start()
        self.votumTask.start()

    @staticmethod
    def init():
        for i in SQLWorker.GetMuteMembers():
            muteList[i[0], i[1]] = {
                'serverId': i[0],
                'userId': i[1],
                'roleId': i[2],
                'endTime': i[3],
            }

        for i in SQLWorker.GetVotums():
            votumList[i[0], i[1]] = {
                'ServerId': i[0],
                'MessageId': i[1],
                'UserId': i[2],
                'EndTime': i[3],
                'ChannelId': i[4]
            }

    @tasks.loop(seconds=60, reconnect=True)
    async def muteTask(self):
        for i in muteList:
            if datetime.datetime.utcnow() >= datetime.datetime.strptime(muteList[i]['endTime'], '%Y-%m-%d %H:%M:%S.%f'):
                guild = await self.bot.fetch_guild(muteList[i]['serverId'])
                member = await guild.fetch_member(muteList[i]['userId'])
                try:
                    await member.remove_roles(guild.get_role(int(muteList[i]['roleId'])))
                except PermissionError:
                    pass
                SQLWorker.DelMute(muteList[i]['userId'], muteList[i]['serverId'])
                muteList.pop(i)

    @tasks.loop(seconds=60, reconnect=True)
    async def votumTask(self):
        for i in votumList:
            if datetime.datetime.utcnow() >= \
                    datetime.datetime.strptime(votumList[i]['EndTime'], '%Y-%m-%d %H:%M:%S.%f'):
                try:
                    channel = await self.bot.fetch_channel(votumList[i]['ChannelId'])
                    message = await channel.fetch_message(votumList[i]['MessageId'])
                    await message.delete()
                except discord.errors.NotFound:
                    pass
                SQLWorker.DelVotum(votumList[i]['ServerId'], votumList[i]['MessageId'], )
                votumList.pop(i)

    # Кол-во пришедших
    @cog_ext.cog_slash(
        name='count',
        description="Выводит статистику посещения сервера, а сколько пришло или ушло"
    )
    async def count(self, ctx: SlashContext):
        stat = SQLWorker.GetStat(ctx.guild.id)
        embed = discord.Embed(title="Я запомнила " + str(stat[0]) + " чел.", description="На данный момент")
        embed.add_field(name="Ушло", value=str(stat[1]) + " чел.")
        embed.add_field(name="Осталось", value=str(stat[2]) + " чел.")
        await ctx.send(embed=embed)

    # Устанавливает информационный канал
    @is_owner()
    @commands.command(name="setinfo", help="Задаёт канал для вывода сообщений об приходе/уходе/возвращение "
                                           "пользователей.", usage="ПингКанала", brief="Устанавливает информационный "
                                                                                       "канал")
    async def setInfo(self, ctx, channel):
        ch = await commands.TextChannelConverter().convert(ctx, channel)
        SQLWorker.SetInfoChan(ctx.guild.id, ch.id)
        await ctx.send("InfoChannel: {}".format(channel))

    # Устанавливает роль новичков
    @is_owner()
    @commands.command(name="setjoinrole", help="Задаёт роль для пользовтелей который только-что присоединились.",
                      usage="Название роли", brief="Устанавливает роль для новичков")
    async def setJoinRole(self, ctx, roleName=None):
        if roleName:
            role = await commands.RoleConverter().convert(ctx, roleName)
            SQLWorker.SetJoinRole(ctx.guild.id, role.id)

            await ctx.send("Join role changed to: {}".format(roleName))
        else:
            SQLWorker.SetJoinRole(ctx.guild.id, roleName)

            await ctx.send("Join role cleared")

    # Устанавливает название участника сервера
    @is_owner()
    @commands.command(name="setmemname",
                      help="Устанавливает называние при приходе/уходе/возвращение пользователей на сервер.",
                      usage="[Строка обозначающее имя участника канала == Member]",
                      brief="Устанавливает имя участника сервера")
    async def setMemName(self, ctx, name="Member"):
        SQLWorker.SetMemName(ctx.guild.id, name)
        await ctx.send("Member name changed to: {}".format(name))

    # Устанавливает текст при бане пользователя на сервере
    @is_owner()
    @commands.command(name="setbantext", help="Устанавливает текст при бане пользователя на сервере.",
                      usage="[Сроки обозначающие, что пользовтатель был забанен == has been banned.]",
                      brief="Устанавливает текст при бане пользователя на сервере.")
    async def setBanText(self, ctx, *args):
        text = ' '.join(args)
        if len(text) == 0:
            text = 'has been banned.'
        SQLWorker.SetBanText(ctx.guild.id, text)
        await ctx.send("Ban text changed for: {}".format(text))

    # Подключение к серверу
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logging.info("Join to: {} {}".format(guild.id, guild.name))
        if not SQLWorker.CheckServer(guild.id):
            common.createServerFolder(guild)
            SQLWorker.AddServer(guild.id)
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

        for i in SQLWorker.GetAllEmojie(ctx.guild.id):
            emoji = emojies.get(i[1])
            if emoji:
                embed = discord.Embed(title=emoji.name)
                embed.set_thumbnail(url=emoji.url)
                embed.add_field(name="Кол-во:",
                                value=i[2],
                                inline=True)
                import datetime
                embed.add_field(name="Последнее использование:",
                                value=str(datetime.datetime.fromtimestamp(i[3])),
                                inline=True)
                await ctx.send(embed=embed)

    @is_owner()
    @commands.command(name="setmuterole", help="Задаёт роль для пользовтелей которых нужно замутить.",
                      usage="Название роли", brief="Устанавливает роль для мута")
    async def setMuteRole(self, ctx, roleName=None):
        if roleName:
            role = await commands.RoleConverter().convert(ctx, roleName)
            SQLWorker.SetMuteRole(ctx.guild.id, role.id)

            await ctx.send("Mute role changed to: {}".format(roleName))
        else:
            SQLWorker.SetMuteRole(ctx.guild.id, roleName)
            await ctx.send("Mute role cleared")

    @cog_ext.cog_slash(
        name='votum',
        description="Начинает голосование по выдачи Вотума недовольства (Мута) пользователю.",
        options=[
            create_option(
                name="member",
                description="@Пинг пользователя, которому выдаём Вотум",
                required=True,
                option_type=SlashCommandOptionType.USER,
            ),
        ]
    )
    async def votum(self, ctx: SlashContext, member):
        if not SQLWorker.CheckMuteRole(ctx.guild.id):
            return await ctx.send("Не найдена Мут-роль воспользйетсь коммандой !setmuterole")

        if member.bot:
            emb = discord.Embed(
                title="Некорректный вызов",
                description="Пользователь {0} - это Бот".format(member.name))
            return await ctx.send(embed=emb)

        if muteList.get((member.guild.id, member.id)):
            return await ctx.send("Пользователь {} уже в муте".format(member.name))

        # Проверяем не идёт ли уже голосование за мут
        if SQLWorker.CheckVotum(member.id):
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
        endTime = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        SQLWorker.CreateVotum(ctx.guild.id, ctx.channel.id, member.id, msg.id, endTime)

        votumList[ctx.guild.id, msg.id] = {
            'ServerId': ctx.guild.id,
            'ChannelId': ctx.channel.id,
            'MessageId': msg.id,
            'UserId': member.id,
            'EndTime': str(endTime),
        }

        await msg.add_reaction('\N{THUMBS UP SIGN}')
        return msg

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        if reaction.count >= 6:

            message = reaction.message
            member = await message.guild.fetch_member(
                votumList[reaction.message.guild.id, reaction.message.id]['UserId'])
            if not await muteFunc(member, 24):
                return

            votumList.pop((reaction.message.guild.id, reaction.message.id))
            SQLWorker.DelVotum(reaction.message.guild.id, reaction.message.id)
            await reaction.message.delete()

            return await message.send("Пользователь {} заглушен на {} часа".format(member.name, 24))

    @is_owner()
    @commands.command(name="mute", help="Мутит пользователя.",
                      usage="@Пинг пользователя [Кол-во часов мута]", brief="Мут пользователя")
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, member, hours: int = 4):
        if not SQLWorker.CheckMuteRole(ctx.guild.id):
            await ctx.send("Не найдена Мут-роль воспользйетсь коммандой !setmuterole")
            return
        if member:
            member = await commands.MemberConverter().convert(ctx, member)
            if not member:
                await ctx.send("Пользователь {} не найден".format(member.name))
                return
            if muteList.get((member.guild.id, member.id)):
                await ctx.send("Пользователь {} уже в муте".format(member.name))
                return
        if await muteFunc(member, hours):
            await ctx.send("Пользователь {} заглушен на {} часа".format(member.name, hours))


def setup(client):
    client.add_cog(Admin(client))
