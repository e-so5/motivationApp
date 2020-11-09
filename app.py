from flask import Flask, render_template, request, redirect, session
# flaskとは違うモジュール
import sqlite3
app = Flask(__name__)
app.secret_key = "panda"

# tasklistの作成
@app.route("/tasklist")
def task_list():
	if "user_id" in session:
		py_user_id = session["user_id"][0]
		conn = sqlite3.connect("flasktest.db")
		c=conn.cursor()
		c.execute("select task,point from tasktable where user_id = ?",(py_user_id,))
		task_list = []
		for row in c.fetchall():
			task_list.append({"task":row[1],"point":row[2]})
		c.close()
		print(task_list)
		return render_template("tasklist.html",html_task_list = task_list)
	else:
		return redirect("/login")

# task追加のget通信
	@app.route("/addtask")
	def add_get():
		if "user_id" in session:
		return render_template("addpage.html")
	else:
			return redirect("/login")

# task追加のpost通信
	@app.route("/addtask",methods=["POST"])
	def add_post():
		user_id = session["user_id"][0]
		add_task = request.form.get("task")
		add_point = request.form.get("point")
		conn = sqlite3.connect("flasktest.db")
		c = conn.cursor()
		c.execute("INSERT INTO tasktable VALUES(null,?,?,?)",(add_task, add_point,   user_id))
		conn.commit()
		c.close()
		return redirect("/list")

# uselistの作成
@app.route("/uselist")
def task_list():
	if "user_id" in session:
		py_user_id = session["user_id"][0]
		conn = sqlite3.connect("flasktest.db")
		c=conn.cursor()
		c.execute("select item, point from usertable where user_id = ?",(py_user_id,))
		item_list = []
		for row in c.fetchall():
			item_list.append({"item":row[1],"point":row[2]})
		c.close()
		print(item_list)
		return render_template("uselist.html",html_item_list = item_list)
	else:
		return redirect("/login")

# uselit追加のget通信
	@app.route("/adduselist")
	def add_get():
		if "user_id" in session:
		return render_template("usepage.html")
	else:
			return redirect("/login")

# uselist追加のpost通信
	@app.route("/adduselist",methods=["POST"])
	def add_post():
		user_id = session["user_id"][0]
		add_item = request.form.get("item")
		add_point = request.form.get("point")
		conn = sqlite3.connect("flasktest.db")
		c = conn.cursor()
		c.execute("INSERT INTO tasktable VALUES(null,?,?,?)",(add_item, add_point,   user_id))
		conn.commit()
		c.close()
		return redirect("/list")

if __name__ == "__main__":
	app.run(debug=True)