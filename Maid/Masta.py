import sqlite3

conn = sqlite3.connect("AquariusDB.db")

def AddNewLabmem(id):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO labmems ('DiscordID')VALUES (?)",[id])
    conn.commit()

def CheckMember(id):
    cursor = conn.cursor()
    return cursor.execute("SELECT count(LabmemNum)as 'c' FROM LabMems WHERE DiscordID=?",[id]).fetchone()[0]==1
