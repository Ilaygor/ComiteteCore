import discord
from discord.ext.commands import TextChannelConverter
from discord.ext import commands
import os 
import json
from . import Memes_name_subject_to_change as mem

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="memes", help="Генерирует мем.\nМемы:\n> ahshit - мем про cj, требует ссылку на изображение в Данные_мема или приложеное изображение.\n> sayher - мем про парня и девушку, требует любой текст в Данные_мема.\n> tobe - jojo мем to be continued, требует ссылку на изображение в Данные_мема или приложеное изображение.",usage="Мем Данные_мема",brief="Мемген")
    async def memes(self,ctx,memname=None,*args):
        #await ctx.message.delete()
        if os.path.exists('src/Images/memes/{}.json'.format(memname)):
            typeMem=json.loads(open('src/Images/memes/{}.json'.format(memname)).read())['type']
            if (typeMem=='onetext'):
                text=' '.join(args)
                path=mem.CreateMem(memname,text)

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