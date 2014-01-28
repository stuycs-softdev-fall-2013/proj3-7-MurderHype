from pymongo import MongoClient
from time import strftime
client = MongoClient()
thread = client.db.thread
response = client.db.response

def write(author,title,post):
    if thread.find({"title":title}).count()==0:
        thread.insert({"title":title,'author':author,'time':strftime("%X %x"),'hits':0,'post':post,'responses':0})
    else: return False
    return True

def getTitles():
    return [x for x in thread.find({},fields={'_id':False,'post':False,'response':False})]

def edit(title,npost):
    thread.update({'title':title},{"$set":{'post':npost}})

def delete(title = ""):
    if title != "":
        if thread.find({"title":title}).count()!=0:
            thread.remove({"title":title})

def getPost(title):
    return [x for x in thread.find({"title":title},fields={'_id':False,'response':False})]

def hit(title):
    thread.update({'title':title},{"$inc":{'hits':1}})

def respond(responder,title,text):
    id = [x['responses'] for x in thread.find({'title':title})]
    response.insert({'author':responder,'title':title,'response':text,'id':id[0],'time':strftime("%X %x"),'likes':0})
    thread.update({'title':title},{'$inc':{'responses':1}})
    return id[0]

def upvote(id):
    response.update({'id':id},{"$inc":{'likes':1}})

def getResponses(title):
    return [x for x in response.find({'title':title},fields={'_id':False,'id':False,'title':False})]

if __name__ == "__main__":
    write('kevin','first post','FIRST')
    write('kevin','my 2nd post','ahhahahah')
    write('jason','first','new here hi guys')
    write('bob','new here','yolasiku')

    print(getTitles())
    print(getPost('first post'))
    edit('first post','sry for being ass')
    hit('first post')
    hit('first post')
    print(getPost('first post'))

    print('done w/ this shit')
    print(respond('bob','first post','such bm'))
    print([x for x in response.find({})])
    print(getPost('first post'))

    print(respond('jason','first post','much wow'))
    print(respond('kevin','first post','so smart'))
    print([x for x in response.find({})])
    print(getResponses('first post'))
    print(getPost('first post'))

    thread.remove()
    response.remove()
