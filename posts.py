from pymongo import MongoClient
from time import strftime
client = MongoClient()
posts = client.db.posts
users = client.db.users


def write(author,title,post):
    if posts.find({"Title":title}).count() == 0:
        posts.insert({"author":author,"title":title,"time":strftime("%X %x"),"post":post})
        users.update({"username":author},{"$inc":{"posts":1}})
    else: return False
    return True

def getPosts(author):
    return [x for x in posts.find({"author":author},fields={"_id":False,"author":False})]

def getRanking():
    candidates = users.find({},fields={"_id":False,"pw":False})
    ranking = sorted(candidates, key=lambda x: x['posts'],reverse=True)
    return ranking[:10]


if __name__ == "__main__":
    write('kevin','asd','qweqweqwe')
    write('jason','456','asdasdasdad')
    write('bob','123','zczxczxczxc')
    write('kevin','qwerty',"linkin park")

    print(getPosts('kevin'))
    print(getPosts('jason'))

    print(getRanking())
    
    posts.remove()
