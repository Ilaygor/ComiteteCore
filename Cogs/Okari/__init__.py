import discord
from discord.ext import commands
import os
import SQLWorker
import PictureCreator
from Cogs.Profile import XpSys

from models.Members import Member
from models.database import Session
from models.Emojies import Emojie
from models.Servers import Server
from models.RoleLists import RoleList
session = Session()

class Okari(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Пользователь присоединился
    @commands.Cog.listener()
    async def on_member_join(self, member):
        server = session.query(Server).filter(Server.Id == member.guild.id).first()
        path = "Temp/{0}.png".format(member.id)
        memberSql = session.query(Member).filter(Member.MemberId == member.id).first()
        if memberSql:
            SQLWorker.SetAlive(server.Id, member.id)
            PictureCreator.CreatWelcomeMessage(member.avatar_url_as(size=128),
                                               member.name,
                                               server.MemberName) \
                .save(path, format="png")
        else:
            SQLWorker.AddNewMem(serverId=server.Id, memberId=member.id)
            PictureCreator.CreateFirstWelcomeMessage(member.avatar_url_as(size=128),
                                                     member.name,
                                                     server.MemberName) \
                .save(path, format="png")

        file = discord.File(path, filename="MemJoin.png")
        await member.guild.get_channel(server.InfoChannel).send(file=file)
        os.remove(path)

        if not memberSql:
            joinRole = server.JoinRole
            if joinRole:
                await member.add_roles(member.guild.get_role(int(joinRole)))
        else:
            for roleList in session.query(RoleList).filter(RoleList.MemberId == memberSql.Id):
                try:
                    await member.add_roles(member.guild.get_role(roleList.RoleId))
                except AttributeError:
                    roleList.delete()
                    session.commit()
                except discord.errors.Forbidden:
                    pass

        if not member.bot:
            XpSys.AddMem(member.id, server.Id)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if len(before.roles) < len(after.roles):
            member = session.query(Member)\
                .filter(Member.MemberId == after.id)\
                .filter(Member.ServerId == after.guild.id).first()
            for i in after.roles:
                if i in before.roles:
                    continue
                role = session.query(RoleList)\
                    .filter(RoleList.MemberId == member.Id)\
                    .filter(RoleList.RoleId == i.id).first()
                if not role:
                    role = RoleList(memberId=member.id, roleId=i.id)
                    session.add(role)
                    session.commit()

        if len(before.roles) > len(after.roles):
            member = session.query(Member)\
                .filter(Member.MemberId == after.id)\
                .filter(Member.ServerId == after.guild.id).first()
            for i in before.roles:
                if i not in after.roles:
                    role = session.query(RoleList)\
                        .filter(RoleList.MemberId == member.Id)\
                        .filter(RoleList.RoleId == i.id).first()
                    role.delete()
                    session.commit()

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        if len(before) < len(after):
            for i in after:
                if i in before:
                    continue
                emojie = session.query(Emojie)\
                    .filter(Emojie.Id == i.id)\
                    .filter(Emojie.ServerId == guild.id).first()
                if not emojie:
                    emojie = Emojie(id=i.id, serverId=guild.id)
                    session.add(emojie)
                    session.commit()

        if len(before) > len(after):
            for i in before:
                if i not in after:
                    emojie = session.query(Emojie)\
                        .filter(Emojie.Id == i.id)\
                        .filter(Emojie.ServerId == guild.id).first()
                    emojie.Delete()
                    session.commit()

    # Пользователь покинул сервер
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        server = session.query(Server).filter(Server.Id == member.guild.id).first()
        try:
            await member.guild.fetch_ban(member)
            if not member.bot:
                XpSys.DelMem(member.id, member.guild.id)

        except discord.NotFound:
            path = "Temp/{0}.png".format(member.id)
            PictureCreator.CreateLostMessage(member.avatar_url_as(size=128),
                                             member.name,
                                             member.top_role,
                                             server.MemberName) \
                .save(path, format="png")
            SQLWorker.SetDead(server.Id, member.id)
            file = discord.File(path, filename="MemRemove.png")
            await member.guild.get_channel(server.InfoChannel).send(file=file)
            os.remove(path)

    # Пользователя забанили
    @commands.Cog.listener()
    async def on_member_ban(self, guild, mem):
        server = session.query(Server).filter(Server.Id == mem.guild.id).first()
        path = "Temp/{0}.png".format(mem.id)
        PictureCreator.CreateLostMessage(mem.avatar_url_as(size=128),
                                         mem.name,
                                         None,
                                         server.MemberName) \
            .save(path, format="png")
        SQLWorker.SetDead(guild.id, mem.id)
        file = discord.File(path, filename="MemRemove.png")

        reason = await guild.fetch_ban(mem)
        embed = discord.Embed(title=mem.name + " " + server.BanText)
        embed.add_field(name="Причина:",
                        value=(reason[0] if reason[0] else "Отсутсвует"),
                        inline=False)
        await guild.get_channel(server.InfoChannel).send(embed=embed, file=file)
        os.remove(path)


def setup(client):
    client.add_cog(Okari(client))
