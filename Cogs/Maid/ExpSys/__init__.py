import sqlite3
import discord
from discord import File
import os
from . import PictureCreator

conn = sqlite3.connect("BotDB.db")

UsersData={}

def init():
    for i in conn.cursor().execute("SELECT id,Xp,MaxXP,Level,Mentions,TotalXP,ServerID FROM Members WHERE IsAlive=1"):
        UsersData[i[6],i[0]]={
            'level':i[3],
            'xp':i[1],
            'maxxp':i[2],
            'mentions':i[4],
            'TotalXP':i[5]
        }
    return 'done'

async def levelUp(channel,id,level):
    mem=channel.guild.get_member(id)
    path="Temp/"+str(id)+".png"

    PictureCreator.CreateLevelUpMessage(mem.avatar_url_as(size=128),mem.name,str(level)).save(path, format="png")
    
    file=File(path,filename="LevelUp.png")
    await channel.send(file=file)
    os.remove(path) 

def AddMem(id,serverid):
    usr=conn.cursor().execute("SELECT xp,MaxXP,level,Mentions,TotalXP FROM Members WHERE id=? and ServerID=?",[id,serverid]).fetchone()
    UsersData[serverid,id]={
        'level':usr[2],
        'xp':usr[0],
        'maxxp':usr[1],
        'mentions':usr[3],
        'TotalXP':usr[4]
    }

def DelMem(id,ServerID):
    UsersData.pop((ServerID,id))

def AddMention(id,ServerID):
    UsersData[ServerID,id]['mentions']+=1
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET Mentions=? WHERE id=? and ServerID=?",[UsersData[ServerID,id]['mentions'],id,ServerID])
    conn.commit()

async def AddExp(id,ServerID,count,channel):
    try:
        user=UsersData[ServerID,id]
    except KeyError:
        return
    user['xp']+=round(float(count),2)
    user['TotalXP']+=round(float(count),2)
    await checkXp(user,id,ServerID,channel)

async def checkXp(user,id,ServerID,channel):
    if (user['maxxp']>=user['xp']):
        cursor = conn.cursor()
        cursor.execute("UPDATE Members SET Xp=?,MaxXP=?,Level=?,TotalXp=? WHERE id=? and ServerID=?",[round(user['xp'],2),round(user['maxxp'],2),user['level'],user['TotalXP'],id,ServerID])
        conn.commit()
    else:
        user['xp']-=user['maxxp']
        user['maxxp']*=1.5
        user['level']+=1
        await levelUp(channel,id,user['level'])
        await checkXp(user,id,ServerID,channel)

def checkChennel(serverid,channelid):
    return conn.cursor().execute("SELECT count(channelid) FROM IgnorList WHERE ServerID ={} and ChannelID={}".format(serverid,channelid)).fetchone()[0]>=1