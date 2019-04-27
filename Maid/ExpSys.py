import sqlite3
import discord
from discord import File
import Okari
import os

conn = sqlite3.connect("AquariusDB.db")

UsersData={}

bot=discord.ext.commands.Bot

def init():
    for i in conn.cursor().execute("SELECT DiscordID,Xp,MaxXP,Level FROM LabMems WHERE IsActive=1"):
        UsersData[i[0]]={
            'level':i[3],
            'xp':i[1],
            'maxxp':i[2]
        }
    return 'done'

async def levelUp(channel,id,level):
    mem=channel.guild.get_member(id)
    path="Maid/src/Images/Temp/"+str(id)+".png"

    Okari.CreateLevelUpMessage(mem.avatar_url_as(size=128),mem.name,str(level)).save(path, format="png")
    
    file=File(path,filename="LevelUp.png")
    await channel.send(file=file)
    os.remove(path) 

def AddMem(id):
    usr=conn.cursor().execute("SELECT xp,MaxXP,level FROM LabMems WHERE DiscordID=?",[id]).fetchone()
    UsersData[id]={
        'level':usr[2],
        'xp':usr[0],
        'maxxp':usr[1]
    }

def DelMem(id):
    UsersData.pop(id)

async def AddExp(id,count,channel):
    try:
        user=UsersData[id]
    except KeyError:
        return
    user['xp']+=float(count)
    await checkXp(user,id,channel)
    
async def checkXp(user,id,channel):
    if (user['maxxp']>=user['xp']):
        cursor = conn.cursor()
        cursor.execute("UPDATE LabMems SET Xp=?,MaxXP=?,Level=? WHERE DiscordID=?",[user['xp'],user['maxxp'],user['level'],id])
        conn.commit()
    else:
        user['xp']-=user['maxxp']
        user['maxxp']*=1.5
        user['level']+=1
        await levelUp(channel,id,user['level'])
        await checkXp(user,id,channel)