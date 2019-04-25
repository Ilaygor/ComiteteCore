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

def CreateLostMessage(memberAvatar,name,role):
    Avatar = Image.open(GetAvatarFromUrl(memberAvatar))
    ImageDraw.Draw(Avatar,'RGBA').rectangle([(0,0),(128,128)],fill=(255,0,0,70))
    base = Image.open('Maid/src/Images/LabmemberLost.png')
    base.paste(Avatar,(12,11))
    AddText(name,(160, 65),base)
    AddText(role,(160, 110),base,size=18)
    return base



def AddText(text,position,img,color=(255,255,255),size=22):
    from PIL import ImageFont
    Font = ImageFont.truetype("Maid/src/Fonts/ariblk.ttf", size)
    ImageDraw.Draw(img).text(position,text,color,font=Font)

def GetAvatarFromUrl(url):
    from io import BytesIO
    from requests import get
    return BytesIO(get(url).content)