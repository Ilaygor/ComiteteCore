import sqlite3
import os

conn = sqlite3.connect("BotDB.db")

def GetMemInfo(id):
    return conn.cursor().execute("SELECT level,Xp,MaxXP,Mentions,TotalXp FROM Members WHERE id=?",[id]).fetchone()

def GetRank(id):
    i1=0
    for i in conn.cursor().execute("SELECT id FROM Members Where IsAlive='1' ORDER BY TotalXP DESC").fetchall():
        i1+=1
        if i[0]==id:
            return i1

def SetInfo(id,text):
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET Info=? WHERE id=?",[text,id])
    conn.commit()

def GetInfo(id):
    return conn.cursor().execute("SELECT info FROM Members WHERE id=?",[id]).fetchone()[0]

def GetTopMembers(page):
    users=5*page
    return conn.cursor().execute("SELECT id,TotalXP FROM Members Where IsAlive='1' ORDER BY TotalXP DESC LIMIT ?,?",[0+users,5+users])
    
def GetTopMenMembers(page):
    users=5*page
    return conn.cursor().execute("SELECT id,Mentions FROM Members Where IsAlive='1' ORDER BY Mentions DESC LIMIT ?,?",[0+users,5+users])


