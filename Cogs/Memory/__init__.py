import datetime

import discord
from discord import MessageType

from discord.ext import commands, tasks

from models.Message import Message
from models.Members import Member
from models.database import Session
from discord.commands import slash_command, Option
from discord.ext.pages import Paginator, Page
from sqlalchemy import desc
session = Session()


class Memory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forget.start()

    @tasks.loop(seconds=3600, reconnect=True)
    async def forget(self):
        session.query(Message).filter(
            Message.Created <= (datetime.datetime.now() - datetime.timedelta(hours=1))).delete()
        session.commit()

    @slash_command(
        name='memory',
        description="Выводит последние сообщения.",
    )
    async def memory(self, ctx,
                     channel: Option(discord.TextChannel, "Выбреите канал", required=True),
                     member: Option(discord.Member, "Выберите пользователя", required=False, default=None)):
        messages = session.query(Message, Member)\
            .filter(Message.ChannelId == channel.id)\
            .filter(Message.MemberId == Member.Id)

        if member:
            messages = messages.filter(Member.MemberId == member.id)

        pages = []

        iter = 0
        for message, dbmember in messages.order_by(desc(Message.Created)):
            member = ctx.guild.get_member(dbmember.MemberId)
            iter += 1
            embed = discord.Embed(title=member.name)
            embed.add_field(name="Сообщение:",
                            value=message.Text,
                            inline=True)
            embed.add_field(name="Отправлено:",
                            value=str(message.Created),
                            inline=True)

            if iter == 1:
                page = Page(embeds=[embed])
            else:
                page.embeds.append(embed)
            if iter == 10:
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

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.type == MessageType.new_member:
            return
        if len(message.content) == 0:
            return
        member = session.query(Member) \
            .filter(Member.ServerId == message.guild.id) \
            .filter(Member.MemberId == message.author.id).first()

        saveMessage = Message(member.Id, message.channel.id, message.content)
        session.add(saveMessage)
        session.commit()


def setup(client):
    client.add_cog(Memory(client))
