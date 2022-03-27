import os

from discord import File

import PictureCreator
from models.Members import Member
from models.database import Session

session = Session()

UsersData = {}


def init():
    for member in session.query(Member).filter(Member.IsAlive).all():
        UsersData[member.ServerId, member.MemberId] = member
    return 'done'


def AddMem(memberId, serverId):
    member = session.query(Member).filter(Member.MemberId == memberId, Member.ServerId == serverId)
    UsersData[serverId, memberId] = member


def DelMem(memberId, ServerID):
    UsersData.pop((ServerID, memberId))


def AddMention(memberId, serverId):
    member = UsersData[serverId, memberId]
    member.Mentions += 1
    session.commit()


async def AddExp(memberId, ServerID, count, channel):
    try:
        member = UsersData[ServerID, memberId]
    except KeyError:
        return
    member.Xp = member.Xp + round(float(count), 2)
    member.TotalXp += round(float(count), 2)
    session.commit()
    await checkXp(member, memberId, ServerID, channel)


async def checkXp(member, memberId, serverId, channel):
    if member.MaxXp >= member.Xp:
        session.commit()
    else:
        member.Xp -= member.MaxXp
        member.MaxXp *= 1.5
        member.Level += 1
        await levelUp(channel, memberId, member.Level)
        await checkXp(member, memberId, serverId, channel)


async def levelUp(channel, memberId, level):
    mem = channel.guild.get_member(memberId)
    path = "Temp/{}.png".format(memberId)
    PictureCreator.CreateLevelUpMessage(mem, str(level)).save(path, format="png")
    file = File(path, filename="LevelUp.png")
    await channel.send(file=file)
    os.remove(path)
