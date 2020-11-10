from flask import Flask, render_template, request, redirect, session

import sqlite3
app = Flask(__name__)
app.secret_key="sunabaco"

@app.route("/test")
def debug():
  return render_template("/tasklist.html")

@app.route("/test3")
def debug3():
  return render_template("/uselist.html")

@app.route("/resultwin")
def debug2():
  return render_template("/resultwin.html")

@app.route('/comp')
def comp_login():
  return render_template("/comp.html")
# 
@app.route('/new_login')
def new_login_get():
    return render_template('new_login.html')

@app.route('/new_login',methods=["POST"])   
def new_login_post():
    name = request.form.get('user_name')
    password = request.form.get('password')
    conn = sqlite3.connect('app.db')
    c=conn.cursor()
    c.execute("INSERT INTO user VALUES(null,?,?,0)",(name,password))
    conn.commit()
    c.close()
    return redirect ('/comp')


# login

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/login',methods=["POST"])   
def login_post():
  name =request.form.get('user_name')
  password=request.form.get('password')
  conn = sqlite3.connect('app.db')
  c=conn.cursor()
  c.execute("SELECT id FROM user WHERE user_name = ? AND password = ?",(name,password))
  py_user_id=c.fetchone()
  c.close()
  if py_user_id is not None:
      session["user_id"]=py_user_id
      # /new_loginをtopに変える↓
      return redirect('/new_login')
  else:
      return redirect('/login')



















if __name__ == "__main__":

	app.run(debug=True)




