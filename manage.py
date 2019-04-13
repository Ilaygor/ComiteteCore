import discord
from discord.ext import commands
from Aquarius.Okari import AddMember

bot = commands.Bot(command_prefix='!@')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#BotCommands
@bot.command()
async def addmem(ctx):
    file=discord.File(AddMember(ctx.author),filename="Newmember.png")
    await ctx.send(file=file)



#MemberEvents
@bot.event
async def on_member_join(mem):
    file=discord.File(AddMember(mem.author),filename="Newmember.png")
    await bot.get_channel(566000934493224962).send(file=file)

'''
@bot.event
async def on_message(message):
    if message.author.id != bot.user.id:
        file=discord.File(AddMember(message.author),filename="Newmember.png")
        await message.channel.send(file=file)
'''
bot.run(open('AccessToken','r').read())

