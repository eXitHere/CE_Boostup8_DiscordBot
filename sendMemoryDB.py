import pymongo
from setting import urlDB
client = pymongo.MongoClient(urlDB)
collection = client.databaseall.sendMemory

def getState(discordid):
    for x in collection.find({'discordid': int(discordid)}):
        return x['state'], x['name']
    return -1, 'none'

def setState(discordid, value):
    collection.update_one({'discordid': int(discordid)}, {'$set': {'state': int(value)}})

def getPassword(discordid):
    for x in collection.find({'discordid': int(discordid)}):
        return x['password'], x['url']
    return -1, 'none'

def getAccept():
    return collection.find({'state': int(4)}).count()