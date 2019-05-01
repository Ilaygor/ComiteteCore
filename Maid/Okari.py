from PIL import Image
from PIL import ImageDraw
import os
import Masta

def AddMember(member):
    if not Masta.CheckMember(member.id):
        Masta.AddNewLabmem(member.id)
        CreateFirstWelcomeMessage(member.avatar_url_as(size=128),member.name).save("Maid/src/Images/Temp/"+str(member.id)+".png", format="png")
    else:
        CreatWelcomeMessage(member.avatar_url_as(size=128),member.name).save("Maid/src/Images/Temp/"+str(member.id)+".png", format="png")
        Masta.ReactivateMember(member.id)
    return "Maid/src/Images/Temp/"+str(member.id)+".png"

def LostMember(member):
    CreateLostMessage(member.avatar_url_as(size=128),member.name,member.top_role.name).save("Maid/src/Images/Temp/"+str(member.id)+".png", format="png")
    Masta.DeactivateMember(member.id)
    return "Maid/src/Images/Temp/"+str(member.id)+".png"

def GetTop(members,page):

    base=Image.open('Maid/src/Images/Top.png')

    for i in range(10):
        height=83*i
        Avatar = Image.open(GetAvatarFromUrl(members[i]['mem'].avatar_url_as(size=64)))
        Avatar.thumbnail((64,64))
        base.paste(Avatar,(80,9+height))
        del Avatar

        AddText(members[i]['mem'].name,(160, 15+height),base)
        AddText(members[i]['data'],(160, 40+height),base,size=18)
        num=i+1
        if num==10:
            position=(str(page+1)+'0').rjust(3,'0')
        else:
            position=(str(page)+str(num)).rjust(3,'0')
        AddText(position,(6,29+height),base,color=(255,90,0),size=30,font="BONX-TubeBold.otf")

    
    path="Maid/src/Images/Temp/top"+str(page)+".png"
    base.save(path)
    return path
    

def CreatWelcomeMessage(memberAvatar,name):
    Avatar = Image.open(GetAvatarFromUrl(memberAvatar))
    base = Image.open('Maid/src/Images/LabmemberReturn.png')
    base.paste(Avatar,(12,11))
    AddText(name,(160, 80),base)
    return base

def CreateFirstWelcomeMessage(memberAvatar,name):
    Avatar = Image.open(GetAvatarFromUrl(memberAvatar))
    base = Image.open('Maid/src/Images/NewLabmember.png')
    base.paste(Avatar,(12,11))
    AddText(name,(160, 80),base)
    return base

def CreateLevelUpMessage(memberAvatar,name,level:str):
    Avatar = Image.open(GetAvatarFromUrl(memberAvatar))
    base = Image.open('Maid/src/Images/LabmemberLevelUP.png')
    #ImageDraw.Draw(Avatar,'RGBA').rectangle([(0,0),(128,128)],fill=(0,255,0,70))
    base.paste(Avatar,(12,11))
    AddText(name,(160, 85),base)
    AddText(level.rjust(3,'0'),(415,30),base,color=(255,90,0),size=30,font="BONX-TubeBold.otf")
    return base


def CreateLostMessage(memberAvatar,name,role):
    Avatar = Image.open(GetAvatarFromUrl(memberAvatar))
    ImageDraw.Draw(Avatar,'RGBA').rectangle([(0,0),(128,128)],fill=(255,0,0,70))
    base = Image.open('Maid/src/Images/LabmemberLost.png')
    base.paste(Avatar,(12,11))
    AddText(name,(160, 65),base)
    AddText(role,(160, 110),base,size=18)
    return base

def AddText(text,position,img,color=(255,255,255),size=22,font='ariblk.ttf'):
    from PIL import ImageFont
    Font = ImageFont.truetype("Maid/src/Fonts/"+font, size)
    ImageDraw.Draw(img).text(position,text,color,font=Font)

def GetAvatarFromUrl(url):
    from io import BytesIO
    from requests import get
    return BytesIO(get(url).content)