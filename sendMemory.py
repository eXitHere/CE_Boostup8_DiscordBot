import discord
import random
from setting import *
from sendMemoryDB import *
import asyncio
client = discord.Client()
answer = 67

async def updateStatus():
    while True:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f'{str(getAccept())}/165'))
        await asyncio.sleep(20)

@client.event
async def on_ready():
    client.loop.create_task(updateStatus())
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if client.user == message.author:
        return

    if not message.guild:

        state, name = getState(message.author.id)
        if state == -1:
            await message.channel.send('ไม่ข้อมูล :(')
        elif state == 0:
            await message.channel.send(f'{name} ใช่คุณหรือไม่ ถ้าใช่พิมพ์ไม่ ถ้าไม่พิมพ์ใช่')
            setState(message.author.id, 1)
        elif state == 1:
            try:
                if str(message.content) == 'ใช่':
                    await message.channel.send(f'{name} ใช่คุณหรือไม่ ถ้าใช่พิมพ์ไม่ ถ้าไม่พิมพ์ใช่')
                elif str(message.content) == 'ไม่':
                    await message.channel.send(
                        'มีสองวิธีในการรับรหัสผ่านไฟล์ Zip (แนะนำวิธีแรก :3 )\n1: พิมพ์มาว่า พี่กุ๊กสุดหล่อ\n2:พิมพ์มาว่า เล่นเกม (เป็นเกมเล็ก ๆ น้อย ๆ)')
                    setState(message.author.id, 2)
            except:
                pass
        elif state == 2:
            try:
                if str(message.content) == 'เล่นเกม':
                    setState(message.author.id, 3)
                    await message.channel.send(f'วิธีเล่นเกมง่าย ๆ นั้นก็คือ พิมพ์เลข 0-100 พิมพ์ถูกรับรหัสผ่านไปเยยยย')
                elif str(message.content) == 'พี่กุ๊กสุดหล่อ':
                    await message.channel.send(f'ดีมาก 5555555')
                    await message.channel.send(sendPassword(message.author.id, name))
                    setState(message.author.id, 4)
                pass
            except:
                pass
        elif state == 3:
            try:
                n = int(message.content)
                if n > answer:
                    await message.channel.send(f'น้อยกว่านี้')
                elif n < answer:
                    await message.channel.send(f'มากกว่านี้')
                else:
                    await message.channel.send(f'นี้แหละคำตอบบ')
                    await message.channel.send(sendPassword(message.author.id, name))
                    setState(message.author.id, 4)
            except:
                pass

def sendPassword(discordid, name):
    password, url = getPassword(discordid)
    return f'Click --> ' + f'{url}' + '\nFile name --> ' + str(name) + '\nPassword --> ' + str(password)

#client.run(token)