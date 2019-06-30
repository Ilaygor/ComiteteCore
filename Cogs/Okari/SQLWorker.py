import sqlite3
import os

conn = sqlite3.connect("BotDB.db")

def CheckMember(serverid,id):
    return conn.cursor().execute("SELECT count(id) FROM Members WHERE ServerID ={} and id={}".format(serverid,id)).fetchone()[0]>=1

def GetInfoChan(serverid):
    return conn.cursor().execute("SELECT infoChan FROM Servers WHERE id=?",[serverid]).fetchone()[0]

def GetStat(id):
    return conn.cursor().execute("SELECT (SELECT count(id) FROM Members WHERE ServerID={}) as 'all',(SELECT count(id) FROM Members WHERE IsAlive=0 and ServerID={}) as deactive ,(SELECT count(id) FROM Members WHERE IsAlive=1 and ServerID={}) as active FROM Members".format(id,id,id)).fetchone()

def AddNewmem(serverid,id):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Members ('id',ServerID) VALUES ({},{})".format(id,serverid))
    conn.commit()

def ReactivateMember(serverid,id):
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET isAlive=1 WHERE id={} and ServerID={}".format(id,serverid))
    conn.commit()

def DeactivateMember(serverid,id):
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET isAlive=0 WHERE id={} and ServerID={}".format(id,serverid))
    conn.commit()