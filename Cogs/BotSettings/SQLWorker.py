import sqlite3
import os
from datetime import datetime

conn = sqlite3.connect("BotDB.db")
role = sqlite3.connect("Cogs/GuildMaster/RoleList.db")

def SetInfoChan(serverid,channelid):
    cursor = conn.cursor()
    cursor.execute("UPDATE Servers SET infoChan=? WHERE id=?",[channelid,serverid])
    conn.commit()

def SetMemName(serverid,name):
    cursor = conn.cursor()
    cursor.execute("UPDATE Servers SET MemName=? WHERE id=?",[name,serverid])
    conn.commit()

def SetBanText(serverid,text):
    cursor = conn.cursor()
    cursor.execute("UPDATE Servers SET BanText=? WHERE id=?",[text,serverid])
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

def SetAlive(memberid,serverid):
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET IsAlive=1 WHERE id=? and ServerID=?",[memberid,serverid])
    conn.commit()

def SetDead(memberid,serverid):
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET IsAlive=0 WHERE id=? and ServerID=?",[memberid,serverid])
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

def AddEmoji(ServerID,EmojiID):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Emojies (EmojiID,ServerID) VALUES ({},{})".format(EmojiID,ServerID))
    conn.commit()

def CheckEmoji(ServerID,EmojiID):
    return conn.cursor().execute("SELECT count(EmojiID) FROM Emojies WHERE ServerID ={} and EmojiID={}".format(ServerID,EmojiID)).fetchone()[0]>=1


def CheckServer(ServerID):
    return conn.cursor().execute("SELECT count(id) FROM Servers WHERE id ={}".format(ServerID)).fetchone()[0]>=1

def AddServer(ServerID):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Servers (id) VALUES ({})".format(ServerID))
    conn.commit()