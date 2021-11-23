from passlib.hash import pbkdf2_sha256
import pymongo

# Establishing the connection
username = "daciit"
password = "supplychain"

srv = "mongodb+srv://{}:{}@supplychain-u6nhl.mongodb.net/test?retryWrites=true&w=majority".format(
    username, password)
client = pymongo.MongoClient(srv)

print("Connection Established")

db = client['Authenication']
logincol = db['Login']

FeedBack = client['FeedBack']
Message = FeedBack['Message']


def Register(email, name, password, category, hashc):

    q1 = {"email": email}
    p = logincol.find(q1)
    check = False

    for i in p:
        if email == i['email']:
            check = True

    if check:
        print("email adress already in database")
        return False
    else:
        password = pbkdf2_sha256.hash(password)
        q2 = {"name": name, "email": email,
              "password": password, 'hash': hashc}
        q2['category'] = category

        if category == "SME":
            q2['approval'] = False

        # print(q2)
        r = logincol.insert_one(q2)
        return True


def Login(email, password):
    l1 = {"email": email}
    res = logincol.find(l1)

    data = {}
    data['check'] = False
    for i in res:
        if pbkdf2_sha256.verify(password, i['password']):
            data['name'] = i['name']
            data['category'] = i['category']
            data['check'] = True
            data['hash'] = i['hash']
    print(data)
    return data
