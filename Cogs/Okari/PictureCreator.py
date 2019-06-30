from PIL import Image
from PIL import ImageDraw
import os
from . import SQLWorker

def AddMember(member):
    serverid=member.guild.id
    if SQLWorker.CheckMember(serverid,member.id):
        SQLWorker.ReactivateMember(serverid,member.id)
        CreatWelcomeMessage(member.avatar_url_as(size=128),member.name).save("Temp/"+str(member.id)+".png", format="png")
    else:
        SQLWorker.AddNewmem(serverid,member.id)
        CreateFirstWelcomeMessage(member.avatar_url_as(size=128),member.name).save("Temp/"+str(member.id)+".png", format="png")
        
    return "Temp/"+str(member.id)+".png"

def LostMember(member):
    CreateLostMessage(member.avatar_url_as(size=128),member.name,member.top_role).save("Temp/"+str(member.id)+".png", format="png")
    SQLWorker.DeactivateMember(member.guild.id,member.id)
    return "Temp/"+str(member.id)+".png"


def CreatWelcomeMessage(memberAvatar,name):
    Avatar = Image.open(GetAvatarFromUrl(memberAvatar))
    Avatar.thumbnail((128,128))
    base = Image.open('src/Images/LabmemberReturn.png')
    base.paste(Avatar,(12,11))
    AddText(name,(160, 80),base)
    return base

def CreateFirstWelcomeMessage(memberAvatar,name):
    Avatar = Image.open(GetAvatarFromUrl(memberAvatar))
    Avatar.thumbnail((128,128))
    base = Image.open('src/Images/NewLabmember.png')
    base.paste(Avatar,(12,11))
    AddText(name,(160, 80),base)
    return base

def CreateLostMessage(memberAvatar,name,role):
    Avatar = Image.open(GetAvatarFromUrl(memberAvatar))
    Avatar.thumbnail((128,128))
    ImageDraw.Draw(Avatar,'RGBA').rectangle([(0,0),(128,128)],fill=(255,0,0,70))
    base = Image.open('src/Images/LabmemberLost.png')
    base.paste(Avatar,(12,11))
    AddText(name,(160, 65),base)
    AddText(role.name,(160, 110),base,size=18,color=role.colour.to_rgb())
    return base


def AddText(text,position,img,color=(255,255,255),size=22,font='ariblk.ttf'):
    from PIL import ImageFont
    Font = ImageFont.truetype("src/Fonts/"+font, size)
    ImageDraw.Draw(img).text(position,text,color,font=Font)

def GetAvatarFromUrl(url):
    from io import BytesIO
    from requests import get
    return BytesIO(get(url).content)