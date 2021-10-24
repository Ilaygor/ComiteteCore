import discord
from discord.ext import commands
import os
import logging
from discord_slash import SlashCommand


logging.basicConfig(filename="Bot.log", level=logging.INFO)

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', description='Amadeus Kurisu', intents=intents)
slash = SlashCommand(client, sync_commands=True, )


@client.event
async def on_ready():
    logging.info('Logged in as')
    logging.info(client.user.name)
    logging.info(client.user.id)
    logging.info("-------------------------\n")


if __name__ == '__main__':
    for cog in os.listdir("Cogs"):
        try:
            client.load_extension(".".join(["Cogs", cog]))
            logging.info("{} - DONE".format(cog))
        except Exception as error:
            logging.error("{} - ERROR [{}]".format(cog, error))
    logging.info("-------------------------\n")

    client.run(open('AccessToken', 'r').read())
