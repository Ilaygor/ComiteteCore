from discord.ext import commands
import discord
import os;


client = commands.Bot(command_prefix='NM!', description='Сomitete System')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print("-------------------------\n")

if __name__ == '__main__':
    for extention in os.listdir("Cogs"):
        try:
            client.load_extension(".".join(["Cogs",extention]))
            print("{} - DONE".format(extention))
        except Exception as error:
            print ("{} - ERROR [{}]".format(extention,error))
    print("-------------------------\n")  
    client.run(open('AccessToken','r').read())