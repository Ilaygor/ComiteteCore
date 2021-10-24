import SQLWorker


def createServerFolder(guild):
    try:
        import os
        os.mkdir("src/Images/Usr/" + str(guild.id))
    except FileExistsError:
        pass


def addMembersOnServer(guild):
    for member in guild.members:
        if not member.bot:
            SQLWorker.AddNewMem(guild.id, member.id)


def checkMembersOnServer(guild):
    memberList = {}
    for member in SQLWorker.GetMembers(guild.id):
        memberList.update({member[0]: member[1]})
    for member in guild.members:
        if memberList.get(member.id):
            if memberList[member.id] == 1:
                memberList.pop(member.id)
            else:
                SQLWorker.SetAlive(member.id, guild.id)
        else:
            SQLWorker.AddNewMem(guild.id, member.id)
    for member in memberList.keys():
        if memberList[member] == 1:
            SQLWorker.SetDead(member, guild.id)


def addEmojies(guild):
    for emoji in guild.emojis:
        if not SQLWorker.CheckEmoji(guild.id, emoji.id):
            SQLWorker.AddEmoji(guild.id, emoji.id)

def addRoles(guild):
    for mem in guild.members:
        for role in mem.roles:
            if not SQLWorker.CheckRole(guild.id, mem.id, role.id) and not role.is_default():
                SQLWorker.AddRoles(guild.id, mem.id, role.id)