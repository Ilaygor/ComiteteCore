import sqlite3

conn = sqlite3.connect("AquariusDB.db")

def AddNewLabmem(id):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO labmems ('DiscordID')VALUES (?)",[id])
    conn.commit()

def GetTopMembers(page):
    users=10*page
    return conn.cursor().execute("SELECT DiscordID,(Xp+MaxXP*Level) FROM LabMems Where IsActive='1' ORDER BY Level DESC,MaxXP DESC,Xp DESC LIMIT ?,?",[0+users,10+users])

def CheckMember(id):
    return conn.cursor().execute("SELECT count(LabmemNum)as 'c' FROM LabMems WHERE DiscordID=?",[id]).fetchone()[0]==1

def DeactivateMember(id):
    cursor = conn.cursor()
    cursor.execute("UPDATE LabMems SET IsActive=0 WHERE DiscordID=?",[id])
    conn.commit()

def GetMemInfo(id):
    return conn.cursor().execute("SELECT level,Xp,MaxXP,Mentions,Title,Info FROM labmems WHERE DiscordID=?",[id]).fetchone()

def ReactivateMember(id):
    cursor = conn.cursor()
    cursor.execute("UPDATE LabMems SET IsActive=1 WHERE DiscordID=?",[id])
    conn.commit()

