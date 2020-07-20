import pymongo
from setting import urlDB
client = pymongo.MongoClient(urlDB)
collection = client.databaseall.memory
Log = client.databaseall.memory_log

def check(discordid):
    for x in collection.find({'discordid': int(discordid)}):
        return True
    return False

def checkWithName(name):
    for x in collection.find({'name': str(name)}):
        return x['discordid'], x['counter']
    return False

def checkWithNumber(number):
    for x in collection.find({'number': int(number)}):
        return x['discordid'], x['counter']
    return False

def createNewMemory(discordid, name, group):
    for x in collection.find({'group_num': int(group)}):
        oldNumber = x['counter']
        collection.update_one({'group_num': int(group)}, {'$set': {'counter': oldNumber + 1}})
        break
    collection.insert_one({'discordid': discordid, 'name': name, 'group': int(group), 'counter': 0, 'number': int(oldNumber)})

def LogDB(discordid, url, to, timestamp, oldcounter):
    collection.update_one({'discordid': int(to)}, {'$set': {'counter': oldcounter + 1}})
    Log.insert_one({'discordid':discordid, 'url': url ,'to': to, 'timestamp': timestamp, 'id': int(Log.count()), 'deleted': False})
    return Log.count()-1

def getMemberWithGroup(group):
    return collection.find({'group': int(group)})

def getCount(discordid):
    for x in collection.find({'discordid': discordid}):
        return x['counter'], x['name'], x['number']
    return "Noting here yep", 0, 0

def editName(newname, discordid):
    collection.update_one({'discordid': int(discordid)}, {'$set': {'name': newname}})

def getMessage(discordid):
    return Log.find({'discordid': int(discordid), 'deleted': False})

def deleteLog(id, discordid):
    for x in Log.find({'id': int(id)}):
        if x['discordid'] == int(discordid) and not x['deleted']:
            Log.update_one({'id': int(id)}, {'$set': {'deleted': True}})
            return "ลบจดหมาย ID:" + str(id).zfill(4) + " เรียบร้อยแล้ว"
    return "กรุณาตรวจสอบหมายเลขที่ต้องการลบอีกครั้ง :("