import asyncio
from setting import *
import json
import discord
from database import getDB
from datetime import datetime
client = discord.Client()
@client.event
async def on_ready():
    global guild
    client.loop.create_task(updateStatus())
    print(f'{client.user} (Grader) has connected to Discord!')
    guild = discord.utils.find(lambda m: m.id == serverID, client.guilds)

counterMsg = 0
isStart = False
@client.event
async def on_message(message):
    global counterMsg
    global isStart
    if client.user == message.author:
        return
    if message.content == "fksalasdiasdpzxcozpdoasdlas;dzxlc;zxlvsdjfkasdf":
        isStart = True
        await message.channel.send("เริ่ม! จัดไปให้ครบ 2000 คอมเม้น!")
        return
    if isStart:
        counterMsg += 1
        print(counterMsg)
        if counterMsg >= 2000:
            isStart = False
            await message.channel.send("ครบแล้ว")
            await sendData()

async def sendData():
    global guild
    for x in getDB():
        try:
            user = discord.utils.find(lambda m: m.id == int(x['discordkey']), guild.members)
            await user.send(f"""👏 👏 ขอบคุณที่ให้ความสนใจบอทผึ้งน้อย🐝 นี้กันนะค้าบบ 
สิ่งที่พี่ ๆ ฝากของขวัญเล็ก ๆ น้อย ๆ มาให้บอทผึ้งน้อยนี้ก็คืออออออออออ

ของเล่นแก้เหงานั่นเองงงง  >>>  https://grader.everythink.dev/  <<<

ของเล่นชิ้นนี้มันก็ต้องมีความลับกันบ้างแหละ แต่สำหรับน้อง ๆ พี่เลย
มอบกุญแจไขความลับนี้ให้ 🔐 วี๊วววววว //ดีใจแหละดูออกพี่พิมพ์ยังดีใจเลย

Username```fix
{x['username']}
```Password```yaml
{x['password']}
```""")
        except:
            pass
    print("Send complete");

async def updateStatus():
    await client.wait_until_ready()
    while True:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name="counter-> " + str(counterMsg)))
        await asyncio.sleep(1)

#client.run(token)