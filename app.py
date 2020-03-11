from flask import Flask, render_template, request, make_response
from werkzeug import secure_filename
import sqlite3
app = Flask(__name__)

#SqLite Database
conn = sqlite3.connect('test.db')
print ("Opened database successfully")
conn.execute('''CREATE TABLE IF NOT EXISTS admin
        (username TEXT PRIMARY KEY NOT NULL,
         name TEXT NOT NULL,
		 password TEXT NOT NULL 
        );''')
conn.close()

@app.route('/')
def login():
   #conn = sqlite3.connect('test.db')
   #conn.execute("INSERT INTO admin (username, name, password) VALUES ('rehan', 'Md Rehan', 'romy12345')")
   #conn.commit()
   #conn.close()
   username = request.cookies.get('username')
   if username != None:
    return '<META http-equiv="refresh" content="1.0;URL=/adminpanel"/>'
   return render_template('login.html',name = 'Admin')
   
@app.route('/adminpanel')
def adminpanel():
   username = request.cookies.get('username')
   if username == None:
    return '<META http-equiv="refresh" content="1.0;URL=/"/><h1>Session Expire</h1>'
	
   return render_template('adminpanel.html',username = username)
	
@app.route('/loginsubmit', methods = ['GET', 'POST'])
def loginsubmit():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
	
    opassword = ''
	
    conn = sqlite3.connect('test.db')
    cursor = conn.execute("SELECT username, name, password FROM admin")
    for row in cursor:
     print ("ID = ", row[0])
     print ("NAME = ", row[1])
     #print ("PASSWORD = ", row[2])
     opassword = row[2]
	
    if opassword != password:
      return '<h1>Error</h1>'
	
    res = make_response('<META http-equiv="refresh" content="2.0;URL=adminpanel"/><h1>Logged in</h1>')
    res.set_cookie("username", "rehan", max_age = 60*60*24)
    return res

@app.route('/logout')
def logout():
    res = make_response('<META http-equiv="refresh" content="1.0;URL=/"/><h1>Logged out</h1>')
    res.set_cookie("username", "", max_age = 0)
    return res
		
if __name__ == '__main__':
   app.run(host='' debug = True)