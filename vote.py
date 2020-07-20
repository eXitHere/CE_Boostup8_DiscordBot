import asyncio
import discord
from setting import *

client = discord.Client()

voteStart = ''
time = 0
choices = []
counterChoices = []
messageBotVote = ''
voteMentionList = []
voteChoiceList = []
bot_spam_vote_channel = ''
bot_spam_channel = ''
duplicated = False
reportAfterEnd = False


@client.event
async def on_ready():
    global admin_role
    guild = discord.utils.find(lambda m: m.id == serverID, client.guilds)
    admin_role = discord.utils.find(lambda m: m.id == adminTeam, guild.roles)
    print(f'{client.user} (vote) has connected to Discord!')


@client.event
async def on_message(message):
    if client.user == message.author:
        return
    global bot_spam_vote_channel
    global voteMentionList
    global voteChoiceList
    global duplicated
    listCommand = message.content.split()
    if message.channel == bot_spam_vote_channel:
        if len(listCommand) == 1 and str(voteStart) != '' and message.author != client.user and listCommand[0].isnumeric():
            try:
                # index = choices.index(message.content)
                if 0 < int(listCommand[0]) <= len(choices):
                    if message.author not in voteMentionList or duplicated:
                        voteMentionList.append(message.author)
                        voteChoiceList.append(int(listCommand[0]))
                        counterChoices[int(listCommand[0]) - 1] += 1
                        await message.delete()
                        # await messageBotVote.edit(content=await printVote())
                    else:
                        await message.delete(delay=3)
                        await bot_spam_vote_channel.send("ฮฮั่นแน่~~ ชอบโกงรึเปล่า!!", delete_after=3)
                        pass
            except:
                pass
    if message.content.startswith(botID):
        if len(listCommand) > 1:
            if listCommand[1] == 'vote':  # and isAdmin(message.author.roles):
                if str(bot_spam_vote_channel) == '' or bot_spam_vote_channel == message.channel:
                    bot_spam_vote_channel = message.channel
                    if len(listCommand) > 3:
                        if len(listCommand) > 4 and listCommand[4].isnumeric():
                            if len(listCommand) == 6 and listCommand[5].isnumeric():
                                canDuplicate = bool(int(listCommand[5]) != 0)
                                getReportAfterEnd = 0
                            elif len(listCommand) == 7 and listCommand[5].isnumeric() and listCommand[6].isnumeric():
                                canDuplicate = bool(int(listCommand[5]) != 0)
                                getReportAfterEnd = bool(int(listCommand[6]) != 0)
                            else:
                                canDuplicate = 1
                                getReportAfterEnd = 0
                            await vote(message.author, message, listCommand[2], listCommand[3], int(listCommand[4]),
                                       canDuplicate, getReportAfterEnd)
                            return
                        elif len(listCommand) == 4:
                            await vote(message.author, message, listCommand[2], listCommand[3])
                            return
                    elif len(listCommand) > 2:
                        await vote(message.author, message, listCommand[2])
                        return
                    else:
                        await message.delete(delay=5)
                        await message.channel.send("รูปแบบในการสั่งไม่ถูกต้อง :(", delete_after=3)
                else:
                    await message.delete(delay=5)
                    await message.channel.send("Sorry, I'm busy (Someone is voting)", delete_after=5)
                    return


async def taskForVote():
    global time
    global voteStart
    global messageBotVote
    global bot_spam_vote_channel
    while True:
        try:
            if time >= 0 and voteStart != '':
                time -= 1
                await messageBotVote.edit(content=await printVote())
                if time <= 0:
                    await reportVote()
                    voteStart = ''
                    messageBotVote = ''
                    bot_spam_vote_channel = ''
        except:
            pass
        # print(time)
        await asyncio.sleep(1)


async def printVote():
    global choices
    global counterChoices
    global bot_spam_channel
    message = f'**Vote started by {voteStart.mention}**\n\n'
    index = 1
    for c in choices:
        message += f'**{counterChoices[index - 1]} เสียง'.ljust(20) + f'**```fix' + \
                   f'\nพิมพ์ {str(index)}'.ljust(10) + f' : {c}```'
        index += 1
    if time > 0:
        message += f'\n=== vote closing in **{time}** second(s) ===\n'
    elif time <= 0:
        message += f'\n=== this vote has ended ===\n'
    return message


async def reportVote():
    global choices
    global counterChoices
    global bot_spam_channel
    global reportAfterEnd
    global voteMentionList
    global voteChoiceList
    message = f'>>> Vote started by {voteStart.mention}\n\n'
    index = 1
    mention = [''] * len(choices)
    if reportAfterEnd:
        index = 0
        mention = [''] * len(choices)
        for x in voteMentionList:
            mention[voteChoiceList[index] - 1] += str(x.mention + ' ')
            index += 1
    index = 1
    for c in choices:
        message += f'**{counterChoices[index - 1]} เสียง'.ljust(20) + f'**{mention[index - 1]}```fix' + \
                   f'\nพิมพ์ {str(index)}'.ljust(10) + f' : {c}```'
        index += 1
    message += f'\n=== **this vote has ended** ===\n'
    voteMentionList = []
    voteChoiceList = []
    if len(message) > 1950:
        await bot_spam_vote_channel.send("สรุปผลไม่ได้เนื่องจากข้อความยาวเกินขีดจำกัด :(")
    else:
        await messageBotVote.delete()
        await bot_spam_vote_channel.send(message)


async def vote(owner, messageOri, command, choiceAll=[], timex=60, duplicatedX=True, reportAfterEndX=False):
    global duplicated
    global reportAfterEnd
    global voteStart
    global choices
    global counterChoices
    global time
    global messageBotVote
    if command == 'start' and str(voteStart) == '':
        choices = choiceAll.split(',')
        if len(choices) > 10:
            await bot_spam_vote_channel.send("vote ตัวเลือกเยอะเกิน 10 กรุณาลองใหม่น้า :(")
            return
        voteStart = owner
        if timex <= 0:
            timex = 60
        time = timex
        duplicated = bool(duplicatedX)
        reportAfterEnd = bool(reportAfterEndX)
        counterChoices = [0] * len(choices)
        messageBotVote = await bot_spam_vote_channel.send(await printVote())
        return
    elif command == 'start' and str(voteStart) != '':
        await messageOri.delete(delay=5)
        await bot_spam_vote_channel.send(f"Can't start vote! {voteStart.mention} has already started the vote :(",
                                         delete_after=5)
        return
    elif command == 'stop' and str(voteStart) == '':  ##################
        await messageOri.delete(delay=5)
        await bot_spam_vote_channel.send(f"Sorry, there are currently no votes!\n\n")
        return
    elif command == 'stop' and isAdmin(owner.roles) or voteStart == owner:
        time = 3
        await bot_spam_vote_channel.send(f"Vote ended by {owner.mention} :)\n\n")
        return
    elif command == 'stop' and voteStart != owner:
        await messageOri.delete(delay=5)
        await bot_spam_vote_channel.send(f"Can't stop vote! this vote started by {voteStart.mention}:(\n\n ",
                                         delete_after=5)
        return


def isAdmin(roles):
    try:
        index = roles.index(admin_role)
        return True
    except:
        return False


client.loop.create_task(taskForVote())
client.run(token)
