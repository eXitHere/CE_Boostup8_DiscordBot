import asyncio
import discord
from datetime import datetime
from connectDB import *
from setting  import *

client = discord.Client()

nameGroup = ['diff\n+ กลุ่ม 0 admin/staff', 'diff\n+ กลุ่ม 1 ผึ้งนักล่า', 'diff\n+ กลุ่ม 2 ผึ้งหลวง','diff\n+ กลุ่ม 3 ผึ้งทหาร', 'diff\n+ กลุ่ม 4 ผึ้งราชินี', 'diff\n+ กลุ่ม 5 ผึ้งงาน']


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if client.user == message.author:
        return
    if not message.guild:
        commandList = message.content.split();
        if len(commandList) == 3 and commandList[0] == 'สร้างสมุดกระจก' and commandList[1] != '' and commandList[
            2].isnumeric():
            try:
                if not check(message.author.id):
                    if int(commandList[2]) < 0 or int(commandList[2]) > 5:
                        await message.channel.send(
                            "ไม่สามารถสร้างสมุดกระจกได้ เนื่องจากใส่เลขกลุ่มนอกช่วงที่กำหนดคือ 0-5")
                    else:
                        createNewMemory(message.author.id, commandList[1], commandList[2])
                        await message.channel.send("สร้างสมุดกระจกแล้ว : " + commandList[1])
                else:
                    await message.channel.send("ไม่สามารถสร้างสมุดกระจกได้ เนื่องจากมีสมุดกระจกอยู่แล้ว")
            except:
                pass
        elif len(commandList) == 1 and len(message.attachments) == 1:
            try:
                key = False
                oldCounter = 0
                if commandList[0].isnumeric():
                    key, oldCounter = checkWithNumber(commandList[0])
                if not key:
                    key, oldCounter = checkWithName(commandList[0])
                if key:
                    # photo_name = datetime.now().strftime('%d%m%Y%H%M%S') + '.png'
                    messageID = LogDB(message.author.id, message.attachments[0].url, int(key), datetime.now(), oldCounter)
                    await message.channel.send("การส่งจดหมายสำเร็จแล้ว (ส่งไปยัง <@" + str(key) + ">)" + " message id:" + str(messageID).zfill(4))
                else:
                    await message.channel.send("การส่งจดหมายไม่สำเร็จ เนื่องจากไม่พบชื่อผู้ใช้งาน :(")
            except:
                pass

        elif len(commandList) == 1 and commandList[0] == 'สมุดกระจก':
            try:
                res = "```css\n🐝 สมุดกระจกทั้งหมด 🐝\n```"
                for i in range(0, 6):
                    res += "```" + nameGroup[i] + "\n\n"
                    for x in getMemberWithGroup(i):
                        res += '[ ' + str(x['number']).zfill(3) + ' ]: ' + x['name'] + "\n"
                    res += "```"
                    await message.channel.send(res)
                    res = ''
            except:
                pass

        elif len(commandList) == 2 and commandList[0] == 'เปลี่ยนชื่อ' and commandList[1] != '':
            try:
                editName(commandList[1], message.author.id)
                await message.channel.send("เปลี่ยนชื่อเรียบร้อยแล้ว :3")
            except:
                pass

        elif len(commandList) == 1 and commandList[0] == 'สมุดกระจกของฉัน':
            try:
                count, name, number = getCount(message.author.id)
                if str(count) == 'Noting here yep':
                    await message.channel.send('ไม่ข้อมูล :(')
                else:
                    await message.channel.send('[ ' + str(number).zfill(3) + ' ]: ' + name + "\nจำนวนจดหมายขาเข้านั้นก็คืออออ " + str(count) + " ซอง XD\n")
                    links = getMessage(message.author.id)
                    res = "จดหมายที่ส่งแล้ว\n"
                    counterUser = 0
                    for link in links:
                        counterUser += 1
                        res += '-> ID: ' + str(link['id']).zfill(4) + ' <@' + str(link['to']) + '>'+ ' timestamp: ' + link['timestamp'].strftime('%d/%m/%Y %H:%M:%S') + '\n'
                        if counterUser == 20:
                            await message.channel.send(res)
                            res += ''
                            counterUser = 0
                    if counterUser != 0:
                        await message.channel.send(res)
                    await message.channel.send("```css\nวิธีลบจดหมายขาออก พิมพ์ ลบจดหมาย XXXX (ID 4 หลักของจดหมาย)\n```")
            except:
                pass
        elif len(commandList) == 2 and commandList[0] == 'ลบจดหมาย' and commandList[1].isnumeric():
            await message.channel.send(deleteLog(commandList[1], message.author.id))
        elif len(commandList) == 1 and commandList[0] == 'help':
            try:
                await message.channel.send('กำลังทำ :(')
            except:
                pass
        elif len(commandList) == 1 and commandList[0] == 'test':
            await message.channel.send("```css\nHello [test](https://www.facebook.com/?ref=tn_tnmn)\n```")
        else:
            pass
            #print(check(message.author.id))


client.run(token)
