from flask import Flask, render_template, request, redirect, session
# flaskとは違うモジュール
import sqlite3
app = Flask(__name__)

@app.route("/test")
def debug():
  return render_template("/tasklist.html")

@app.route("/test3")
def debug3():
  return render_template("/uselist.html")

@app.route("/resultwin")
def debug2():
  return render_template("/resultwin.html")

if __name__ == "__main__":
	app.run(debug=True)