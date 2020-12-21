from flask import Flask, render_template, request, jsonify, redirect, make_response
import linkx
import hashlib


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/duyurular")
def duyurular():
    duyurs = linkx.allduyurular()
    ds = []
    for _ in duyurs:
        ds.append(_)
    
    ds.reverse()

    return render_template("duyurular.html", duyurus=ds)

@app.route("/short")
def kisaltpage():

    s1, s2 = linkx.topstats()
    return render_template("kisalt.html", s1=s1, s2=s2)

@app.route("/short", methods=["POST"])
def kisaltislem():
    try:
        if request.environ['HTTP_X_FORWARDED_FOR']:
            ip = request.environ['HTTP_X_FORWARDED_FOR']
    except:
        ip = request.environ['REMOTE_ADDR']
    
    password = request.form.get("password")
    limit = request.form.get("limit")
    kategori = request.form.get("kategori")
    ozellink = request.form.get("ozellink")
    limit = request.form.get("limit")
    uribro = request.form.get("uribro")

    usernam = request.cookies.get("userx")
    pwd = request.cookies.get("passx")

    alim = linkx.allkullanicilar()
    sahibim = None
    for _ in alim:
        if _["username"] == usernam and hashlib.md5(_["password"].encode()).hexdigest() == pwd:
            sahibim = usernam

    if uribro == "":
        return "Link boş olamaz"
    
    a = linkx.addlink(uribro, kategori, limit, ip, password, ozellink, sahibim)

    return a

@app.route("/<keyim>")
def linksayfa(keyim):
    try:
        if request.environ['HTTP_X_FORWARDED_FOR']:
            ip = request.environ['HTTP_X_FORWARDED_FOR']
    except:
        ip = request.environ['REMOTE_ADDR']

    asa = linkx.izlenmeekle(keyim, ip)

    return redirect(asa, 302)

@app.route("/login")
def loginpage():
        
    us = request.cookies.get("userx")
    pas = request.cookies.get("passx")

    alli = linkx.allkullanicilar()

    for _ in alli:
        if _["username"] == us and hashlib.md5(_["password"].encode()).hexdigest() == pas:
            return redirect("/index")
    
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def loginitpage():
    
    uname = request.form.get("username")
    password = request.form.get("password")
    print(uname, password)
    sonuc = linkx.loginit(uname, password)

    if sonuc:
        resp = make_response(redirect("/index"))

        resp.set_cookie("userx", uname)
        resp.set_cookie("passx", hashlib.md5(password.encode()).hexdigest())

        return resp
    
    return "Şifren veya kullanıcı adın yanlıştı"

@app.route("/index")
def indexpage():
    
    return render_template("index.html")

@app.route("/register")
def regpage():
    
    us = request.cookies.get("userx")
    pas = request.cookies.get("passx")

    alli = linkx.allkullanicilar()

    for _ in alli:
        if _["username"] == us and hashlib.md5(_["password"].encode()).hexdigest() == pas:
            return redirect("/index")

    resp = make_response(render_template("register.html"))
    resp.set_cookie('userx', '', expires=0)
    resp.set_cookie('passx', '', expires=0)

    return resp

@app.route("/register", methods=["POST"])
def registeritb():
    uname = request.form.get("username")
    mailad =  request.form.get("mailadress")
    password =  request.form.get("password")

    test = linkx.registerit(uname, mailad, password)

    if test == "True":
        return redirect("/login", 302)

    return test

@app.route("/links")
def linkspage():
    us = request.cookies.get("userx")
    pas = request.cookies.get("passx")

    alli = linkx.allkullanicilar()

    for _ in alli:
        if _["username"] == us and hashlib.md5(_["password"].encode()).hexdigest() == pas:
            linkler = linkx.userslinks(us, pas)
            return render_template("links.html", linkler=linkler)
    
    return redirect("/index")


if __name__ == "__main__":
    app.run(debug=True)