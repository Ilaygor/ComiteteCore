from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option


class Cleaner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='clear',
        description="Чистит канал от сообщений бота.",
        options=[
            create_option(
                name="channel",
                description="Пинг Канала который нужно очистить",
                required=False,
                option_type=SlashCommandOptionType.CHANNEL
            ),
            create_option(
                name="count",
                description="Число последний сообщений среди которых нужно удалить",
                required=False,
                option_type=SlashCommandOptionType.INTEGER
            )
        ]
    )
    async def clear(self, ctx, channel=None, count=100):
        if not channel:
            channel = ctx.channel
        async for i in channel.history(limit=int(count)):
            if i.author.id == self.bot.user.id:
                await i.delete()


def setup(client):
    client.add_cog(Cleaner(client))
