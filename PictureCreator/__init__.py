from PIL import Image
from PIL import ImageDraw
import os
from . import utils


def CreatWelcomeMessage(memberAvatar, name, memname):
    memname += " Return"
    Avatar = Image.open(utils.GetAvatarFromUrl(memberAvatar))
    Avatar.thumbnail((128, 128))
    base = Image.open('src/Images/Labmember.png')
    base.paste(Avatar, (12, 11))
    utils.AddText(name, (160, 80), base)
    fontsize = utils.AutoFontSize(memname, 338)
    utils.AddText(memname,
                  (152 + utils.CenterText(memname, 338, fontsize), 11 + utils.MiddleText(55, fontsize)),
                  base,
                  color=(240, 116, 33),
                  size=fontsize,
                  font='BONX-TubeBold.otf')
    return base


def CreateFirstWelcomeMessage(memberAvatar, name, memname):
    memname = "New " + memname
    Avatar = Image.open(utils.GetAvatarFromUrl(memberAvatar))
    Avatar.thumbnail((128, 128))
    base = Image.open('src/Images/Labmember.png')
    base.paste(Avatar, (12, 11))
    utils.AddText(name, (160, 80), base)
    fontsize = utils.AutoFontSize(memname, 338)
    utils.AddText(memname,
                  (152 + utils.CenterText(memname, 338, fontsize), 11 + utils.MiddleText(55, fontsize)),
                  base,
                  color=(240, 116, 33),
                  size=fontsize,
                  font='BONX-TubeBold.otf')
    return base


def CreateLostMessage(memberAvatar, name, role, memname):
    memname += " Lost!"
    Avatar = Image.open(utils.GetAvatarFromUrl(memberAvatar)).convert('RGB')
    Avatar.thumbnail((128, 128))
    ImageDraw.Draw(Avatar, 'RGBA').rectangle([0, 0, 128, 128],
                                             fill=(255, 0, 0, 70))
    base = Image.open('src/Images/LabmemberLost.png')
    base.paste(Avatar, (12, 11))
    utils.AddText(name, (160, 65), base)
    if role:
        utils.AddText(role.name, (160, 110), base,
                  size=18, color=role.colour.to_rgb())
    fontsize = utils.AutoFontSize(memname, 338)
    utils.AddText(memname, (152 + utils.CenterText(memname, 338, fontsize), utils.MiddleText(55, fontsize)),
                  base,
                  color=(240, 116, 33),
                  size=fontsize,
                  font='BONX-TubeBold.otf')
    return base


def CreateProfile(member):
    base = Image.open('src/Images/Profile.png')

    import SQLWorker
    info = SQLWorker.GetMemInfo(member.id, member.guild.id)

    if os.path.exists("src/Images/Usr/" + str(member.guild.id) + "/" + str(member.id) + "/profile.png"):
        bg = Image.open("src/Images/Usr/" + str(member.guild.id) + "/" + str(member.id) + "/profile.png")
        bg.paste(base, (0, 0), base)
        base = bg
        del bg

    Avatar = Image.open(utils.GetAvatarFromUrl(member.avatar_url_as(size=128)))
    base.paste(Avatar, (24, 94))
    del Avatar

    nik = member.name
    if member.nick:
        nik += " AKA " + member.nick
    fontsize = 22
    lines = utils.WrapText(nik, 340 * 1.5, fontsize)
    while fontsize > 12:
        if len(lines) > 1:
            fontsize -= 2
            lines = utils.WrapText(nik, 340 * 1.5, fontsize)
        else:
            break
    utils.AddText(nik, (172, 97), base, size=fontsize)

    utils.AddText(str(info[0]).rjust(3, '0') + "LV", (327, 161), base, color=(255, 90, 0), size=18,
                  font="BONX-TubeBold.otf")

    if info[1] != 0:
        zero = 2.16
        Re = info[1] / (info[2] / 100)
        ImageDraw.Draw(base, 'RGBA').rectangle([(174, 191), (174 + Re * zero, 214)], fill=(255, 90, 0, 255))

    utils.AddText(str(info[3]).rjust(4, '0'), (28, 265), base, color=(255, 90, 0), size=24, font="BONX-TubeBold.otf")

    utils.AddText(member.top_role.name, (180, 125), base, color=member.colour.to_rgb(), size=18)

    utils.AddText("XP:" + utils.ConvrterToCI(round(info[4], 2)).rjust(7, '0'), (173, 161), base, color=(255, 90, 0),
                  size=18,
                  font="BONX-TubeBold.otf")

    utils.AddText(str(SQLWorker.GetRank(member.id, member.guild.id)).rjust(4, '0'), (431, 190), base,
                  color=(255, 90, 0),
                  size=24, font="BONX-TubeBold.otf")

    text = SQLWorker.GetInfoProfile(member.id, member.guild.id)

    fontsize = 22
    height = 138
    width = 500
    lines = utils.WrapText(text, width, fontsize)
    while fontsize > 10:
        if fontsize * len(lines) > height:
            fontsize -= 2
            lines = utils.WrapText(text, width, fontsize)
        else:
            break

    offset = 0
    for i in lines:
        if (offset + 1) * fontsize < height:
            utils.AddText(i, (175, 240 + offset * fontsize), base, color=(255, 255, 255), size=fontsize,
                          font='ariblk.ttf')
            offset += 1
        else:
            break

    return base


def SetBG(serverid, id, url):
    bg = Image.open(utils.GetAvatarFromUrl(url))
    if not os.path.exists("src/Images/Usr/" + str(serverid) + "/" + str(id)):
        os.mkdir("src/Images/Usr/" + str(serverid) + "/" + str(id))

    if bg.width > bg.height:
        bg = bg.resize((round(bg.width * (400 / bg.height)), 400))
        bg = bg.crop(box=(round(bg.width / 2) - 265, 0, round(bg.width / 2) + 265, 400))
    elif bg.width < bg.height:
        bg = bg.resize((530, round(bg.height * (530 / bg.width))))
        bg = bg.crop(box=(0, 0, 530, 400))
    else:
        bg.thumbnail((530, 530))
        bg = bg.crop(box=(0, round(bg.width / 2) + 200, 530, round(bg.width / 2) - 200))

    bg.save("src/Images/Usr/" + str(serverid) + "/" + str(id) + "/profile.png")


def CreateRank(member):
    import SQLWorker

    Info = SQLWorker.GetMemInfo(member.id, member.guild.id)

    base = Image.open('src/Images/Rank.png')

    if os.path.exists("src/Images/Usr/{}/{}/profile.png".format(member.guild.id, member.id)):
        bg = Image.open("src/Images/Usr/{}/{}/profile.png".format(member.guild.id, member.id))\
            .crop(box=(0, 70, 530, 70 + 188))
        bg.paste(base,
                 (0, 0),
                 base)
        base = bg
        del bg

    Avatar = Image.open(
        utils.GetAvatarFromUrl(
            member.avatar_url_as(size=128)))
    base.paste(Avatar,
               (24, 34))
    del Avatar

    nik = member.name
    if member.nick:
        nik += " AKA {}".format(member.nick)
    fontsize = 22
    lines = utils.WrapText(nik,
                           340 * 1.5,
                           fontsize)
    while fontsize > 12:
        if len(lines) > 1:
            fontsize -= 2
            lines = utils.WrapText(nik,
                                   340 * 1.5,
                                   fontsize)
        else:
            break
    utils.AddText(lines[0],
                  (172, 37),
                  base,
                  size=fontsize)

    utils.AddText(str(Info[0]).rjust(3, '0') + "LV",
                  (327, 97),
                  base,
                  color=(255, 90, 0),
                  size=18,
                  font="BONX-TubeBold.otf")
    utils.AddText(member.top_role.name,
                  (180, 62), base,
                  color=member.colour.to_rgb(),
                  size=18)
    utils.AddText("XP:" + utils.ConvrterToCI(round(Info[4], 2)).rjust(7, '0'),
                  (173, 97),
                  base,
                  color=(255, 90, 0),
                  size=18,
                  font="BONX-TubeBold.otf")
    if Info[1] != 0:
        zero = 2.16
        Re = Info[1] / (Info[2] / 100)
        ImageDraw.Draw(base, 'RGBA').rectangle(
            [(174, 125), (174 + Re * zero, 154)],
            fill=(255, 90, 0, 255))

    utils.AddText(str(SQLWorker.GetRank(member.id, member.guild.id)).rjust(4, '0'),
                  (431, 129),
                  base,
                  color=(255, 90, 0),
                  size=24,
                  font="BONX-TubeBold.otf")
    return base


def GetTop(members, page):
    base = Image.open('src/Images/Top.png')

    for i in range(len(members)):
        height = 83 * i
        Avatar = Image.open(utils.GetAvatarFromUrl(members[i]['url']))
        Avatar = Avatar.resize((64, 64))
        base.paste(Avatar, (80, 9 + height))
        del Avatar

        nik = members[i]['mem'].name
        try:
            if members[i]['mem'].nick:
                nik += " AKA " + members[i]['mem'].nick
        except:
            pass
        fontsize = 20
        lines = utils.WrapText(nik, 340 * 1.5, fontsize)
        while fontsize > 12:
            if len(lines) > 1:
                fontsize -= 2
                lines = utils.WrapText(nik, 340 * 1.5, fontsize)
            else:
                break
        utils.AddText(nik,
                      (160, 15 + height),
                      base,
                      size=fontsize)
        utils.AddText(members[i]['data'],
                      (160, 40 + height),
                      base,
                      size=18)
        num = 5 * page + i + 1
        position = (str(num)).rjust(3, '0')
        utils.AddText(position,
                      (6, 29 + height),
                      base,
                      color=(255, 90, 0),
                      size=30,
                      font="BONX-TubeBold.otf")

    return base


def CreateLevelUpMessage(memberAvatar, name, level: str):
    Avatar = Image.open(utils.GetAvatarFromUrl(memberAvatar))
    Avatar.thumbnail((128, 128))
    base = Image.open('src/Images/LabmemberLevelUP.png')
    # ImageDraw.Draw(Avatar,'RGBA').rectangle([(0,0),(128,128)],fill=(0,255,0,70))
    base.paste(Avatar, (12, 11))
    utils.AddText(name, (160, 85), base)
    utils.AddText(level.rjust(3, '0'),
                  (415, 30),
                  base,
                  color=(255, 90, 0),
                  size=30,
                  font="BONX-TubeBold.otf")
    return base
