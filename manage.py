import discord
import asyncio
from Aquarius.Okari import AddMember

bot = discord.Client()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


'''
@bot.event
async def on_member_join(mem):
    AddMember(mem)
'''
@bot.event
async def on_message(message):
    if message.author.id != bot.user.id:
        await bot.send_file(message.channel,AddMember(message.author))

bot.run(open('AccessToken','r').read())

