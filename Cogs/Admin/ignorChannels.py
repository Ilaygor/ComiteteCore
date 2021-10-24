import discord
from discord.ext.commands import TextChannelConverter
from discord.ext import commands
from datetime import datetime
import SQLWorker


async def list(ctx):
    IgnorList = SQLWorker.GetIgnorList(ctx.guild.id)
    embed = discord.Embed(title="Cписок игнорируемых каналов:",
                          description="Каналы в которых бот не учитывает XP.")
    for i in IgnorList:
        channel = ctx.guild.get_channel(i[0])
        if channel:
            embed.add_field(name=channel.name, inline=False,
                            value="Добавлен: " + str(datetime.fromtimestamp(i[1]).date()))
        else:
            SQLWorker.DelIgnorList(i[0], ctx.guild.id)
    return embed


async def add(ctx, channel):
    ch = await commands.TextChannelConverter().convert(ctx, channel)
    if not SQLWorker.checkChannel(ctx.guild.id, ch.id):
        SQLWorker.AddIgnorList(ch.id, ctx.guild.id)
        embed = discord.Embed(title="Канал {} успешно добавлен в список игнора.".format(ch.name))
    else:
        embed = discord.Embed(title="Канал {} уже добавлен в список игнора.".format(ch.name))
    return embed


async def remove(ctx, channel):
    ch = await TextChannelConverter().convert(ctx, channel)
    if SQLWorker.checkChannel(ctx.guild.id, ch.id):
        SQLWorker.DelIgnorList(ch.id, ctx.guild.id)
        embed = discord.Embed(title="Канал {} успешно удалён из списока игнора.".format(ch.name))
    else:
        embed = discord.Embed(title="Канал {} отсутсвует в списоке игнора.".format(ch.name))
    return embed
