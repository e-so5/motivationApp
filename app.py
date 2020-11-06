from flask import Flask, render_template, request, redirect, session
# flaskとは違うモジュール
import sqlite3
app = Flask(__name__)
app.secret_key = "panda"

# @app.route("/test")
# def debug():
#   return render_template("/tasklist.html")

# @app.route("/test3")
# def debug3():
#   return render_template("/uselist.html")

# @app.route("/resultwin")
# def debug2():
#   return render_template("/resultwin.html")

@app.route("/list")
def task_list():
	if "user_id" in session:
		py_user_id = session["user_id"][0]
		conn = sqlite3.connect("flasktest.db")
		c=conn.cursor()
		c.execute("select task,point from tasktable where user_id = ?",(py_user_id,))
		task_list = []
		for row in c.fetchall():
			task_list.append({"task":row[0],"point":row[1]})
		c.close()
		print(task_list)
		return render_template("tasklist.html",html_task_list = task_list)
	else:
		return redirect("/login")

if __name__ == "__main__":
	app.run(debug=True)