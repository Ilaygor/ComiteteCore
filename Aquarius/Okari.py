from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests

from io import BytesIO
import os

def AddMember(member):
    if not os.path.exists("Aquarius/src/Images/Users/"+str(member.id)) :
        os.mkdir("Aquarius/src/Images/Users/"+str(member.id))
        CreateFirstWelcomeMessage(member.avatar_url,member.name).save("Aquarius/src/Images/Users/"+str(member.id)+"/first.png", format="png")
    return "Aquarius/src/Images/Users/"+str(member.id)+"/first.png"


def CreateFirstWelcomeMessage(memberAvatar,name):
    Avatar = Image.open(BytesIO(requests.get(memberAvatar).content)).resize((125,125))
    base = Image.open('Aquarius/src/Images/NewLabmember.png')
    base.paste(Avatar,(12,11))
    Font = ImageFont.truetype("Aquarius/src/Images/ariblk.ttf", 22)
    ImageDraw.Draw(base).text((160, 80),name,(255,255,255),font=Font)
    return base
