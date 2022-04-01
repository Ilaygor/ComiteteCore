import discord
from discord.ext import commands

from models.IgnorLists import IgnoreList
from models.database import Session

session = Session()


async def list(ctx):
    ignoreLists = session.query(IgnoreList).filter(IgnoreList.ServerId == ctx.guild.id).all()
    embed = discord.Embed(title="Cписок игнорируемых каналов:",
                          description="Каналы в которых бот не учитывает XP.")
    for ignoreList in ignoreLists:
        channel = ctx.guild.get_channel(ignoreList.ChannelId)
        if channel:
            embed.add_field(name=channel.name, inline=False,
                            value="Добавлен: " + str(ignoreList.CreatedTime))
        else:
            ignoreList.delete()
            session.commit()

    return embed


async def add(ctx, channel):
    channelSql = session.query(IgnoreList)\
        .filter(IgnoreList.ServerId == ctx.guild.id)\
        .filter(IgnoreList.ChannelId == channel.id).first()
    if not channelSql:
        newList = IgnoreList(channelId=channel.id, serverId=ctx.guild.id)
        session.add(newList)
        session.commit()
        embed = discord.Embed(title="Канал {} успешно добавлен в список игнора.".format(channel.name))
    else:
        embed = discord.Embed(title="Канал {} уже добавлен в список игнора.".format(channel.name))
    return embed


async def remove(ctx, channel):
    channelSql = session.query(IgnoreList)\
        .filter(IgnoreList.ServerId == ctx.guild.id)\
        .filter(IgnoreList.ChannelId == channel.id).first()
    if channelSql:
        session.delete(channelSql)
        session.commit()
        embed = discord.Embed(title="Канал {} успешно удалён из списока игнора.".format(channel.name))
    else:
        embed = discord.Embed(title="Канал {} отсутсвует в списоке игнора.".format(channel.name))
    return embed
