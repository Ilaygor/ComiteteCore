from PIL import Image
from PIL import ImageDraw
import os
from . import SQLWorker


def CreateProfile(member):
    Info=SQLWorker.GetMemInfo(member.id,member.guild.id)
    
    path= "Temp/"+str(member.id)+".png"
    
    base=Image.open('src/Images/Profile.png')

    if os.path.exists("src/Images/Usr/"+str(member.guild.id)+"/"+str(member.id)+"/profile.png"):
        bg=Image.open("src/Images/Usr/"+str(member.guild.id)+"/"+str(member.id)+"/profile.png")
        bg.paste(base,(0,0),base)
        base=bg
        del bg

    Avatar = Image.open(GetAvatarFromUrl(member.avatar_url_as(size=128)))
    base.paste(Avatar,(24,94))
    del Avatar

    nik=member.name
    if member.nick:
        nik+=" AKA "+member.nick
    fontsize=22
    lines=WrapText(nik,340*1.5,fontsize)
    while fontsize>12:
        if len(lines) > 1:
            fontsize-=2
            lines=WrapText(nik,340*1.5,fontsize)
        else:
            break
    AddText(nik,(172, 97),base,size=fontsize)

    AddText(str(Info[0]).rjust(3,'0')+"LV",(327,161),base,color=(255,90,0),size=18,font="BONX-TubeBold.otf")

    if (Info[1]!=0):
        zero=2.16
        Re= Info[1]/(Info[2]/100)
        ImageDraw.Draw(base,'RGBA').rectangle([(174,191),(174+Re*zero,214)],fill=(255,90,0,255))

    AddText(str(Info[3]).rjust(4,'0'),(28,265),base,color=(255,90,0),size=24,font="BONX-TubeBold.otf")

    
    AddText(member.top_role.name,(180,125),base,color=member.colour.to_rgb(),size=18)

    
    AddText("XP:"+ConvrterToCI(round(Info[4],2)).rjust(7,'0'),(173,161),base,color=(255,90,0),size=18,font="BONX-TubeBold.otf")
    
    AddText(str(SQLWorker.GetRank(member.id,member.guild.id)).rjust(4,'0'),(431,190),base,color=(255,90,0),size=24,font="BONX-TubeBold.otf")
    
    
    text=SQLWorker.GetInfo(member.id,member.guild.id)

    fontsize=22
    height=138
    width=500
    lines=WrapText(text,width,fontsize)
    while fontsize>10:
        if fontsize*len(lines) > height:
            fontsize-=2
            lines=WrapText(text,width,fontsize)
        else:
            break

    offset=0
    for i in lines:
        if (offset+1)*fontsize < height:
            AddText(i,(175,240+offset*fontsize),base,color=(255,255,255),size=fontsize,font='ariblk.ttf')
            offset+=1
        else:
            break

    base.save(path)
    
    return path

def WrapText(text,width,fontsize):
    outputList=[]
    import math
    CharLength=math.floor(width/fontsize)

    Line=""
    LineLenght=CharLength
    for i in text.split(" "):
        if len(i)<LineLenght:
            Line+=i+" "
            LineLenght-=(len(i)+1)
        elif len(i)==LineLenght:
            Line+=i
            outputList.append(Line)
            Line=""
            LineLenght=CharLength
        elif len(i)>LineLenght:
            outputList.append(Line)
            LineLenght=CharLength-len(i)-1
            Line=i+" "
    outputList.append(Line)
    return outputList

def SetBG(serverid,id,url):
    bg=Image.open(GetAvatarFromUrl(url))
    if not os.path.exists("src/Images/Usr/"+str(serverid)+"/"+str(id)):
        os.mkdir("src/Images/Usr/"+str(serverid)+"/"+str(id))

    if bg.width > bg.height:
        bg = bg.resize((round(bg.width*(400/bg.height)), 400))
        bg = bg.crop(box=(round(bg.width/2)-265,0,round(bg.width/2)+265,400))
    elif bg.width < bg.height:
        bg = bg.resize((530, round(bg.height*(530/bg.width))))
        bg = bg.crop(box=(0,0,530,400))
    else:
        bg.thumbnail((530,530))
        bg = bg.crop(box=(0,round(bg.width/2)+200,530,round(bg.width/2)-200))
    bg.save("src/Images/Usr/"+str(serverid)+"/"+str(id)+"/profile.png")

def ConvrterToCI(num:int):
    lennum=len(str(round(num)))
    if lennum > 6:
        return str(round(num/pow(10,6),2))+"M"
    if lennum > 3:
        return str(round(num/pow(10,3),2))+"K"
    return str(num)
    
def AddText(text,position,img,color=(255,255,255),size=22,font='ariblk.ttf'):
    from PIL import ImageFont
    Font = ImageFont.truetype("src/Fonts/"+font, size)
    ImageDraw.Draw(img).text(position,text,color,font=Font)

def GetAvatarFromUrl(url):
    from io import BytesIO
    from requests import get
    return BytesIO(get(url).content)