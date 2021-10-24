import discord
from discord.ext import commands
import datetime
from . import SQLWorker

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == ctx.guild.owner_id or ctx.author.id == 269860812355665921
    return commands.check(predicate)

class GuildMaster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="returnroles", help="Возвращают текущему пользователю роли если они вдруг автоматически не вернулись при возвращении на сервер",usage="[@Пользователь]",brief="Возвращение ролей")
    async def returnroles(self,ctx,member=None):
        if (member):
            author=await commands.MemberConverter().convert(ctx,member)
        else:
            author=ctx.author

        embed=discord.Embed(title="Cписок ролей:", description="Роли пользователя "+author.name,color=author.color)
        for i in SQLWorker.GetRoles(ctx.guild.id, author.id):
            role= ctx.guild.get_role(int(i[0]))
            if role:
                if role in author.roles:
                    embed.add_field(name=role.name, inline=True, value=str(i[0]))
                else:
                    try:
                        await author.add_roles(role)
                        embed.add_field(name=role.name+" (Возврашено)", inline=True, value=str(i[0]))
                    except discord.errors.Forbidden:
                        embed.add_field(name=role.name+" (Missing Permissions)", inline=True, value=str(i[0]))
            else:
                embed.add_field(name="Роль не найдена и удалена из БД", inline=True, value=str(i[0]))
                SQLWorker.DelRole(i[0])
        await ctx.send(embed=embed)

    @commands.command(name="tocolor", brief="Переключает существующую роль в цветную.",usage="[имя или пинг или id роли]",help="Переключает существующую роль в цветную. Требует ввести Имя или Пинг или id роли. Можно ввести несколько.")
    @is_owner()
    async def tocolor(self,ctx,*name):
        for i in name:
            try:
                role=await commands.RoleConverter().convert(ctx,i)
            except commands.errors.BadArgument:
                await ctx.send("Роль {} не найдена!".format(i))
                pass
            SQLWorker.CreateColorRole(ctx.guild.id, role.id)
            await ctx.send("Теперь роль {} - цветная!".format(role))
    @commands.command(name="tosimple", brief="Переключает существующую роль в обычную.",usage="[имя или пинг или id роли]",help="Переключает существующую роль в обычную. Требует ввести Имя или Пинг или id роли. Можно ввести несколько.")
    @is_owner()
    async def tosimple(self,ctx,*name):
        for i in name:
            try:
                role=await commands.RoleConverter().convert(ctx,i)
            except commands.errors.BadArgument:
                await ctx.send("Роль {} не найдена!".format(i))
                pass
            SQLWorker.DeleteColorRole(ctx.guild.id, role.id)
            await ctx.send("Теперь роль {} - обычная!".format(role))
    @commands.command(name="changecolor", brief="Изменяет цвет цветной роли.",usage="[имя или пинг или id роли] [цвет]",help="Изменяеи цвеи цветной роли. Требует ввести Имя или Пинг или id роли, а также цвет роли в HEX (#99AAB5), чтобы изменить цвет роли.")
    async def changecolor(self,ctx,name,color):
        try:
            role=await commands.RoleConverter().convert(ctx,name)
        except commands.errors.BadArgument:
            await ctx.send("Роль {} не найдена!".format(name))
            return

        if role in ctx.author.roles:
            if SQLWorker.IsColorRole(ctx.guild.id, role.id):
                colored=await commands.ColourConverter().convert(ctx,color)
                await role.edit(colour=colored)
                await ctx.send("Цвет роли {} успешно изменён".format(role))
            else:
                await ctx.send("Цвет роли {} нельзя изменить т.к. это не цветная роль.".format(role)) 
        else:
            await ctx.send("Роль {} не принадлежит вам!".format(role))
        
    @commands.command(name="mycolors", brief="Выводит список ролей цвет которых вы можете изменить.",usage="",help="Выводит список ролей цвет которых вы можете изменить.")
    async def mycolors(self,ctx):
        embed=discord.Embed(title="Cписок ролей:", description="Роли пользователя {}, цвет которых можно изменить.".format(ctx.author.name),color=ctx.author.color)
        for i in ctx.author.roles:
            if SQLWorker.IsColorRole(ctx.guild.id, i.id):
                embed.add_field(name=i.name, inline=False, value=i.color)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self,role):
        if SQLWorker.IsColorRole(role.guild.id, role.id):
            SQLWorker.DeleteColorRole(role.guild.id, role.id)






def setup(client):
    client.add_cog(GuildMaster(client))