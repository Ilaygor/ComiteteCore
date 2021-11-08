import sqlite3

from discord import File
import os
import PictureCreator
import SQLWorker

conn = sqlite3.connect("BotDB.db")

UsersData = {}


def init():
    for i in SQLWorker.GetActiveMembers():
        UsersData[i[6], i[0]] = {
            'level': i[3],
            'xp': i[1],
            'maxxp': i[2],
            'mentions': i[4],
            'TotalXP': i[5]
        }
    return 'done'


def AddMem(memberId, serverId):
    usr = SQLWorker.GetMemInfo(memberId, serverId)

    UsersData[serverId, memberId] = {
            'level': usr[0],
            'xp': usr[1],
            'maxxp': usr[2],
            'mentions': usr[3],
            'TotalXP': usr[4]
    }


def DelMem(memberId, ServerID):
    UsersData.pop((ServerID, memberId))


def AddMention(memberId, serverId):
    UsersData[serverId, memberId]['mentions'] += 1
    SQLWorker.IncMention(memberId, serverId, UsersData[serverId, memberId]['mentions'])


async def levelUp(channel, memberId, level):
    mem = channel.guild.get_member(memberId)
    path = "Temp/{}.png".format(memberId)
    PictureCreator.CreateLevelUpMessage(mem.avatar_url_as(size=128),
                                        mem.name,
                                        str(level)).save(path, format="png")
    file = File(path, filename="LevelUp.png")
    await channel.send(file=file)
    os.remove(path)


async def checkXp(user, memberId, serverId, channel):
    if user['maxxp'] >= user['xp']:
        SQLWorker.updateXp(user, memberId, serverId)
    else:
        user['xp'] -= user['maxxp']
        user['maxxp'] *= 1.5
        user['level'] += 1
        await levelUp(channel, memberId, user['level'])
        await checkXp(user, memberId, serverId, channel)


async def AddExp(memberId, ServerID, count, channel):
    try:
        user = UsersData[ServerID, memberId]
    except KeyError:
        return
    user['xp'] += round(float(count), 2)
    user['TotalXP'] += round(float(count), 2)
    await checkXp(user, memberId, ServerID, channel)

