from PIL import Image
from PIL import ImageDraw
import os

def CreateLevelUpMessage(memberAvatar,name,level:str):
    Avatar = Image.open(GetAvatarFromUrl(memberAvatar))
    Avatar.thumbnail((128,128))
    base = Image.open('src/Images/LabmemberLevelUP.png')
    #ImageDraw.Draw(Avatar,'RGBA').rectangle([(0,0),(128,128)],fill=(0,255,0,70))
    base.paste(Avatar,(12,11))
    AddText(name,(160, 85),base)
    AddText(level.rjust(3,'0'),(415,30),base,color=(255,90,0),size=30,font="BONX-TubeBold.otf")
    return base



def AddText(text,position,img,color=(255,255,255),size=22,font='ariblk.ttf'):
    from PIL import ImageFont
    Font = ImageFont.truetype("src/Fonts/"+font, size)
    ImageDraw.Draw(img).text(position,text,color,font=Font)

def GetAvatarFromUrl(url):
    from io import BytesIO
    from requests import get
    return BytesIO(get(url).content)