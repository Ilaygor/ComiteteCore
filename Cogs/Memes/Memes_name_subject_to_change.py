from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
import textwrap
import json
import os
import random

def CreateVisualMem(memname,url):
    try:
        base = Image.open(GetAvatarFromUrl(url))
    except OSError:
        return None

    memdata=json.loads(open('src/Images/memes/{}.json'.format(memname)).read())
    Addiction = Image.open('src/Images/memes/'+memdata['filename'])

    Addiction = Addiction.resize((round(base.width*memdata['percent'][0]),round(Addiction.height*(base.width*memdata['percent'][0]/Addiction.width))))

    if memdata.get('filter'):
        fillter=Image.new('RGBA',(base.width,base.height),color=(memdata['filter'][0],memdata['filter'][1],memdata['filter'][2],memdata['filter'][3]))
        base.paste(fillter,(0,0),fillter)
    
    if memdata['position']=="right": 
        base.paste(Addiction,(base.width-Addiction.width,base.height-Addiction.height),Addiction)
    elif memdata['position']=="left":
        base.paste(Addiction,(0,base.height-Addiction.height),Addiction)

    path="Temp/"+memname+'_'+str(random.randint(0,100))+".png"
    base.save(path, format="png")

    return path

def CreateMem(memname,text:str):
    memdata=json.loads(open('src/Images/memes/{}.json'.format(memname)).read())
    base = Image.open('src/Images/memes/'+memdata['filename'])
    linecount=0
    width=int(memdata['placewidth']/(memdata['font-size']*0.5))
    for line in textwrap.wrap(text,width=width):
        offset=linecount*memdata['font-size']
        if offset<memdata['placeheight']:
            AddText(('{:^'+str(width)+'}').format(line),(memdata['x'], memdata['y']+offset),base,size=memdata['font-size'],color=ImageColor.getrgb(memdata['textcolor']))
            linecount+=1
        else:
            break
    path="Temp/"+memname+'_'+str(random.randint(0,100))+".png"
    base.save(path, format="png")
    return path



def AddText(text,position,img,color=(255,255,255),size=22,font='ariblk.ttf'):
    from PIL import ImageFont
    Font = ImageFont.truetype("src/Fonts/"+font, size)
    ImageDraw.Draw(img).text(position,text,color,font=Font)

def GetAvatarFromUrl(url):
    from io import BytesIO
    from requests import get
    return BytesIO(get(url).content)