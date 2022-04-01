import discord
from discord.ext import commands

from models.BoostLists import BoostList
from models.database import Session

session = Session()


async def list(ctx):
    boostLists = session.query(BoostList).filter(BoostList.ServerId == ctx.guild.id).all()
    embed = discord.Embed(title="Cписок Boost каналов :",
                          description="Каналы в которых бот учитывает XP в двойном объёме.")
    for boostList in boostLists:
        channel = ctx.guild.get_channel(boostList.ChannelId)
        if channel:
            embed.add_field(name=channel.name, inline=False,
                            value="Добавлен: " + str(boostList.CreatedTime))
        else:
            boostList.delete()
            session.commit()

    return embed


async def add(ctx, channel):

    channelSql = session.query(BoostList)\
        .filter(BoostList.ServerId == ctx.guild.id)\
        .filter(BoostList.ChannelId == channel.id).first()
    if not channelSql:
        newList = BoostList(channelId=channel.id, serverId=ctx.guild.id)
        session.add(newList)
        session.commit()
        embed = discord.Embed(title="Канал {} успешно добавлен в список игнора.".format(channel.name))
    else:
        embed = discord.Embed(title="Канал {} уже добавлен в список игнора.".format(channel.name))
    return embed


async def remove(ctx, channel):
    channelSql = session.query(BoostList)\
        .filter(BoostList.ServerId == ctx.guild.id)\
        .filter(BoostList.ChannelId == channel.id).first()
    if channelSql:
        session.delete(channelSql)
        session.commit()
        embed = discord.Embed(title="Канал {} успешно удалён из списока игнора.".format(channel.name))
    else:
        embed = discord.Embed(title="Канал {} отсутсвует в списоке игнора.".format(channel.name))
    return embed
