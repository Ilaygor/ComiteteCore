import sqlite3
import os

conn = sqlite3.connect("BotDB.db")

def GetMemInfo(id,serverid):
    return conn.cursor().execute("SELECT level,Xp,MaxXP,Mentions,TotalXp FROM Members WHERE id=? and ServerID=?",[id,serverid]).fetchone()

def GetRank(id,serverid):
    i1=0
    for i in conn.cursor().execute("SELECT id FROM Members Where IsAlive='1' and ServerID={} ORDER BY TotalXP DESC".format(serverid)).fetchall():
        i1+=1
        if i[0]==id:
            return i1

def SetInfo(id,serverid,text):
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET Info=? WHERE id=? and ServerID=?",[text,id,serverid])
    conn.commit()

def GetInfo(id,serverid):
    return conn.cursor().execute("SELECT info FROM Members WHERE id=? and ServerID=?",[id,serverid]).fetchone()[0]
