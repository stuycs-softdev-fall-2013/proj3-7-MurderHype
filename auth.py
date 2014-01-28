from pymongo import MongoClient
client = MongoClient()
users = client.db.users


def register(username,pw):
    if users.find({"username":username}).count() == 0:
        users.insert({"username":username,"pw":pw,"posts":0})
    else: return False
    return True

def authen(username,pw):
    return users.find({"username":username,"pw":pw}).count() != 0

def changepw(username,pw,npw):
    if users.find({"username":username,"pw":pw}).count() == 1:
        users.update({'username':username},{"$set":{'pw':npw}},upsert=False)
    else: return False
    return True

if __name__ == "__main__":
    register('kevin','123')
    register('jason','456')
    register('bob','789')

    print(authen('kevin','123'))
    print(authen('kevin','321'))
    print(authen('jason','456'))
    print(authen('jason','123'))

    print("\n")
    print(changepw('kevin','123','321'))
    print(authen('kevin','321'))
    print(authen('kevin','123'))

    print(changepw('kevin','321','123'))
    print(authen('kevin','123'))
    
    
    
    users.remove()
