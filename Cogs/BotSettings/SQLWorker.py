import sqlite3
import os

conn = sqlite3.connect("BotDB.db")

def SetInfoChan(serverid,channelid):
    cursor = conn.cursor()
    cursor.execute("UPDATE Servers SET infoChan=? WHERE id=?",[channelid,serverid])
    conn.commit()

def GetMembers(serverid): 
    return conn.cursor().execute("SELECT id,IsAlive FROM Members WHERE ServerID=?",[serverid])

def SetAlive(memberid):
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET IsAlive=1 WHERE id=?",[memberid])
    conn.commit()

def SetDead(memberid):
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET IsAlive=0 WHERE id=?",[memberid])
    conn.commit()

def AddNewmem(serverid,id):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Members ('id',ServerID) VALUES ({},{})".format(id,serverid))
    conn.commit()