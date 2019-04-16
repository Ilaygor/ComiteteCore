from discord import File,Member
from discord.ext import commands
from discord.ext.commands import MemberConverter
import Okari
import Memes_name_subject_to_change as mem
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
async def addmem(ctx,*args):
    if args:
        author=await MemberConverter().convert(ctx,args[0])
    else:
        author=ctx.author
    path=Okari.AddMember(author)
    file=File(path,filename="Member.png")
    await ctx.send(file=file)
    os.remove(path)    

@bot.command(name="@lostmem")
async def lostmem(ctx):
    path=Okari.LostMember(ctx.author)
    file=File(path,filename="LostMem.png")
    await ctx.send(file=file)
    os.remove(path)

#memes

@bot.command(name="memes")
async def memes(ctx,*args):
    if os.path.exists('Maid/src/Images/memes/{}.json'.format(args[0])):
        path=mem.CreateMem(args[0],' '.join(args[1:]))
        file=File(path,filename=args[0]+".png")
        await ctx.send(file=file)
        os.remove(path)
    else:
        await ctx.send("Мем с именем {} не найден!".format(args[0]))

#MemberEvents
@bot.event
async def on_member_join(mem):
    path=Okari.AddMember(mem)
    file=File(path,filename="MemJoin.png")
    await mem.guild.get_channel(566000934493224962).send(file=file)
    os.remove(path)

@bot.event
async def on_member_remove(mem):
    path=Okari.LostMember(mem)
    file=File(path,filename="MemRemove.png")
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