from PIL import Image
from PIL import ImageDraw
import os
from . import SQLWorker

def AddMember(member):
    serverid=member.guild.id
    if SQLWorker.CheckMember(serverid,member.id):
        SQLWorker.ReactivateMember(serverid,member.id)
        CreatWelcomeMessage(member.avatar_url_as(size=128),member.name,SQLWorker.GetMemName(member.guild.id)).save("Temp/"+str(member.id)+".png", format="png")
    else:
        SQLWorker.AddNewmem(serverid,member.id)
        CreateFirstWelcomeMessage(member.avatar_url_as(size=128),member.name,SQLWorker.GetMemName(member.guild.id)).save("Temp/"+str(member.id)+".png", format="png")
        
    return "Temp/"+str(member.id)+".png"

def LostMember(member):
    CreateLostMessage(member.avatar_url_as(size=128),member.name,member.top_role,SQLWorker.GetMemName(member.guild.id)).save("Temp/"+str(member.id)+".png", format="png")
    SQLWorker.DeactivateMember(member.guild.id,member.id)
    return "Temp/"+str(member.id)+".png"


def CreatWelcomeMessage(memberAvatar,name,memname):
    memname+=" Return"
    Avatar = Image.open(GetAvatarFromUrl(memberAvatar))
    Avatar.thumbnail((128,128))
    base = Image.open('src/Images/Labmember.png')
    base.paste(Avatar,(12,11))
    AddText(name,(160, 80),base)
    fontsize=AutoFontSize(memname,338)
    AddText(memname,(152+CenterText(memname,338,fontsize), 11+MiddleText(55,fontsize)),base,color=(240,116,33),size=fontsize,font='BONX-TubeBold.otf')
    return base

def CreateFirstWelcomeMessage(memberAvatar,name,memname):
    memname="New "+memname
    Avatar = Image.open(GetAvatarFromUrl(memberAvatar))
    Avatar.thumbnail((128,128))
    base = Image.open('src/Images/Labmember.png')
    base.paste(Avatar,(12,11))
    AddText(name,(160, 80),base)
    fontsize=AutoFontSize(memname,338)
    AddText(memname,(152+CenterText(memname,338,fontsize), 11+MiddleText(55,fontsize)),base,color=(240,116,33),size=fontsize,font='BONX-TubeBold.otf')
    return base

def CreateLostMessage(memberAvatar,name,role,memname):
    memname+=" Lost!"
    Avatar = Image.open(GetAvatarFromUrl(memberAvatar))
    Avatar.thumbnail((128,128))
    ImageDraw.Draw(Avatar,'RGBA').rectangle([(0,0),(128,128)],fill=(255,0,0,70))
    base = Image.open('src/Images/LabmemberLost.png')
    base.paste(Avatar,(12,11))
    AddText(name,(160, 65),base)
    AddText(role.name,(160, 110),base,size=18,color=role.colour.to_rgb())
    fontsize=AutoFontSize(memname,338)
    AddText(memname,(152+CenterText(memname,338,fontsize), MiddleText(55,fontsize)),base,color=(240,116,33),size=fontsize,font='BONX-TubeBold.otf')
    return base


def AddText(text,position,img,color=(255,255,255),size=22,font='ariblk.ttf'):
    from PIL import ImageFont
    Font = ImageFont.truetype("src/Fonts/"+font, size)
    ImageDraw.Draw(img).text(position,text,color,font=Font)

def GetAvatarFromUrl(url):
    from io import BytesIO
    from requests import get
    return BytesIO(get(url).content)

def AutoFontSize(text,width,fontsize=34):
    lentext= len(text)
    while fontsize>6:
        if (lentext*fontsize>=width*1.3):
            fontsize-=1
        else:
            break
    return fontsize

def CenterText(text,width, fontsize):
    lentext= len(text)
    return round((width*1.3)/2-(lentext*fontsize)/2)

def MiddleText(height, fontsize):
    return round(height/2-fontsize/2)