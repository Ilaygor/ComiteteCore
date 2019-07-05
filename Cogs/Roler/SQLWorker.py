import sqlite3
import os

conn = sqlite3.connect("Cogs/Roler/RoleList.db")

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
