from PIL import Image
import requests 
from io import BytesIO
import os

def AddMember(member):
    os.mkdir("Aquarius/src/Images/Users/"+member.name)
    CreateFirstWelcomeMessage(member.avatar_url).save("Aquarius/src/Images/Users/"+member.name+"/first"+".png", format="png")
    return "Aquarius/src/Images/Users/"+member.name+"/first"+".png"


def CreateFirstWelcomeMessage(memberAvatar):
    Avatar = Image.open(BytesIO(requests.get(memberAvatar).content))
    .thumbnail((125,125))
    base = Image.open('Aquarius/src/Images/NewLabmember.png')
    dir(base)
    base.paste(Avatar,(12,11))
    return base
