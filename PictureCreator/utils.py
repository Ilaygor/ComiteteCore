def GetAvatarFromUrl(url):
    from io import BytesIO
    from requests import get
    return BytesIO(get(url).content)


def AddText(text, position, img, color=(255, 255, 255), size=22, font='ariblk.ttf'):
    from PIL import ImageFont, ImageDraw
    Font = ImageFont.truetype("src/Fonts/" + font, size)
    ImageDraw.Draw(img).text(position,
                             text,
                             color,
                             font=Font)


def AutoFontSize(text, width, fontsize=34):
    lentext = len(text)
    while fontsize > 6:
        if lentext * fontsize >= width * 1.3:
            fontsize -= 1
        else:
            break
    return fontsize


def CenterText(text, width, fontsize):
    lentext = len(text)
    return round((width * 1.3) / 2 - (lentext * fontsize) / 2)


def MiddleText(height, fontsize):
    return round(height / 2 - fontsize / 2)


def WrapText(text, width, fontsize):
    outputList = []
    import math
    CharLength = math.floor(width / fontsize)

    Line = ""
    LineLenght = CharLength
    for i in text.split(" "):
        if len(i) < LineLenght:
            Line += i + " "
            LineLenght -= (len(i) + 1)
        elif len(i) == LineLenght:
            Line += i
            outputList.append(Line)
            Line = ""
            LineLenght = CharLength
        elif len(i) > LineLenght:
            outputList.append(Line)
            LineLenght = CharLength - len(i) - 1
            Line = i + " "
    outputList.append(Line)
    return outputList


def ConvrterToCI(num: int):
    lennum = len(str(round(num)))
    if lennum > 6:
        return str(round(num / pow(10, 6), 2)) + "M"
    if lennum > 3:
        return str(round(num / pow(10, 3), 2)) + "K"
    return str(num)
