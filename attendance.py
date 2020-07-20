import asyncio
from setting import *
import json
import discord
from database import addAttedance
from datetime import datetime

client = discord.Client()

@client.event
async def on_ready():
    global bot_text_student
    global admin_role
    global guild
    global student
    global studyAllRoom
    global bot_voice1_student
    student = []
    bot_text_student = []
    bot_voice1_student = []
    guild = discord.utils.find(lambda m: m.id == serverID, client.guilds)
    studyAllRoom = discord.utils.find(lambda m: m.id == voiceStudy, guild.channels)
    for atext in textTeam:
        bot_text_student.append(discord.utils.find(lambda m: m.id == atext, guild.channels))
    for astudent in listTeam:
        student.append(discord.utils.find(lambda m: m.id == astudent, guild.roles))
    for aroom in voice1Team:
        bot_voice1_student.append(discord.utils.find(lambda m: m.id == aroom, guild.channels))
    guild = discord.utils.find(lambda m: m.id == serverID, client.guilds)
    admin_role = discord.utils.find(lambda m: m.id == adminTeam, guild.roles)
    print(f'{client.user} (attendance) has connected to Discord!')

@client.event
async def on_message(message):
    if client.user == message.author:
        return
    member = message.author
    if message.content.startswith(botID):
        ## with spam bot channel
        listCommand = message.content.split()
        if len(listCommand) > 1:
            if listCommand[1] == 'check':
                student1 = []
                student2 = []
                student3 = []
                student4 = []
                student5 = []
                dateCommand = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                for x in range(0, 5):
                    await bot_text_student[x].send(
                        f"**ค้นหาเด็กดี . . . ** By {message.author.mention} {dateCommand} \n {student[x].mention} เด็ก ๆ อยู่ไหนกันน๊าาา ~~~~")
                await asyncio.sleep(3)
                timeTodelete = 5
                for x in range(timeTodelete, 0, -1):
                    for y in range(0, 5):
                        await bot_text_student[y].send(f"{student[y].mention * x}", delete_after=timeTodelete + x)
                for y in range(0, 5):
                    await bot_text_student[y].send(f"เริ่มแล้วน้า", delete_after=5)
                await asyncio.sleep(3)
                global jsonMention
                jsonMention = []
                for x in studyAllRoom.members:
                    index = isStudent(x.roles)
                    if index >= 0:
                        jsonMention.append(str(x.id))
                        if index == 0:
                            student1.append(x.mention)
                        elif index == 1:
                            student2.append(x.mention)
                        elif index == 2:
                            student3.append(x.mention)
                        elif index == 3:
                            student4.append(x.mention)
                        elif index == 4:
                            student5.append(x.mention)

                for y in bot_voice1_student:
                    for x in y.members:
                        jsonMention.append(str(x.id))
                        index = isStudent(x.roles)
                        if index >= 0:
                            if index == 0:
                                student1.append(x.mention)
                            elif index == 1:
                                student2.append(x.mention)
                            elif index == 2:
                                student3.append(x.mention)
                            elif index == 3:
                                student4.append(x.mention)
                            elif index == 4:
                                student5.append(x.mention)
                jsonRes = {
                    'date': dateCommand,
                    'member': jsonMention
                }
                addAttedance(jsonRes)
                listStudent = [student1, student2, student3, student4, student5]
                index = 0
                for indexList in listStudent:
                    listMention = ''
                    for astudent in indexList:
                        listMention += f'-> {astudent}\n'

                    if len(indexList) > 0:
                        await bot_text_student[index].send(f"```diff\n+--------  รายชื่อเด็กดี :D  --------+\n```{listMention}")
                    else:
                        await bot_text_student[index].send(f"```diff\n+--------  รายชื่อเด็กดี :D  --------+\n```-> :(")
                    listMention = ''
                    index += 1


def isStudent(roles):
    for y in roles:
        index = 0
        for x in student:
            if x == y:
                return index
            index += 1
    return -1


async def check():
    for x in guild.members:
        if x.status == 'offline' or x.bot or not x.voice:
            continue
        if str(admin_role.id) in str(x.roles):
            pass
            # await bot_spam_channel.send(f'ทดสอบระบบเชคชื่อ {x.mention} เข้าเรียน')


async def boardCast(message):
    for x in bot_text_student:
        await x.send(f"ประกาศ ๆ {message}", delete_after=20)


def isAdmin(roles):
    try:
        index = roles.index(admin_role)
        return True
    except:
        return False




client.run(token)
