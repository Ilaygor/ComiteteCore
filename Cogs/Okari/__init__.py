import discord
from discord.ext import commands
import os
import SQLWorker
import PictureCreator
from Cogs.Profile import XpSys


class Okari(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Пользователь присоединился
    @commands.Cog.listener()
    async def on_member_join(self, member):
        path = "Temp/{0}.png".format(member.id)
        if SQLWorker.CheckMember(member.guild.id, member.id):
            SQLWorker.SetAlive(member.guild.id, member.id)
            PictureCreator.CreatWelcomeMessage(member.avatar_url_as(size=128),
                                               member.name,
                                               SQLWorker.GetMemName(member.guild.id)) \
                .save(path, format="png")
        else:
            SQLWorker.AddNewMem(member.guild.id, member.id)
            PictureCreator.CreateFirstWelcomeMessage(member.avatar_url_as(size=128), member.name,
                                                     SQLWorker.GetMemName(member.guild.id)) \
                .save(path, format="png")

        file = discord.File(path, filename="MemJoin.png")
        await member.guild.get_channel(SQLWorker.GetInfoChan(member.guild.id)).send(file=file)
        os.remove(path)

        joinRole = SQLWorker.GetJoinRole(member.guild.id)
        if joinRole:
            await member.add_roles(member.guild.get_role(int(joinRole)))

        for i in SQLWorker.GetRoles(member.guild.id, member.id):
            try:
                await member.add_roles(member.guild.get_role(int(i[0])))
            except AttributeError:
                SQLWorker.DelRole(i[0])
            except discord.errors.Forbidden:
                pass

        if not member.bot:
            XpSys.AddMem(member.id, member.guild.id)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if len(before.roles) < len(after.roles):
            for i in after.roles:
                if i not in before.roles and not SQLWorker.CheckRole(after.guild.id, after.id, i.id):
                    SQLWorker.AddRoles(after.guild.id, after.id, i.id)
        if len(before.roles) > len(after.roles):
            for i in before.roles:
                if i not in after.roles:
                    SQLWorker.DelRole(i.id)

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        if len(before) < len(after):
            for i in after:
                if i not in before and not SQLWorker.CheckEmoji(guild.id, i.id):
                    SQLWorker.AddEmoji(guild.id, i.id)
        if len(before) > len(after):
            for i in before:
                if i not in after:
                    SQLWorker.DelEmoji(i.id)

    # Пользователь покинул сервер
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            await member.guild.fetch_ban(member)
            if not member.bot:
                XpSys.DelMem(member.id, member.guild.id)

        except discord.NotFound:
            path = "Temp/{0}.png".format(member.id)
            PictureCreator.CreateLostMessage(member.avatar_url_as(size=128),
                                             member.name,
                                             member.top_role,
                                             SQLWorker.GetMemName(member.guild.id)) \
                .save(path, format="png")
            SQLWorker.SetDead(member.guild.id, member.id)
            file = discord.File(path, filename="MemRemove.png")
            await member.guild.get_channel(SQLWorker.GetInfoChan(member.guild.id)).send(file=file)
            os.remove(path)

    # Пользователя забанили
    @commands.Cog.listener()
    async def on_member_ban(self, guild, mem):
        path = "Temp/{0}.png".format(mem.id)
        PictureCreator.CreateLostMessage(mem.avatar_url_as(size=128),
                                         mem.name,
                                         None,
                                         SQLWorker.GetMemName(guild.id)) \
            .save(path, format="png")
        SQLWorker.SetDead(guild.id, mem.id)
        file = discord.File(path, filename="MemRemove.png")

        reason = await guild.fetch_ban(mem)
        embed = discord.Embed(title=mem.name + " " + SQLWorker.GetBanText(guild.id))
        embed.add_field(name="Причина:",
                        value=(reason[0] if reason[0] else "Отсутсвует"),
                        inline=False)
        await guild.get_channel(SQLWorker.GetInfoChan(guild.id)).send(embed=embed, file=file)
        os.remove(path)


def setup(client):
    client.add_cog(Okari(client))
