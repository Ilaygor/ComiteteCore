import sqlite3
import os
from datetime import datetime

conn = sqlite3.connect("BotDB.db")
role = sqlite3.connect("Cogs/Roler/RoleList.db")

def SetInfoChan(serverid,channelid):
    cursor = conn.cursor()
    cursor.execute("UPDATE Servers SET infoChan=? WHERE id=?",[channelid,serverid])
    conn.commit()

def AddIgnorList(channelID,serverid):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO IgnorList (ChannelID,ServerID,TimeStamp) VALUES (?,?,?);",[channelID,serverid,datetime.now().timestamp()])
    conn.commit()

def DelIgnorList(channelID,serverid):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM IgnorList WHERE ChannelID = ? and ServerID=?;",[channelID,serverid])
    conn.commit()

def GetIgnorList(serverid):
    return conn.cursor().execute("SELECT channelID,TimeStamp FROM IgnorList WHERE ServerID=?",[serverid])

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

def checkChennel(serverid,channelid):
    return conn.cursor().execute("SELECT count(channelid) FROM IgnorList WHERE ServerID ={} and ChannelID={}".format(serverid,channelid)).fetchone()[0]>=1

def CheckRole(serverid,id,RoleId):
    return role.cursor().execute("SELECT count(RoleId) FROM RoleList WHERE RoleId={} and ServerID ={} and UserId={}".format(RoleId,serverid,id)).fetchone()[0]>=1
def AddRoles(serverid,id,RoleId):
    cursor = role.cursor()
    cursor.execute("INSERT INTO RoleList (RoleId,ServerId,UserId) VALUES (?,?,?);",[RoleId,serverid,id])
    role.commit()
def DelRole(RoleId):
    cursor = role.cursor()
    cursor.execute("DELETE FROM RoleList WHERE RoleId=?",[RoleId])
    role.commit()