from Cogs.Profile import XpSys
from models.Emojies import Emojie
from models.Members import Member
from models.RoleLists import RoleList
from models.database import Session
import SQLWorker
session = Session()


def createServerFolder(guild):
    try:
        import os
        os.mkdir("src/Images/Usr/" + str(guild.id))
    except FileExistsError:
        pass


def addMembersOnServer(guild):
    for member in guild.members:
        if not member.bot:
            member = Member(serverId=guild.id, memberId=member.MemberId)
            session.add(member)
            session.commit()
            XpSys.AddMem(member.id, guild.id)


def checkMembersOnServer(guild):
    memberList = {}
    # Смотрим что в бд и записываем в словарь
    for memberSql in session.query(Member).filter(Member.ServerId == guild.id):
        memberList.update({memberSql.MemberId: memberSql.IsAlive})
    # Сопоставляем наших пользователей из бд с данными Discord
    for discordMember in guild.members:
        # Если пользователь есть в нашей бд
        if discordMember.id in memberList.keys():
            # Если пользователь значится как "не активный", то делаем его активным
            if not memberList[discordMember.id]:
                SQLWorker.SetAlive(serverId=guild.id, memberId=discordMember.id)
            # Чистим пользователя из списка
            memberList.pop(discordMember.id)
        # Если пользователя нет, то заносим в бд
        else:
            SQLWorker.AddNewMem(serverId=guild.id, memberId=discordMember.id)
            memberList.pop(discordMember.id)


    # Оставшиеся пользователи означает, что они уже покинули Сервер
    for member in memberList.keys():
        if memberList[member]:
            SQLWorker.SetDead(serverId=guild.id, memberId=member)

def addEmojies(guild):
    for emoji in guild.emojis:
        emojieSql = session.query(Emojie).filter(Emojie.ServerId == guild.id, Emojie.Id == emoji.id).first()
        if not emojieSql:
            newEmojie = Emojie(serverId=guild.id, id=emoji.id)
            session.add(newEmojie)
            session.commit()


def addRoles(guild):
    for mem in guild.members:
        for role in mem.roles:
            if role.is_default():
                continue

            roleList = session.query(RoleList).filter(RoleList.RoleId == role.id, RoleList.MemberId == mem.id).first()
            if not roleList:
                newRole = RoleList(roleId=role.id, memberId=mem.id)
                session.add(newRole)
                session.commit()
