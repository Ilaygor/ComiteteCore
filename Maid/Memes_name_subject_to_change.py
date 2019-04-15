from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
import textwrap
import json
import os
import random
from Okari import AddText

def CreateMem(memname,text):
    memdata=json.loads(open('Maid/src/Images/memes/{}.json'.format(memname)).read())
    base = Image.open('Maid/src/Images/memes/'+memdata['filename'])
    linecount=0
    for line in textwrap.wrap(text,width=memdata['placewidth']):
        AddText(line,(memdata['x'], memdata['y']+linecount*memdata['font-size']),base,size=memdata['font-size'],color=ImageColor.getrgb(memdata['textcolor']))
        linecount+=1
    path="Maid/src/Images/Temp/"+memname+'_'+str(random.randint(0,100))+".png"
    base.save(path, format="png")
    return path