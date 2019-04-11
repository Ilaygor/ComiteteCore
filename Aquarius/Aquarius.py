import discord
import datetime
import json
import random
import sqlite3

TOKEN = 'NTE1MDcwOTYwNTg0NDkxMDI5.D0Ti4Q.DrIbHCqAWa9bxqrBGYsjGG50oTE'

client = discord.Client()
conn=sqlite3.connect("/root/AquariusDB.db")
conn.row_factory = sqlite3.Row

def memjoined(mem):
	jd=getDate(mem).split(';')

	delta=(datetime.date.today()- datetime.date(int(jd[0]),int(jd[1]),int(jd[2]))).days
	day=delta%30
	day=day+1
	delta=delta//30
	month=delta%12
	year=delta//12
	if year == 0:
		year= ' '
	elif year==1:
		year= '1 год'
	elif year > 4:
		year= str(year) + ' лет'
	else:
		year= str(year) + ' года'

	if month==0:
		month= ' '
	elif  month>4:
		month= str(month) + ' месяцев и '
	elif month==1:
		month= str(month) + ' месяц и '
	else:
		month= str(month)+ ' месяца и '

	if  day>4:
		day= str(day) + ' дней'
	elif day==1:
		day= str(day) + ' день'
	elif day<1:
		day= ''
	else:
		day= str(day) + ' дня'
	
	return year+month+day


def GetCountWin(mem):
	cursor = conn.cursor()
	cursor.execute("SELECT countWins FROM Players WHERE discordID=?", [(mem)])
	return cursor.fetchone()[0]

def CheckAdmin(mem):
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM Admins WHERE discordID =?", [(mem)])
	if cursor.fetchone():
		return True
	else:
		return False

def CheckUser(mem):
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM Players WHERE discordID =?", [(mem)])
	if cursor.fetchone():
		return True
	else:
		return False

def getDate(mem):
	cursor = conn.cursor()
	cursor.execute("SELECT date FROM Players WHERE discordID=?", [(mem)])
	return cursor.fetchone()[0]



def IncWin(mem):
	cursor = conn.cursor()
	cursor.execute("UPDATE Players SET countWins =? WHERE discordID =?",[(GetCountWin(mem)+1),(mem)])
	conn.commit()

def DecWin(mem):
	cursor = conn.cursor()
	cursor.execute("UPDATE Players SET countWins =? WHERE discordID =?",[(GetCountWin(mem)-1),(mem)])
	conn.commit()

def SetInfo(mem):
	jd=memjoined(mem.id)
	emb= discord.Embed(title=mem.display_name,color=mem.color)
	emb.set_author(name="Aquarius System")
	emb.add_field(name="Id:", value=mem.id, inline=True)
	emb.add_field(name="Время на сервере:",value=jd, inline=False)
	emb.add_field(name="Количество побед:",value=GetCountWin(mem.id), inline=False)
	if (CheckAdmin(mem.id)):
		emb.add_field(name="Имеет привелегии учёта победителя",value="**", inline=False)
	emb.add_field(name="Наивысшая роль:", value=mem.top_role.name, inline=False)
	if mem.game:
		emb.add_field(name="Игра:",value=mem.game, inline=False)
	emb.set_image(url=mem.avatar_url)
	return emb

def SetHelp(mem):
	emb= discord.Embed(title="Справка",color=mem.color)
	emb.set_author(name="Aquarius System")
	emb.add_field(name="!help", value="Справка по всем командам", inline=False)
	emb.add_field(name="!info",value="Получение информации о себе", inline=False)
	emb.add_field(name="!info   @никнейм1 [@никнейм2 ... @никнеймN]",value="Получение информации о пользователях", inline=False)
	emb.add_field(name="!addWin @никнейм1 [@никнейм2 ... @никнеймN]",value="Добовление победы пользователям", inline=False)
	emb.add_field(name="!rmWin  @никнейм1 [@никнейм2 ... @никнеймN]",value="Удаление победы у пользователям", inline=False)
	emb.add_field(name="!top",value="Вывод топа победителей", inline=False)
	return emb


def SetTop(ser):
		
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM Players WHERE countWins>0 AND onServer='0' ORDER BY countWins DESC")
	
	TopList=cursor.fetchall()

	emb= discord.Embed(title="Топ игроков",color=ser.get_member(TopList[0][0]).color)
	emb.set_author(name="Aquarius System")

	for i in TopList:
		emb.add_field(name=ser.get_member(i[0]).display_name, value=i[1], inline=False)

	return emb


@client.event
async def on_message(message):
	
	if '!help' in message.content:
		await client.send_message(message.channel,embed=SetHelp(message.author))


	if '!top' in message.content:
		await client.send_message(message.channel,embed=SetTop(message.server))


	if '!info' in message.content:
		mems=message.mentions
		if mems:
			for mem in mems:
				await client.send_message(message.channel,embed=SetInfo(mem))
		else:
			await client.send_message(message.channel,embed=SetInfo(message.author))

	if '!addWin' in message.content and message.mentions:
		if (CheckAdmin(message.author.id)):
			for mem in message.mentions:
				IncWin(mem.id)			
				await client.send_message(message.channel,"Победа "+mem.display_name+"`а учтена.")
		else:
			await client.send_message(message.channel,"Вы не имеете привелегий для учёта побед.")

	if '!rmWin' in message.content and message.mentions:
		if (CheckAdmin(message.author.id)):
			for mem in message.mentions:
				DecWin(mem.id)			
				await client.send_message(message.channel,"Победа "+mem.display_name+"`а убрана.")
		else:
			await client.send_message(message.channel,"Вы не имеете привелегий для учёта побед.")
	
@client.event
async def on_member_join(mem):
	cursor = conn.cursor()
	if (CheckUser(mem.id)):
		cursor.execute("UPDATE Players SET onServer = '0' WHERE discordID =?", [(mem.id)])
		emb= discord.Embed(title="Предприниматель вернулся!",color=0xf55186)
	else:
		date=datetime.date.today()
		cursor.execute("INSERT INTO Players (discordID, onServer, countWins,date) VALUES (?,'0',0,'?')", [(mem.id),(str(date.year)+";"+str(date.month)+";")+str(date.day)])
		emb= discord.Embed(title="Новый предприниматель!",color=0xf55186)
	conn.commit()
	emb.set_image(url="https://images-ext-1.discordapp.net/external/em_XW7QUwRIuOBOchpLsTQayfAWVX7v6r27tqHzgAnQ/https/images-ext-2.discordapp.net/external/HxrIkjfIRYk3ZFgaFP7YwNbZcCTG_Vkljk3og-XCHdI/https/i.imgur.com/eqgYNr4.gif")
	emb.set_author(name="Aquarius System", icon_url="https://cdn.discordapp.com/app-icons/515070960584491029/c962df12528ce40169418bc8febc8e3f.png")
	emb.add_field(name="Nikname:", value=mem.display_name, inline=True)
	emb.add_field(name="Число побед:", value=GetCountWin(mem.id), inline=True)
	emb.set_thumbnail(url=mem.avatar_url)
	await client.send_message(client.get_channel('544929167188426782'),embed=emb)


@client.event
async def on_member_remove(mem):
	cursor = conn.cursor()
	cursor.execute("UPDATE Players SET onServer = '1' WHERE discordID =?", [(mem.id)])
	emb= discord.Embed(title="Предприниматель обанкротился и ушёл!",color=0xf55186)
	conn.commit()
	emb.set_image(url="https://media1.tenor.com/images/b5b717d7cc86668b60e844e01024ace4/tenor.gif")
	emb.set_author(name="Aquarius System", icon_url="https://cdn.discordapp.com/app-icons/515070960584491029/c962df12528ce40169418bc8febc8e3f.png")
	emb.add_field(name="Nikname:", value=mem.display_name, inline=True)
	emb.add_field(name="Число побед:", value=GetCountWin(mem.id), inline=True)
	emb.set_thumbnail(url=mem.avatar_url)
	await client.send_message(client.get_channel('544929167188426782'),embed=emb)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
