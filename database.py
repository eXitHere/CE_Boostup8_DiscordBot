import pymongo
from setting import *
client = pymongo.MongoClient(urlDB)
collection = client.databaseall.user
attendanceDB = client.databaseall.attendance
graderID = client.databaseall.graderID
#collection.insert_one({'authkey':'thana', 'discordkey':''})

def getDB():
    return graderID.find()

def findAndUpdate(authkey='none', discordID='none'):
    for x in collection.find({'authkey': authkey}):
        if x['discordkey']== '':
            collection.update_one({'authkey': authkey}, {'$set': {'discordkey': str(discordID)}})
            return ['ยินดีต้อนรับสู่การทดสอบระบบ สำหรับค่าย CE Boost up 8!', x['role']]
        else:
            return [authkey + ' นี้ถูกลงทะเบียนไปแล้ว กรุณาติดต่อ staff :(', 'none']
        break;

    return ['ไม่พบรหัสยืนยันตัวตนนี้ กรุณาลองใหม่อีกครั้งครับ ในรูปแบบ 000Xxxx ลำดับในใบรายชื่อ ตามด้วยชื่อจริงขึ้นต้นด้วยตัวพิมพ์ใหญ่', 'none']

def addAttedance(data):
    attendanceDB.insert_one(data)

def getReport():
    staff_count   = 0
    student_count = 0
    sum_user      = 0
    for x in collection.find():
        if x['discordkey'] != '':
            if str(x['role']) in str(listStaff):
                staff_count += 1
            else:
                student_count +=1
        sum_user += 1
    return 'สมาชิกทั้งหมด: ' + str(sum_user) + '\nstaff ลงทะเบียนแล้ว ' + str(staff_count) + '\nstudent ลงทะเบียนแล้ว ' + str(student_count)