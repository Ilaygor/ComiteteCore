import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class Cleaner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='clear', description="Чистит канал от сообщений ботов.")
    async def clear(self, ctx,
                    channel: Option(discord.TextChannel, 'Выберите пользователя, которому выдаём Вотум', required=False, default=None),
                    count: Option(int, 'Число последний сообщений, которые нужно удалить', required=False, default=10, min_value=1, max_value=500)):
        if not channel:
            channel = ctx.channel
        async for i in channel.history(limit=int(count)):
            if i.author.id == self.bot.user.id:
                await i.delete()
        return await ctx.send("Чат очищен успешно")


def setup(client):
    client.add_cog(Cleaner(client))
