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

    @commands.Cog.listener()
    async def on_member_join(self,member):
        if not member.bot:
            jr= SQLWorker.GetJoinRole(member.guild.id)
            if jr:
                await member.add_roles(member.guild.get_role(int(jr)))

            for i in SQLWorker.GetRoles(member.guild.id,member.id):
                try:
                    await member.add_roles(member.guild.get_role(int(i[0])))
                except AttributeError:
                    SQLWorker.DelRole(i[0])
                except discord.errors.Forbidden:
                    pass
    
    @commands.command(name="returnroles", help="Возвращают текущему пользователю роли если они вдруг автоматически не вернулись при возвращении на сервер",usage="[@Пользователь]",brief="Возвращение ролей")
    async def returnroles(self,ctx,member=None):
        if (member):
            author=await commands.MemberConverter().convert(ctx,member)
        else:
            author=ctx.author

        embed=discord.Embed(title="Cписок ролей:", description="Роли пользователя "+author.name,color=author.color)
        for i in SQLWorker.GetRoles(ctx.guild.id,author.id):
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
            SQLWorker.CreateColorRole(ctx.guild.id,role.id)
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
            SQLWorker.DeleteColorRole(ctx.guild.id,role.id)
            await ctx.send("Теперь роль {} - обычная!".format(role))
    @commands.command(name="changecolor", brief="Изменяет цвет цветной роли.",usage="[имя или пинг или id роли] [цвет]",help="Изменяеи цвеи цветной роли. Требует ввести Имя или Пинг или id роли, а также цвет роли в HEX (#99AAB5), чтобы изменить цвет роли.")
    async def changecolor(self,ctx,name,color):
        try:
            role=await commands.RoleConverter().convert(ctx,name)
        except commands.errors.BadArgument:
            await ctx.send("Роль {} не найдена!".format(name))
            return

        if role in ctx.author.roles:
            if SQLWorker.IsColorRole(ctx.guild.id,role.id):
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
            if SQLWorker.IsColorRole(ctx.guild.id,i.id):
                embed.add_field(name=i.name, inline=False, value=i.color)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self,role):
        if SQLWorker.IsColorRole(role.guild.id,role.id):
            SQLWorker.DeleteColorRole(role.guild.id,role.id)

    @commands.command(name="emojistat", help="Выводит статистику использования серверных эмоджи.",usage="",brief="Выводит статистику использования серверных эмоджи.")
    @is_owner()
    async def emojistat(self,ctx):
        emojies={}
        for i in ctx.guild.emojis:
            emojies.update({i.id:i})

        for i in SQLWorker.GetAllEmojie(ctx.guild.id):
            emoji=emojies.get(i[1])
            if emoji:
                embed=discord.Embed(title=emoji.name)
                embed.set_thumbnail(url=emoji.url)
                embed.add_field(name="Кол-во:", value=i[2], inline=True)
                embed.add_field(name="Последнее использование:", value=str(datetime.datetime.fromtimestamp(i[3])), inline=True)
                await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        if len(before.roles)< len(after.roles):
            for i in after.roles:
                if not i in before.roles and not SQLWorker.CheckRole(after.guild.id,after.id,i.id):
                    SQLWorker.AddRoles(after.guild.id,after.id,i.id)
        if len(before.roles)> len(after.roles):
            for i in before.roles:
                if not i in after.roles:
                    SQLWorker.DelRole(i.id)


    @commands.Cog.listener()
    async def on_guild_emojis_update(self,guild, before, after):
        if len(before)< len(after):
            for i in after:
                if not i in before and not SQLWorker.CheckEmoji(guild.id,i.id):
                    SQLWorker.AddEmoji(guild.id,i.id)
        if len(before)> len(after):
            for i in before:
                if not i in after:
                    SQLWorker.DelEmoji(i.id)

def setup(client):
    client.add_cog(GuildMaster(client))