import sqlite3
import os
import datetime

conn = sqlite3.connect("Cogs/GuildMaster (Admin Module)/RoleList.db")
bot = sqlite3.connect("BotDB.db")






def CreateColorRole(ServerID,RoleID):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ColorRoleList (ServerId,RoleId) VALUES (?,?);",[ServerID,RoleID])
    conn.commit()
def IsColorRole(ServerID,RoleID):
    return conn.cursor().execute("SELECT count(RoleId) FROM ColorRoleList WHERE ServerId ={} and RoleId={}".format(ServerID,RoleID)).fetchone()[0]>=1
def DeleteColorRole(ServerID,RoleID):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ColorRoleList WHERE ServerId ={} and RoleId={} ;".format(ServerID,RoleID))
    conn.commit()
def GetColorRoles(ServerID):
    return conn.cursor().execute("SELECT RoleId FROM ColorRoleList WHERE  ServerId=?",[serverid])