import asyncio

from discord.ext import commands
import discord
import re
from database import findAndUpdate, getReport
from setting  import *
client = discord.Client()

@client.event
async def on_ready():
    global guild
    global bot_spam_channel
    global bot_spam_channel_all
    global bot_text_student
    global bot_voice1_student
    global bot_voice2_student
    global admin_role
    global staff
    global student
    staff            = []
    student          = []
    bot_text_student = []
    bot_voice1_student = []
    bot_voice2_student = []
    guild            = discord.utils.find(lambda m: m.id == serverID, client.guilds)
    bot_spam_channel = discord.utils.find(lambda m: m.id == bot_spam_chat, guild.channels)
    bot_spam_channel_all = discord.utils.find(lambda m: m.id == bot_spam_chat_all, guild.channels)
    admin_role = discord.utils.find(lambda m: m.id == adminTeam, guild.roles)
    for astaff in listStaff:
        staff.append(discord.utils.find(lambda m: m.id == astaff, guild.roles))
    for astudent in listTeam:
        student.append(discord.utils.find(lambda m: m.id == astudent, guild.roles))
    for atext in textTeam:
        bot_text_student.append(discord.utils.find(lambda m: m.id == atext, guild.channels))
    for aroom in voice1Team:
        bot_voice1_student.append(discord.utils.find(lambda m: m.id == aroom, guild.channels))
    for aroom in voice2Team:
        bot_voice2_student.append(discord.utils.find(lambda m: m.id == aroom, guild.channels))
    client.loop.create_task(updateStatus())
    for x in staff:
        print(x)
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    member = message.author

    #direct msg
    if not message.guild:
        # authentication
        if re.search(r'\d[a-zA-Z]', message.content):
            #Updating
            #await message.channel.send("กำลังอัพเดทระบบอยู่ ค่อยมายืนยันตัวตนใหม่น้า")
            #return
            res = findAndUpdate(message.content, message.author.id)
            try:
                if res[1] != 'none':
                    role = discord.utils.get(guild.roles, id=int(res[1]))
                    print(role)
                    member = discord.utils.find(lambda m : m.id == member.id, guild.members)
                    await bot_spam_channel.send(message.content + " อยู่ในกลุ่ม " + str(role) +" ลงทะเบียนแล้ว " + '👋')
                    await member.add_roles(role)
            except Exception as e:
                print(e)
                pass
            await message.channel.send(res[0])

    elif message.content.startswith(botID):
        ## with spam bot channel
        listCommand = message.content.split()
        if message.channel == bot_spam_channel:
            listResult = []
            if isAdmin(member.roles):
                if listCommand[1] == 'clear':
                    await message.channel.purge(limit=10)
                    return
                elif 'getroles' in message.content.lower():
                    for x in message.guild.roles:
                        listResult.append(x)
                    await message.delete(delay=10)
                    await message.channel.send(listResult, delete_after = 10)
                    return
                elif 'getchannels' in message.content.lower():
                    for x in message.guild.channels:
                        listResult.append(x)
                    await message.delete(delay=10)
                    #await message.channel.send(listResult, delete_after = 10)
                    return
                elif 'getreport' in message.content.lower():
                    await message.delete(delay=10)
                    await message.channel.send(getReport(), delete_after = 10)
                    return
                else :
                    if len(listCommand) > 1:
                        if listCommand[1] == 'staywithme':
                            if not member.voice:
                                await message.delete(delay=10)
                                await message.channel.send("เข้าห้องก่อนแล้วค่อยสั่งนะครับ!", delete_after=10)
                                return
                            await staywithme(member, listCommand)
                            await message.delete(delay=10)
                            await message.channel.send("STAYWITHME!", delete_after=10)
                            return
                        elif listCommand[1] == 'mute':
                            await muteAdmin(member, listCommand, True)
                            await message.delete(delay=10)
                            await message.channel.send("MUTE!", delete_after=10)
                            return
                        elif listCommand[1] == 'unmute':
                            await muteAdmin(member, listCommand, False)
                            await message.delete(delay=10)
                            await message.channel.send("UNMUTE!", delete_after=10)
                            return
                        elif listCommand[1] == 'deafen':
                            await deafenAdmin(member, listCommand, True)
                            await message.delete(delay=10)
                            await message.channel.send("DEAFEN!", delete_after=10)
                            return
                        elif listCommand[1] == 'undeafen':
                            await deafenAdmin(member, listCommand, False)
                            await message.delete(delay=10)
                            await message.channel.send("UNDEAFEN!", delete_after=10)
                            return
                        elif listCommand[1] == 'check':
                            pass
                            return
            else:
                await message.delete(delay=10)
                await message.channel.send("ขอโทษนะ คำสั่งนี้เฉพาะให้ admin ใช้", delete_after=10)
                return

        ## ห้อง spam ทั่วไป
        elif message.channel == bot_spam_channel_all:
            if listCommand[1] == 'clear' and isAdmin(member.roles):
                await message.channel.purge(limit=10)
                return
            elif len(listCommand) == 1:
                await message.channel.send(f"Hi! {message.author.mention} กินข้าวยังเพื่อนนนน")
        #มาเรียน
        elif listCommand[1] == 'บรรยากาศการเรียน' and (checkPermission(member.roles) or isAdmin(member.roles)):
            await staywithme2(member, listCommand)
            await message.channel.send("มาเรียนกันเร็ว")
            return
        #เงียบก่อนน้า
        elif listCommand[1] == 'หุปปาก' and (checkPermission(member.roles) or isAdmin(member.roles)):
            await muteV2(member, listCommand, True)
            await message.delete(delay=10)
            await message.channel.send("ขอปิดไมค์แป้บน้า!", delete_after=10)
            return
        # คุยได้แล้ว
        elif listCommand[1] == 'แหกปาก' and (checkPermission(member.roles) or isAdmin(member.roles)):
            await muteV2(member, listCommand, False)
            await message.delete(delay=10)
            await message.channel.send("เปิดไมค์ให้แล้ว!", delete_after=10)
            return
        elif listCommand[1] == 'จุ๊จุ๊' and (checkPermission(member.roles) or isAdmin(member.roles)):
            await deafenV2(member, listCommand, True)
            await message.delete(delay=10)
            await message.channel.send("ขอปิดเสียงแป้บน้า!", delete_after=10)
            return
        # คุยได้แล้ว
        elif listCommand[1] == 'ฟัง!' and (checkPermission(member.roles) or isAdmin(member.roles)):
            await deafenV2(member, listCommand, False)
            await message.delete(delay=10)
            await message.channel.send("ฟังได้แล้วน้าา!", delete_after=10)
            return
        elif len(listCommand) > 1 and listCommand[1] == 'vote':
            pass
        elif len(listCommand) > 1 and listCommand[1] == 'clear' and isAdmin(member.roles):
            await message.channel.purge(limit=10)
        else:
            if '.help' in message.content:
                await message.channel.send(f"""```diff
- 1.เข้ากลุ่มไลน์ จะเจอ key ที่พี่ ๆ ส่งมาให้เป็นรูป -
``````fix
* 2. นำ key ที่ได้ส่ง Direct Message มาที่บอท Manager ในรายชื่อด้านขวา โดยคลิกซ้ายที่บอท หลังจากนั้นใส่ key ลงในช่อง "Message @Manager" แล้วกด Enter *
``````diff
+ 3. เมื่อลงทะเบียนสำเร็จบอทจะตอบกลับว่า "ยินดีต้อนรับสู่ค่าย CE Boost up 8!"  และจะได้  Role ตามกลุ่มสังเกตได้ที่ด้านขวา +
```""")
                await message.channel.send(file=discord.File('help.png'))
                pass
            else:
                await message.channel.send("ส่งมาผิดห้องแชท บอทข้อลบข้อความนะครับ", delete_after=3)
                await message.delete(delay=3)

def checkPermission(roles):
    index = -1
    for astaff in staff:
        try:
            index = roles.index(astaff)
        except:
            pass
        if index != -1:  ## แสดงว่าเป็น staff
            break
    if index != -1 :
        print("You can");
        return True
    else:
        print("You can't")
        return False

async def memberCount():
    count = 0
    for x in guild.members:
        if str(x.status) != 'offline' and not x.bot:
            #print(x.name, x.status)
            count += 1
    return 'ออนไลน์ทั้งหมด ' + str(count) + ' คน'

def isAdmin(roles):
    try:
        index = roles.index(admin_role)
        return True
    except:
        return False

async def staywithme2(owner, listCommand):
    listTag = []
    for x in listCommand[2:]:
        splited = x[3:-1]
        canUse = discord.utils.find(lambda m: str(m.id) == str(splited), student)
        if canUse:
            listTag.append(splited)
            continue
        else:
            canUse = discord.utils.find(lambda m: str(m.id) == str(splited), staff)
            if canUse:
                listTag.append(splited)
                continue
    for x in guild.members:
        if x.status == 'offline' or x.bot or not x.voice or owner.id == x.id:
            continue
        for y in listTag:
            if str(y) in str(x.roles):
                await x.edit(voice_channel=owner.voice.channel)
                break

async def muteV2(owner, listCommand, isMute):
    listTag = []
    for x in listCommand[2:]:
        splited = x[3:-1]
        canUse = discord.utils.find(lambda m: str(m.id) == str(splited), student)
        if canUse:
            listTag.append(splited)
            continue
        else:
            canUse = discord.utils.find(lambda m: str(m.id) == str(splited), staff)
            if canUse:
                listTag.append(splited)
                continue
    for x in guild.members:
        if x.status == 'offline' or x.bot or not x.voice or owner == x:
            continue
        for y in listTag:
            if str(y) in str(x.roles):
                await x.edit(mute=isMute)
                break

async def deafenV2(owner, listCommand, isDeafen):
    listTag = []
    for x in listCommand[2:]:
        splited = x[3:-1]
        canUse = discord.utils.find(lambda m: str(m.id) == str(splited), student)
        if canUse:
            listTag.append(splited)
            continue
        else:
            canUse = discord.utils.find(lambda m: str(m.id) == str(splited), staff)
            if canUse:
                listTag.append(splited)
                continue
    for x in guild.members:
        if x.status == 'offline' or x.bot or not x.voice or owner == x:
            continue
        for y in listTag:
            if str(y) in str(x.roles):
                await x.edit(deafen=isDeafen)
                break

async def staywithme(owner, listCommand):
    listTag = []
    for x in listCommand[2:]:
        listTag.append(x[3:-1])
    for x in guild.members:
        if x.status == 'offline' or x.bot or not x.voice or owner.id == x.id:
            continue
        for y in listTag:
            if str(y) in str(x.roles):
                await x.edit(voice_channel=owner.voice.channel)
                break

async def muteAdmin(owner, listCommand, isMute):
    listTag = []
    for x in listCommand[2:]:
        listTag.append(x[3:-1])
    for x in guild.members:
        if x.status == 'offline' or x.bot or not x.voice or owner == x:
            continue
        for y in listTag:
            if str(y) in str(x.roles):
                await x.edit(mute=isMute)
                break

async def deafenAdmin(owner, listCommand, isDeafen):
    listTag = []
    for x in listCommand[2:]:
        listTag.append(x[3:-1])
    for x in guild.members:
        if x.status == 'offline' or x.bot or not x.voice or owner == x:
            continue
        for y in listTag:
            if str(y) in str(x.roles):
                await x.edit(deafen=isDeafen)
                break

async def updateStatus():
    listStatus = ['counter', 'Coding', 'Testing', 'Debugging', 'Lovey', 'Cute <3', 'ได้กลิ่นคนหิวโจทย์ ><']
    indexStatus = 0
    while True:
        await client.wait_until_ready()
        if indexStatus == 0:
            await client.change_presence(status=discord.Status.online, activity=discord.Game(name=await memberCount()))
            await asyncio.sleep(20)
        else:
            await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name=listStatus[indexStatus]))
            await asyncio.sleep(5)
        indexStatus += 1
        indexStatus %= len(listStatus)
        print(indexStatus)

client.run(token)
