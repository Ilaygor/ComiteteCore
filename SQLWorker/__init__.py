import sqlite3
import datetime

conn = sqlite3.connect("BotDB.db")


def GetStat(serverId):
    return conn.cursor() \
        .execute(
        "SELECT (SELECT count(id) FROM Members WHERE ServerID=?) as 'all',(SELECT count(id) FROM Members WHERE "
        "IsAlive=0 and ServerID=?) as deactive ,(SELECT count(id) FROM Members WHERE IsAlive=1 and ServerID=?) as "
        "active FROM Members ", [serverId, serverId, serverId]).fetchone()


def SetInfoChan(serverId, channelId):
    cursor = conn.cursor()
    cursor.execute("UPDATE Servers SET infoChan=? WHERE id=?",
                   [channelId, serverId])
    conn.commit()


def SetMemName(serverId, name):
    cursor = conn.cursor()
    cursor.execute("UPDATE Servers SET MemName=? WHERE id=?",
                   [name, serverId])
    conn.commit()


def GetMemName(serverId):
    return conn.cursor().execute("SELECT MemName FROM Servers WHERE id=?",
                                 [serverId]).fetchone()[0]


def SetJoinRole(serverId, roleid):
    cursor = conn.cursor()
    cursor.execute("UPDATE Servers SET JoinRole=? WHERE id=?",
                   [roleid, serverId])
    conn.commit()


def SetMuteRole(serverId, roleid):
    cursor = conn.cursor()
    cursor.execute("UPDATE Servers SET MuteRole=? WHERE id=?",
                   [roleid, serverId])
    conn.commit()


def CheckMuteRole(serverId):
    return conn.cursor().execute("SELECT count(MuteRole) FROM Servers WHERE id =?",
                                 [serverId]).fetchone()[0] >= 1


def GetMuteRole(serverId):
    return conn.cursor().execute("SELECT MuteRole FROM Servers WHERE id=?",
                                 [serverId]).fetchone()[0]


def MuteMember(roleId, userId, serverId, endTime):
    cursor = conn.cursor()

    cursor.execute("Insert INTO Mutes ('UserId', ServerId, RoleId, EndTime) VALUES (?,?,?,?)",
                   [userId, serverId, roleId, endTime])
    conn.commit()


def DelMute(MemberId, ServerId):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Mutes WHERE ServerId=? and UserId=?", [ServerId, MemberId])
    conn.commit()


def GetMuteMembers():
    return conn.cursor() \
        .execute("SELECT ServerId,UserId,RoleId,EndTime FROM Mutes")


def CreateVotum(serverId, channelId, memberId, messageId, endTime):
    conn.cursor() \
        .execute("Insert INTO Votums (ServerId, ChannelId, MessageId, UserId, EndTime) VALUES (?,?,?,?,?)",
                 [serverId, channelId, messageId, memberId, endTime])
    conn.commit()


def CheckVotum(memberId):
    return conn.cursor().execute("SELECT count(MessageId) FROM Votums WHERE UserId =?",
                                 [memberId]).fetchone()[0] >= 1


def GetVotums():
    return conn.cursor() \
        .execute("SELECT ServerId, MessageId, UserId, EndTime, ChannelId FROM Votums")


def DelVotum(ServerId, MessageId):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Votums WHERE ServerId=? and MessageId=?", [ServerId, MessageId])
    conn.commit()


def SetBanText(serverId, text):
    cursor = conn.cursor()
    cursor.execute("UPDATE Servers SET BanText=? WHERE id=?",
                   [text, serverId])
    conn.commit()


def CheckServer(serverId):
    return conn.cursor().execute("SELECT count(id) FROM Servers WHERE id =?",
                                 [serverId]).fetchone()[0] >= 1


def AddServer(serverId):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Servers (id) VALUES (?)",
                   [serverId])

    conn.commit()


def AddNewMem(serverId, memId):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Members ('id',ServerID) VALUES (?,?)",
                   [memId, serverId])
    conn.commit()


def GetMembers(serverId):
    return conn.cursor().execute("SELECT id,IsAlive FROM Members WHERE ServerID=?",
                                 [serverId])


def CheckMember(serverId, memId):
    return conn.cursor().execute("SELECT count(id) FROM Members WHERE ServerID =? and id=?",
                                 [serverId, memId]).fetchone()[0] >= 1


def SetAlive(memId, serverId):
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET IsAlive=1 WHERE id=? and ServerID=?",
                   [memId, serverId])
    conn.commit()


def SetDead(memId, serverId):
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET IsAlive=0 WHERE id=? and ServerID=?",
                   [memId, serverId])
    conn.commit()


def GetInfoChan(serverId):
    return conn.cursor().execute("SELECT infoChan FROM Servers WHERE id=?",
                                 [serverId]).fetchone()[0]


def GetBanText(serverId):
    return conn.cursor().execute("SELECT BanText FROM Servers WHERE id=?",
                                 [serverId]).fetchone()[0]


# Profile
def GetMemInfo(memId, serverId):
    return conn.cursor().execute("SELECT level,Xp,MaxXP,Mentions,TotalXp FROM Members WHERE id=? and ServerID=?",
                                 [memId, serverId]).fetchone()


def GetRank(memId, serverId):
    i1 = 0
    for i in conn.cursor().execute(
            "SELECT id FROM Members Where IsAlive='1' and ServerID={} ORDER BY TotalXP DESC".format(
                serverId)).fetchall():
        i1 += 1
        if i[0] == memId:
            return i1


def SetInfoProfile(memId, serverId, text):
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET Info=? WHERE id=? and ServerID=?",
                   [text, memId, serverId])
    conn.commit()


def GetInfoProfile(memId, serverId):
    return conn.cursor().execute("SELECT info FROM Members WHERE id=? and ServerID=?",
                                 [memId, serverId]).fetchone()[0]


def GetTopMembers(page, ServerID):
    users = 5 * page
    return conn.cursor().execute(
        "SELECT id,TotalXP FROM Members Where IsAlive='1' and ServerID=? ORDER BY TotalXP DESC LIMIT ?,?",
        [ServerID, 0 + users, 5 + users])


def GetTopMenMembers(page, ServerID):
    users = 5 * page
    return conn.cursor().execute(
        "SELECT id,Mentions FROM Members Where IsAlive='1' and ServerID=? ORDER BY Mentions DESC LIMIT ?,?",
        [ServerID, 0 + users, 5 + users])


def GetActiveMembers():
    return conn.cursor() \
        .execute("SELECT id,Xp,MaxXP,Level,Mentions,TotalXP,ServerID FROM Members WHERE IsAlive=1")


def GetTopEmoji(page, serverID):
    emojies = 5 * page
    return conn.cursor().execute("SELECT EmojiID,Count FROM Emojies Where ServerID=? ORDER BY Count DESC LIMIT ?,?",
                                 [serverID, 0 + emojies, 5 + emojies])


def CheckEmoji(ServerID, EmojiID):
    return conn.cursor().execute(
        "SELECT count(EmojiID) FROM Emojies WHERE ServerID=? and EmojiID=?",
        [ServerID, EmojiID]).fetchone()[0] >= 1


def AddEmoji(ServerID, EmojiID):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Emojies (EmojiID,ServerID,LastUsage) VALUES (?,?,?)",
                   [EmojiID, ServerID, int(str(datetime.datetime.now().timestamp()).split('.')[0])])
    conn.commit()


def DelEmoji(EmojiID):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Emojies WHERE EmojiID=?", [EmojiID])
    conn.commit()


def GetAllEmojie(ServerID):
    return conn.cursor().execute("SELECT * FROM Emojies Where ServerID=? ORDER BY Count DESC", [ServerID])


def IncEmoji(ServerID, EmojiID):
    if CheckEmoji(ServerID, EmojiID):
        cursor = conn.cursor()
        time = int(str(datetime.datetime.now().timestamp()).split('.')[0])
        count = cursor.execute(
            "SELECT Count FROM Emojies WHERE ServerID =? and EmojiID=?",
            [ServerID, EmojiID]).fetchone()[0]
        count += 1
        cursor.execute(
            "UPDATE Emojies SET Count=?,LastUsage=? WHERE ServerID =? and EmojiID=?",
            [count, time, ServerID, EmojiID])
        conn.commit()
    else:
        AddEmoji(ServerID, EmojiID)
        IncEmoji(ServerID, EmojiID)


def IncMention(memberId, serverId, count):
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET Mentions=? WHERE id=? and ServerID=?",
                   [count, memberId, serverId])
    conn.commit()


def updateXp(userData, memberId, serverId):
    cursor = conn.cursor()
    cursor.execute("UPDATE Members SET Xp=?,MaxXP=?,Level=?,TotalXp=? WHERE id=? and ServerID=?",
                   [round(userData['xp'], 2),
                    round(userData['maxxp'], 2),
                    userData['level'],
                    userData['TotalXP'],
                    memberId,
                    serverId])
    conn.commit()


def AddIgnorList(channelID, serverId):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO IgnorList (ChannelID,ServerID,TimeStamp) VALUES (?,?,?);",
                   [channelID, serverId, datetime.datetime.now().timestamp()])
    conn.commit()


def DelIgnorList(channelID, serverId):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM IgnorList WHERE ChannelID = ? and ServerID=?;",
                   [channelID, serverId])
    conn.commit()


def GetIgnorList(serverId):
    return conn.cursor().execute("SELECT channelID,TimeStamp FROM IgnorList WHERE ServerID=?", [serverId])


def checkChannel(serverid, channelid):
    return conn.cursor().execute("SELECT count(channelid) FROM IgnorList WHERE ServerID =? and ChannelID=?",
                                 [serverid, channelid]).fetchone()[0] >= 1


def GetJoinRole(ServerID):
    return conn.cursor().execute("SELECT JoinRole FROM Servers WHERE id=?",
                                 [ServerID]).fetchone()[0]


def GetRoles(serverid, memberId):
    return conn.cursor().execute("SELECT RoleId FROM RoleList WHERE UserId=? and ServerId=?",
                                 [memberId, serverid])


def AddRoles(serverId, memberId, RoleId):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO RoleList (RoleId,ServerId,UserId) VALUES (?,?,?);",
                   [RoleId, serverId, memberId])
    conn.commit()


def DelRole(RoleId):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM RoleList WHERE RoleId=?", [RoleId])
    conn.commit()


def CheckRole(serverId, memberId, RoleId):
    return conn.cursor().execute(
        "SELECT count(RoleId) FROM RoleList WHERE RoleId=? and ServerID=? and UserId=?",
        [RoleId, serverId, memberId]).fetchone()[0] >= 1
