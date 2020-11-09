from flask import Flask, render_template, request, redirect, session
# データベースのimport
import sqlite3
import random

# appにFlaskを定義して使えるようにする
app = Flask(__name__)
app.secret_key = "panda"


@app.route('/')
def index():
    return render_template('/TOP.html')


@app.route('/event')
def event_post():
    # タスクリストからタスクのidを取ってくる
    # id = request.args.get("item_id")
    # print(id)
    # item_id = int(id)

    # # # データベースをフラグ更新する
    # conn = sqlite3.connect('app.db')
    # c = conn.cursor()
    # c.execute("UPDATE tasktable SET flag = 1 where id = ?", (id,))
    # conn.commit()
    # conn.close()
    return render_template('/event.html')


@app.route('/game')
def game():
    userChoice_1 = 1
    userChoice_2 = 3
    comChoice = random.randint(1, 6)
    print(comChoice)
    if userChoice_1 == comChoice or userChoice_2 == comChoice:
        return render_template("/resultwin.html")
    else:
        return render_template("/resultlose.html")


@app.route('/use')
def use():
    # タスクリストからタスクのidを取ってくる
    user_id = 1
    # session['user_id']
    id = request.args.get("item_id")
    print(id)
    # item_id = int(id)

    # idをキーにして、使いたい項目のポイントを取得
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT point FROM user_table where id = ?", (id,))
    point = c.fetchone()
    point = point[0]
    print(point)
    # user_idをキーにして、ユーザーの今ののポイントを取得
    c.execute("SELECT point FROM user where id = ?", (user_id,))
    user_point = c.fetchone()
    user_point = user_point[0]
    print(user_point)

    if point < user_point:
        # ポイントを更新
        updatedPoint = user_point - point
        print(updatedPoint)

    else:
        return ''' <p>ポイントが足りません</p> '''

    # データベースを更新

    c.execute("UPDATE user SET point=? where id = ?", (updatedPoint, user_id))
    conn.commit()
    conn.close()

    return render_template("/uselist.html")


@app.route("/pointDouble")
def pointDouble():
    user_id = 1
    # session['user_id']
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    # user_idをキーにして、ユーザーの今のポイントを取得
    c.execute("SELECT point FROM user where id = ?", (user_id,))
    user_point = c.fetchone()
    user_point = user_point[0]
    print(user_point)

    # user_idをキーにして、ユーザーの今のレベル管理用ポイントを取得
    c.execute("SELECT point, level FROM level_table where user_id = ?", (user_id,))
    level_point = c.fetchone()
    current_level_point = level_point[0]
    current_level = level_point[1]
    print(current_level)

    # タスクテーブルからフラグ1（タスクリストで選択したタスク）のポイントを取得
    c.execute("SELECT id, point FROM tasktable where flag = 1")
    current_task = c.fetchone()
    task_id = current_task[0]
    task_point = current_task[1]
    print(task_point)
    # # 当たったのでポイント2倍
    getPoint = task_point * 2

    # 当選時のポイント算出
    currentPoint = user_point + getPoint
    print(currentPoint)

    # レベル管理用ポイントを計算
    currentLevelPoint = current_level_point + getPoint
    print(currentLevelPoint)

    # ユーザーデータベースのポイントを更新
    c.execute("UPDATE user SET point=? where id = ?", (currentPoint, user_id))
    c.execute("UPDATE tasktable SET flag = 0 where id = ?", (task_id,))

    c.execute("UPDATE level_table SET point = ? where user_id = ?",
              (currentLevelPoint, user_id))
    conn.commit()
    conn.close()

    # レベル管理用ポイントが200を超えるとレベルアップ！
    if currentLevelPoint >= 200:
        current_level += 1
        reset_counter = currentLevelPoint - 200

        # データベース更新
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute("UPDATE level_table SET point=?, level = ? where user_id = ?",
                  (reset_counter, current_level, user_id))
        conn.commit()
        conn.close()
        return render_template("levelUp.html")
    else:
        return redirect("/MyPage")


@app.route("/pointNormal")
def pointNormal():
    user_id = 1
    # session['user_id']
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    # user_idをキーにして、ユーザーの今のポイントを取得
    c.execute("SELECT point FROM user where id = ?", (user_id,))
    user_point = c.fetchone()
    user_point = user_point[0]
    print(user_point)

    # user_idをキーにして、ユーザーの今のレベル管理用ポイントを取得
    c.execute("SELECT point, level FROM level_table where user_id = ?", (user_id,))
    level_point = c.fetchone()
    current_level_point = level_point[0]
    current_level = level_point[1]
    print(current_level)

    # タスクテーブルからフラグ1（タスクリストで選択したタスク）のポイントを取得
    c.execute("SELECT id, point FROM tasktable where flag = 1")
    current_task = c.fetchone()
    task_id = current_task[0]
    task_point = current_task[1]
    print(current_task)

    # # 更新後のポイント算出
    currentPoint = user_point + task_point
    print(currentPoint)

    # レベル管理用ポイントを計算
    currentLevelPoint = current_level_point + task_point
    print(currentLevelPoint)

    # # # ユーザーデータベースのポイントを更新
    c.execute("UPDATE user SET point=? where id = ?", (currentPoint, user_id))
    c.execute("UPDATE tasktable SET flag = 0 where id = ?", (task_id,))
    conn.commit()
    conn.close()

    # レベル管理用ポイントが200を超えるとレベルアップ！
    if currentLevelPoint >= 200:
        current_level += 1
        reset_counter = currentLevelPoint - 200

        # データベース更新
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute("UPDATE level_table SET point=?, level = ? where user_id = ?",
                  (reset_counter, current_level, user_id))
        conn.commit()
        conn.close()
        return render_template("levelUp.html")
    else:
        return redirect("/MyPage")


@ app.route("/resultwin")
def resultwin():
    user_id = 1
    # session['user_id']
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    # タスクテーブルからフラグ1（タスクリストで選択したタスク）のポイントを取得
    c.execute("SELECT id, point FROM tasktable where flag = 1")
    current_task = c.fetchone()
    task_id = current_task[0]
    task_point = current_task[1]
    print(current_task)

    gotPoint = task_point * 2

    return render_template('/resultwin.html', gotPoint=gotPoint)


@ app.route("/MyPage")
def MyPage():
    user_id = 1
    # session['user_id']
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    c.execute("SELECT user_name, point FROM user where id = ?", (user_id,))
    user_info = c.fetchone()
    user_name = user_info[0]
    user_point = user_info[1]

    c.execute("SELECT level FROM level_table where id = ?", (user_id,))
    user_level = c.fetchone()

    conn.commit()
    conn.close()

    return render_template('MyPage.html', user_name=user_name, user_point=user_point, user_level=user_level)


@ app.route("/resultlose")
def ResultLose():
    user_id = 1
    # session['user_id']
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    # タスクテーブルからフラグ1（タスクリストで選択したタスク）のポイントを取得
    c.execute("SELECT id, point FROM tasktable where flag = 1")
    current_task = c.fetchone()
    task_id = current_task[0]
    task_point = current_task[1]
    print(current_task)

    return render_template("/resultlose.html", task_point=task_point)


@ app.route("/levelUp")
def levelUp():
    return render_template("/levelUp.html")


@app.errorhandler(403)
def mistake403(code):
    return render_template("/403error.html")


@app.errorhandler(404)
def notfound404(code):
    return render_template("/new_404.html")


@app.route("/tasklist")
def task_list():
    if "user_id" in session:
        py_user_id = session["user_id"][0]
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute(
            "select task,point from tasktable where user_id = ?", (py_user_id,))
        task_list = []
        for row in c.fetchall():
            task_list.append({"task": row[1], "point": row[2]})
        c.close()
        print(task_list)
        return render_template("tasklist.html", html_task_list=task_list)
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
def uselist():
    if "user_id" in session:
        py_user_id = session["user_id"][0]
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute(
            "select item, point from usertable where user_id = ?", (py_user_id,))
        item_list = []
        for row in c.fetchall():
            item_list.append({"item": row[1], "point": row[2]})
        c.close()
        print(item_list)
        return render_template("uselist.html", html_item_list=item_list)
    else:
        return redirect("/login")


@app.route("/usepage")
def usepage():
    return render_template("/usepage.html")


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
    app.run()
