import discord
from discord.ext.commands import TextChannelConverter
from discord.ext import commands
import os 
import json
from . import Memes_name_subject_to_change as mem

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="memlist", help="Выводит список мемов.",usage="",brief="Выводит список мемов")
    async def memlist(self,ctx):
        embed=discord.Embed(title="Cписок мемов:", description="Мемы которые может сгенерировать бот.")
        for file in os.listdir('src/Images/memes'):
            if file.endswith("json"):
                descript=open('src/Images/memes/{}'.format(file), encoding="utf-8", errors='ignore').read()
                print(descript)
                embed.add_field(name=file.split('.')[0] ,inline=False,
                value=json.loads(descript)['description'])
        await ctx.send(embed=embed)

    @commands.command(name="memes", help="Генерирует мем. Более подробно о мемах можно узнать коммандой NM!memlist ",usage="Мем Данные_мема",brief="Мемген")
    async def memes(self,ctx,memname=None,*args):
        #await ctx.message.delete()
        if os.path.exists('src/Images/memes/{}.json'.format(memname)):
            typeMem=json.loads(open('src/Images/memes/{}.json'.format(memname)).read())['type']
            if (typeMem=='onetext'):
                path=mem.CreateMem(memname,' '.join(args))

            elif(typeMem=='image'):
                if len(args)>=1:
                    urltoPic=args[0]
                else:
                    urltoPic=ctx.message.attachments[0].url
                path=mem.CreateVisualMem(memname,urltoPic)
                if (not path):
                    await ctx.send("URL не корректен!")
                    return
            file=discord.File(path,filename=memname+".png")
            await ctx.send(file=file)
            os.remove(path)
        elif not memname:
            await ctx.send("Не указано имя мема. Воспользуйтесь коммандой `NM!help memes`, чтобы получить больше информации.")
        else:
            await ctx.send("Мем с именем {} не найден!".format(args[0]))

def setup(client):
    client.add_cog(Memes(client))