from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
import textwrap
import json
import os
import random
from Okari import AddText,GetAvatarFromUrl

def CreateVisualMem(memname,url):
    try:
        base = Image.open(GetAvatarFromUrl(url)).convert('RGBA')
    except OSError:
        return None

    memdata=json.loads(open('Maid/src/Images/memes/{}.json'.format(memname)).read())
    Addiction = Image.open('Maid/src/Images/memes/'+memdata['filename'])
    Addiction = Addiction.resize((base.width,round(Addiction.height*(base.width/Addiction.width))))
    base.paste(Addiction,(base.width-Addiction.width,base.height-Addiction.height),Addiction)
    
    path="Maid/src/Images/Temp/"+memname+'_'+str(random.randint(0,100))+".png"
    base.save(path, format="png")

    return path


def CreateMem(memname,text:str):
    memdata=json.loads(open('Maid/src/Images/memes/{}.json'.format(memname)).read())
    base = Image.open('Maid/src/Images/memes/'+memdata['filename'])
    linecount=0
    width=int(memdata['placewidth']/(memdata['font-size']*0.5))
    for line in textwrap.wrap(text,width=width):
        offset=linecount*memdata['font-size']
        if offset<memdata['placeheight']:
            AddText(('{:^'+str(width)+'}').format(line),(memdata['x'], memdata['y']+offset),base,size=memdata['font-size'],color=ImageColor.getrgb(memdata['textcolor']))
            linecount+=1
        else:
            break
    path="Maid/src/Images/Temp/"+memname+'_'+str(random.randint(0,100))+".png"
    base.save(path, format="png")
    return path