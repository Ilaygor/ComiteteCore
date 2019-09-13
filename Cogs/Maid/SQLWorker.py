import sqlite3
import os
import datetime

conn = sqlite3.connect("BotDB.db")

def GetMemInfo(id,ServerID):
    return conn.cursor().execute("SELECT level,Xp,MaxXP,Mentions,TotalXp FROM Members WHERE id=?",[id]).fetchone()

def GetRank(id):
    i1=0
    for i in conn.cursor().execute("SELECT id FROM Members Where IsAlive='1' ORDER BY TotalXP DESC").fetchall():
        i1+=1
        if i[0]==id:
            return i1
            
def GetInfo(id):
    return conn.cursor().execute("SELECT info FROM Members WHERE id=?",[id]).fetchone()[0]

def GetTopMembers(page,ServerID):
    users=5*page
    return conn.cursor().execute("SELECT id,TotalXP FROM Members Where IsAlive='1' and ServerID=? ORDER BY TotalXP DESC LIMIT ?,?",[ServerID,0+users,5+users])
    
def GetTopMenMembers(page,ServerID):
    users=5*page
    return conn.cursor().execute("SELECT id,Mentions FROM Members Where IsAlive='1' and ServerID=? ORDER BY Mentions DESC LIMIT ?,?",[ServerID,0+users,5+users])

def GetTopEmojiMembers(page,serverID):
    emojies=5*page
    return conn.cursor().execute("SELECT EmojiID,Count FROM Emojies Where ServerID=? ORDER BY Count DESC LIMIT ?,?",[serverID,0+emojies,5+emojies])

def IncEmoji(ServerID,EmojiID):
    if CheckEmoji(ServerID,EmojiID):
        cursor = conn.cursor()
        time=int(str(datetime.datetime.now().timestamp()).split('.')[0])
        count = cursor.execute("SELECT Count FROM Emojies WHERE ServerID ={} and EmojiID={}".format(ServerID,EmojiID)).fetchone()[0]
        count+=1
        cursor.execute("UPDATE Emojies SET Count={},LastUsage={} WHERE ServerID ={} and EmojiID={}".format(count,time,ServerID,EmojiID))
        conn.commit()

def CheckEmoji(ServerID,EmojiID):
    return conn.cursor().execute("SELECT count(EmojiID) FROM Emojies WHERE ServerID ={} and EmojiID={}".format(ServerID,EmojiID)).fetchone()[0]>=1

