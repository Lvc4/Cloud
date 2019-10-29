import sqlite3 as sql
import datetime
import hashlib
from MyLibs import configure

database = configure.database

def delete(name):
	con = sql.connect(database)
	cur = con.cursor()
	cur.execute("DELETE FROM files WHERE name='" + name + "'")
	con.commit()
	con.close()
    
def check_valid(username):
    con = sql.connect(database)
    cur = con.cursor()
    try:
        cur.execute("select * from users where username = '" + username + "'")
        user = cur.fetchall()
        print(user[0][1] + " - - username")
        if user[0][1] == username:
            return(False)
        else:
            return(True)
    except:
        return(True)

def check(username, password):
	con = sql.connect(database)
	cur = con.cursor()
	try:
		cur.execute("select * from users where username = '" + username + "'")
		user = cur.fetchall()
		print(user[0][1] + " - - username")
		print(password + " - - password hash")
		if user[0][2] == password:
			return(user[0][3])
		else:
			return("Wrong")
	except:
		return("Wrong")


def insert(username,password, path):
	con = sql.connect(database)
	cur = con.cursor()
	cur.execute("insert into users(username, password, path) values ('" + username + "', '" + hashlib.sha256(bytes(password, "utf8")).hexdigest() + "', '" + path + "')")
	con.commit()


