from discord import File,Member
from discord.ext import commands
from discord.ext.commands import MemberConverter,TextChannelConverter
import Okari, ExpSys,Masta
import Memes_name_subject_to_change as mem
import os
import json

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
        if not i.bot:
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

@bot.command(name="setbg")
async def setbg(ctx,url=None):
    if url=="clear":
        os.remove("Maid/src/Images/Usr/"+str(ctx.author.id)+"/profile.png")
        await ctx.send('Задний фон удалён.')
    elif url:
        try:
            Okari.SetBG(ctx.author.id,url)
            path=Okari.CreateProfile(ctx.author)
            file=File(path,filename="profile.png")
            await ctx.send(file=file)
            os.remove(path)
        except:
            await ctx.send('Некорректная ссылка на изображение.')
    else:
        await ctx.send('Отсутсвует ссылка на изображение.')
    

@bot.command(name="top")
async def top(ctx,cat:str="exp", page:int="1"):
    members=[]
    page=int(page)
    if cat == 'exp':
        for i in Masta.GetTopMembers(page-1):
            members.append({
                "mem":ctx.guild.get_member(i[0]),
                "data":str(round(i[1],2))+" xp"
            })
    elif cat=="men":
        for i in Masta.GetTopMenMembers(page-1):
            members.append({
                "mem":ctx.guild.get_member(i[0]),
                "data":str(round(i[1],2))+" mentions"
            })
    else:
        await ctx.send("Параметр не найден!")
        return

    path=Okari.GetTop(members,page-1)
    file=File(path,filename="LostMem.png")
    await ctx.send(file=file)
    os.remove(path)

@bot.command(name="profile")
async def profile(ctx,member=None):
    if (member):
        author=await MemberConverter().convert(ctx,member)
    else:
        author=ctx.author
    path=Okari.CreateProfile(author)
    file=File(path,filename="profile.png")
    await ctx.send(file=file)
    os.remove(path)



#memes
@bot.command(name="memes")
async def memes(ctx,memname,*args):
    if os.path.exists('Maid/src/Images/memes/{}.json'.format(memname)):
        typeMem=json.loads(open('Maid/src/Images/memes/{}.json'.format(memname)).read())['type']
        if (typeMem=='onetext'):
            text=' '.join(args)
            path=mem.CreateMem(memname,text)

        elif(typeMem=='image'):
            path=mem.CreateVisualMem(memname,args[0])
            if (not path):
                await ctx.send("URL не корректен!")
                return
        file=File(path,filename=memname+".png")
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
    if is_testserver(message)and not message.author.bot and not message.channel.id==323061768714846208:
        if (len(message.mentions)):
            for i in list(set(message.mentions)):
                if not i.bot and not message.author.bot and not i.id==message.author.id:
                    ExpSys.AddMention(i.id)

        await ExpSys.AddExp(message.author.id,len(message.content)/10,message.channel)
        
bot.run(open('Maid/AccessToken','r').read())