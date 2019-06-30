from PIL import Image
from PIL import ImageDraw
import os
from . import SQLWorker

def CreateProfile(member):
    Info=SQLWorker.GetMemInfo(member.id)

    path= "Temp/"+str(member.id)+".png"
    
    base=Image.open('src/Images/Profile.png')

    if os.path.exists("src/Images/Usr/"+str(member.id)+"/profile.png"):
        bg=Image.open("src/Images/Usr/"+str(member.id)+"/profile.png")
        bg.paste(base,(0,0),base)
        base=bg
        del bg

    Avatar = Image.open(GetAvatarFromUrl(member.avatar_url_as(size=128)))
    base.paste(Avatar,(24,94))
    del Avatar
    AddText(member.name,(172, 114),base,size=20)

    AddText(str(Info[0]).rjust(3,'0'),(430,192),base,color=(255,90,0),size=24,font="BONX-TubeBold.otf")

    if (Info[1]!=0):
        zero=2.16
        Re= Info[1]/(Info[2]/100)
        ImageDraw.Draw(base,'RGBA').rectangle([(174,191),(174+Re*zero,214)],fill=(255,90,0,255))

    AddText(str(Info[3]).rjust(4,'0'),(52,233),base,color=(255,90,0),size=24,font="BONX-TubeBold.otf")

    AddText(member.top_role.name,(180,145),base,color=member.top_role.colour.to_rgb(),size=18)

    #AddText(str(Info[5]),(180,250),base,color=(255,255,255),size=18)

    base.save(path)

    return path

def GetTop(members,page):
    base=Image.open('src/Images/Top.png')

    for i in range(len(members)):
        height=83*i
        Avatar = Image.open(GetAvatarFromUrl(members[i]['mem'].avatar_url_as(size=64)))
        Avatar.thumbnail((64,64))
        base.paste(Avatar,(80,9+height))
        del Avatar

        AddText(members[i]['mem'].name,(160, 15+height),base)
        AddText(members[i]['data'],(160, 40+height),base,size=18)
        num=5*page+i+1
        position=(str(num)).rjust(3,'0')
        AddText(position,(6,29+height),base,color=(255,90,0),size=30,font="BONX-TubeBold.otf")

    path="Temp/top"+str(page)+".png"
    base.save(path)
    return path



def AddText(text,position,img,color=(255,255,255),size=22,font='ariblk.ttf'):
    from PIL import ImageFont
    Font = ImageFont.truetype("src/Fonts/"+font, size)
    ImageDraw.Draw(img).text(position,text,color,font=Font)

def GetAvatarFromUrl(url):
    from io import BytesIO
    from requests import get
    return BytesIO(get(url).content)

def SetBG(id,url):
    bg=Image.open(GetAvatarFromUrl(url))
    if not os.path.exists("src/Images/Usr/"+str(id)):
        os.mkdir("src/Images/Usr/"+str(id))

    if bg.width > bg.height:
        bg = bg.resize((round(bg.width*(400/bg.height)), 400))
        bg = bg.crop(box=(round(bg.width/2)-265,0,round(bg.width/2)+265,400))
    elif bg.width < bg.height:
        bg = bg.resize((530, round(bg.height*(530/bg.width))))
        bg = bg.crop(box=(0,0,530,400))
    else:
        bg.thumbnail((530,530))
        bg = bg.crop(box=(0,round(bg.width/2)+200,530,round(bg.width/2)-200))
    bg.save("src/Images/Usr/"+str(id)+"/profile.png")