import sqlite3
import os

conn = sqlite3.connect("Cogs/GuildMaster/RoleList.db")
bot = sqlite3.connect("BotDB.db")
def GetRoles(serverid,id):
    return conn.cursor().execute("SELECT RoleId FROM RoleList WHERE UserId=? and ServerId=?",[id,serverid])

def AddRoles(serverid,id,RoleId):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO RoleList (RoleId,ServerId,UserId) VALUES (?,?,?);",[RoleId,serverid,id])
    conn.commit()
def DelRole(RoleId):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM RoleList WHERE RoleId=?",[RoleId])
    conn.commit()
def CheckRole(serverid,id,RoleId):
    return conn.cursor().execute("SELECT count(RoleId) FROM RoleList WHERE RoleId={} and ServerID ={} and UserId={}".format(RoleId,serverid,id)).fetchone()[0]>=1

def AddEmoji(ServerID,EmojiID):
    cursor = bot.cursor()
    cursor.execute("INSERT INTO Emojies (EmojiID,ServerID) VALUES ({},{})".format(EmojiID,ServerID))
    bot.commit()
def DelEmoji(EmojiID):
    cursor = bot.cursor()
    cursor.execute("DELETE FROM Emojies WHERE EmojiID=?",[EmojiID])
    bot.commit()
def CheckEmoji(ServerID,EmojiID):
    return bot.cursor().execute("SELECT count(EmojiID) FROM Emojies WHERE ServerID ={} and EmojiID={}".format(ServerID,EmojiID)).fetchone()[0]>=1

def GetJoinRole(ServerID):
    return bot.cursor().execute("SELECT JoinRole FROM Servers WHERE id=?",[ServerID]).fetchone()[0]