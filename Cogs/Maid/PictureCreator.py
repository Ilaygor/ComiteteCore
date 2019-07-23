from PIL import Image
from PIL import ImageDraw
import os
from . import SQLWorker

def CreateRank(member):
    Info=SQLWorker.GetMemInfo(member.id)
    
    path= "Temp/"+str(member.id)+".png"
    
    base=Image.open('src/Images/Rank.png')

    if os.path.exists("src/Images/Usr/"+str(member.id)+"/profile.png"):
        bg=Image.open("src/Images/Usr/"+str(member.id)+"/profile.png").crop(box=(0,70,530,70+188))
        bg.paste(base,(0,0),base)
        base=bg
        del bg
    
    Avatar = Image.open(GetAvatarFromUrl(member.avatar_url_as(size=128)))
    base.paste(Avatar,(24,34))
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
    AddText(lines[0],(172, 37),base,size=fontsize)

    AddText(str(Info[0]).rjust(3,'0')+"LV",(327,97),base,color=(255,90,0),size=18,font="BONX-TubeBold.otf")
    AddText(member.top_role.name,(180,62),base,color=member.colour.to_rgb(),size=18)
    AddText("XP:"+ConvrterToCI(round(Info[4],2)).rjust(7,'0'),(173,97),base,color=(255,90,0),size=18,font="BONX-TubeBold.otf")
    if (Info[1]!=0):
        zero=2.16
        Re= Info[1]/(Info[2]/100)
        ImageDraw.Draw(base,'RGBA').rectangle([(174,125),(174+Re*zero,154)],fill=(255,90,0,255))
            
    AddText(str(SQLWorker.GetRank(member.id)).rjust(4,'0'),(431,129),base,color=(255,90,0),size=24,font="BONX-TubeBold.otf")
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

def GetTop(members,page):
    base=Image.open('src/Images/Top.png')

    for i in range(len(members)):
        height=83*i
        Avatar = Image.open(GetAvatarFromUrl(members[i]['url']))
        Avatar=Avatar.resize((64,64))
        base.paste(Avatar,(80,9+height))
        del Avatar

        nik=members[i]['mem'].name
        try:
            if members[i]['mem'].nick:
                nik+=" AKA "+members[i]['mem'].nick
        except:
            pass
        fontsize=20
        lines=WrapText(nik,340*1.5,fontsize)
        while fontsize>12:
            if len(lines) > 1:
                fontsize-=2
                lines=WrapText(nik,340*1.5,fontsize)
            else:
                break
        AddText(nik,(160, 15+height),base,size=fontsize)
        
        AddText(members[i]['data'],(160, 40+height),base,size=18)
        num=5*page+i+1
        position=(str(num)).rjust(3,'0')
        AddText(position,(6,29+height),base,color=(255,90,0),size=30,font="BONX-TubeBold.otf")

    path="Temp/top"+str(page)+".png"
    base.save(path)
    return path

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