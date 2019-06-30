import sqlite3
import discord
from discord import File
import os
from . import PictureCreator

conn = sqlite3.connect("BotDB.db")

UsersData={}

def init():
    for i in conn.cursor().execute("SELECT id,Xp,MaxXP,Level,Mentions FROM Members WHERE IsAlive=1"):
        UsersData[i[0]]={
            'level':i[3],
            'xp':i[1],
            'maxxp':i[2],
            'mentions':i[4]
        }
    return 'done'

async def levelUp(channel,id,level):
    mem=channel.guild.get_member(id)
    path="Temp/"+str(id)+".png"

    PictureCreator.CreateLevelUpMessage(mem.avatar_url_as(size=128),mem.name,str(level)).save(path, format="png")
    
    file=File(path,filename="LevelUp.png")
    await channel.send(file=file)
    os.remove(path) 

def AddMem(id):
    usr=conn.cursor().execute("SELECT xp,MaxXP,level,Mentions FROM Members WHERE id=?",[id]).fetchone()
    UsersData[id]={
        'level':usr[2],
        'xp':usr[0],
        'maxxp':usr[1],
        'mentions':usr[3]
    }

def DelMem(id):
    UsersData.pop(id)

def AddMention(id):
    UsersData[id]['mentions']+=1
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET Mentions=? WHERE id=?",[UsersData[id]['mentions'],id])
    conn.commit()

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
        cursor.execute("UPDATE Members SET Xp=?,MaxXP=?,Level=? WHERE id=?",[user['xp'],user['maxxp'],user['level'],id])
        conn.commit()
    else:
        user['xp']-=user['maxxp']
        user['maxxp']*=1.5
        user['level']+=1
        await levelUp(channel,id,user['level'])
        await checkXp(user,id,channel)