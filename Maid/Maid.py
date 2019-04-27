from discord import File,Member
from discord.ext import commands
from discord.ext.commands import MemberConverter,TextChannelConverter
import Okari, ExpSys
import Memes_name_subject_to_change as mem
import os

bot = commands.Bot(command_prefix='NM!', description='Сomitete System')

async def is_owner(ctx):
    return ctx.author.id == 269860812355665921

def is_testserver(ctx):
    return ctx.guild.id == 198889006006665216

infochan=198892670456692737

@bot.event
async def on_ready():
    print('ExpSys --------- '+ExpSys.init())
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)   

#BotCommands
@bot.command(name="@integrate")
@commands.check(is_owner)
async def integrate(ctx,*args):
    for i in ctx.guild.members:
        path=Okari.AddMember(i)
        os.remove(path)  
        ExpSys.AddMem(i.id)
    await ctx.send("Done")

@bot.command(name="@clear")
@commands.check(is_owner)
async def clear(ctx,chan,count):
    channel=await TextChannelConverter().convert(ctx,chan)
    async for i in channel.history(limit=int(count)):
        if i.author.id==bot.user.id:
            await i.delete()
    await ctx.send("Done")

@bot.command(name="@addmem")
@commands.check(is_owner)
async def addmem(ctx,*args):
    if args:
        author=await MemberConverter().convert(ctx,args[0])
    else:
        author=ctx.author
    ExpSys.AddMem(ctx.author.id)
    path=Okari.AddMember(author)
    file=File(path,filename="Member.png")
    await ctx.send(file=file)
    os.remove(path)  

@bot.command(name="@levelup")
@commands.check(is_owner)
async def levelup(ctx,level):
    await ExpSys.levelUp(ctx.channel,ctx.author.id,int(level))

@bot.command(name="@addexp")
@commands.check(is_owner)
async def addexp(ctx,arg1,arg2):
    author=await MemberConverter().convert(ctx,arg1)
    await ExpSys.AddExp(author.id,arg2,ctx.channel)

@bot.command(name="@lostmem")
@commands.check(is_owner)
async def lostmem(ctx):
    ExpSys.DelMem(ctx.author.id)
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
    if is_testserver(mem):
        path=Okari.AddMember(mem)
        ExpSys.AddMem(mem.id)
        file=File(path,filename="MemJoin.png")
        await mem.guild.get_channel(infochan).send(file=file)
        os.remove(path)

@bot.event
async def on_member_remove(mem):
    if is_testserver(mem):
        path=Okari.LostMember(mem)
        ExpSys.DelMem(mem.id)
        file=File(path,filename="MemRemove.png")
        await mem.guild.get_channel(infochan).send(file=file)
        os.remove(path)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if is_testserver(message):
        await ExpSys.AddExp(message.author.id,len(message.content)/10,message.channel)
        
bot.run(open('Maid/AccessToken','r').read())