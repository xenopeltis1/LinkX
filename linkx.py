from pymongo import MongoClient
import time
import hashlib

cluster = MongoClient("mongodb+srv://hkey:c452254k@cluster0.q5ds9.mongodb.net/users?retryWrites=true&w=majority")
db = cluster['linkx']
linkler = db['linkler']
kullanicilar = db['kullanicilar']
duyurular = db['duyurular']


def ozelvarmi(ozel):
    ali = linkler.find({})

    for _ in ali:
        if _["ozel"] == ozel or _["key"] == ozel:
            return False

    return True

def kisami(uri, user):

    alli = linkler.find({})

    for _ in alli:
        if _["uri"] == uri and _["sahip"] == user:
            return _["key"]

    return False

def allduyurular():
    duyurularim = duyurular.find({})

    
    return duyurularim

def topstats():
    linklerim = linkler.find({})
    toplink = 0
    toptik = 0
    for _ in linklerim:
        toplink +=1
        toptik += _["tik"]
    
    return toplink, toptik

def keyver():
    tit = hashlib.md5(str(time.time()).encode()).hexdigest()

    return tit[:7]


def addlink(uri, kategori, limit, ipadress,password:None, ozel:None, sahip:None):

    if not ozelvarmi(ozel) and ozel != "":
        return "Bu özel link zaten bulunmakta"

    if kisami(uri, sahip) != False:
        return kisami(uri, sahip)


    makey = keyver()
    new = {
        "uri":uri,
        "key":makey,
        "kategori":kategori,
        "limit":limit,
        "password": password,
        "ozel":ozel,
        "tik":0,
        "sahip":sahip,
        "ipadress":ipadress,
        "visitors":[]
    }

    linkler.insert_one(new)

    return makey

def izlenmeekle(key, ip):
    alls = linkler.find({})

    for _ in alls:
        if _["key"] == key or _["ozel"] == key:
            adam = _
    
    listim = adam["visitors"]

    if ip in listim:
        return adam["uri"]

    listim.append(ip)

    linkler.update_one({"key":key}, {"$set": {"tik":adam["tik"]+1}})
    linkler.update_one({"key":key}, {"$set": {"visitors": listim}})

    return adam["uri"]


def uygunmu(uname, mail):
    alli = kullanicilar.find({})

    for _ in alli:
        if _["mail"] == mail or _["username"] == uname:
            return False

    return True



def registerit(uname, mail, password):

    if not uygunmu(uname, mail):
        return "Kullanıcı adı veya mail kayıtlı"

    new = {
        "username":uname,
        "mail":mail,
        "password":password,
        "banned":"no",
        "role":"user"
    }

    kullanicilar.insert_one(new)

    return "True"

def loginit(uname, password):
    alli = kullanicilar.find({})

    for _ in alli:
        if _["username"] == uname and _["password"] == password:
            return True
    
    return False

def allkullanicilar():
    return kullanicilar.find({})

def linkleraga(username):
    tums = linkler.find({})
    linklerin = []
    for _ in tums:
        if _["sahip"] == username:
            linklerin.append(_)

    return linklerin


def userslinks(username, password):
    tum = kullanicilar.find({})

    for _ in tum:
        if _["username"] == username and hashlib.md5(_["password"].encode()).hexdigest() == password:
            return linkleraga(username)
            