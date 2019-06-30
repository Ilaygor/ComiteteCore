import sqlite3
import os

conn = sqlite3.connect("BotDB.db")

def GetMemInfo(id):
    return conn.cursor().execute("SELECT level,Xp,MaxXP,Mentions FROM Members WHERE id=?",[id]).fetchone()

def GetTopMembers(page):
    users=5*page
    return conn.cursor().execute("SELECT id,(Xp+MaxXP*Level) FROM Members Where IsAlive='1' ORDER BY Level DESC,MaxXP DESC,Xp DESC LIMIT ?,?",[0+users,5+users])

def GetTopMenMembers(page):
    users=5*page
    return conn.cursor().execute("SELECT id,Mentions FROM Members Where IsAlive='1' ORDER BY Mentions DESC LIMIT ?,?",[0+users,5+users])


