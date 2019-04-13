import discord
from discord.ext import commands
import Maid.Okari as Okari
import os

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#BotCommands
@bot.command(name="@addmem")
async def addmem(ctx):
    path=Okari.AddMember(ctx.author)
    file=discord.File(path,filename="Newmember.png")
    await ctx.send(file=file)
    os.remove(path)

@bot.command(name="@lostmem")
async def lostmem(ctx):
    path=Okari.LostMember(ctx.author)
    file=discord.File(path,filename="LostMem.png")
    await ctx.send(file=file)
    os.remove(path)

@bot.command(name="@returnmem")
async def returnmem(ctx):
    path=Okari.ReturnMember(ctx.author)
    file=discord.File(path,filename="ReturnMem.png")
    await ctx.send(file=file)
    os.remove(path)

#MemberEvents
@bot.event
async def on_member_join(mem):
    path=Okari.AddMember(mem)
    file=discord.File(path,filename="Newmember.png")
    await mem.guild.get_channel(566000934493224962).send(file=file)
    os.remove(path)

@bot.event
async def on_member_remove(mem):
    path=Okari.LostMember(mem)
    file=discord.File(path,filename="Newmember.png")
    await mem.guild.get_channel(566000934493224962).send(file=file)
    os.remove(path)

'''
@bot.event
async def on_message(message):
    if message.author.id != bot.user.id:
        file=discord.File(AddMember(message.author),filename="Newmember.png")
        await message.channel.send(file=file)
'''
bot.run(open('Maid/AccessToken','r').read())

