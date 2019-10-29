import hashlib
from MyLibs import configure, db

def check(session):
    if 'logged_in' in session:
        username, passwordH = session['logged_in'].split("=")
        login = db.check(username, passwordH)
        if login == "Wrong":
            return(False)
        else:
            return(True)

def login(username, password):
    login = db.check(username, hashlib.sha256(bytes(password, "utf8")).hexdigest())
    return(login)


def create(session, username, password):
    session['logged_in'] = username + "=" + hashlib.sha256(bytes(password, "utf8")).hexdigest()
    return(session)
