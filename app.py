from flask import Flask, render_template, request, redirect, session
# データベースのimport
import sqlite3
import random

# appにFlaskを定義して使えるようにする
app = Flask(__name__)
app.secret_key = "panda"


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect("/MyPage")
    else:
        return render_template('/index.html')


@app.route('/event', methods=['POST'])
def event_post():
    # タスクリストからタスクのidを取ってくる
    id = request.form.get("task_id")
    print(id)

    # # データベースをフラグ更新する
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("UPDATE tasktable SET flag = 1 where id = ?", (id,))
    conn.commit()
    conn.close()
    return render_template('/event.html')


@app.route('/game')
def game():
    userChoice_1 = 1
    userChoice_2 = 3
    comChoice = random.randint(1, 6)
    print(comChoice)
    if userChoice_1 == comChoice or userChoice_2 == comChoice:
        return redirect("/resultwin")
    else:
        return redirect("/resultlose")


@app.route('/use', methods=['POST'])
def use():
    # タスクリストからタスクのidを取ってくる
    user_id = session['user_id'][0]
    id = request.form.get("task_id")
    print(id)
    # item_id = int(id)

    # idをキーにして、使いたい項目のポイントを取得
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT point FROM user_table where id = ?", (id,))
    point = c.fetchone()
    point = point[0]
    print(point)
    # user_idをキーにして、ユーザーの今のポイントを取得
    c.execute("SELECT point FROM user where id = ?", (user_id,))
    user_point = c.fetchone()
    user_point = user_point[0]
    print(user_point)

    if point <= user_point:
        # ポイントを更新
        updatedPoint = user_point - point
        print(updatedPoint)

    else:
        return ''' <p>ポイントが足りません</p> '''

    # データベースを更新

    c.execute("UPDATE user SET point=? where id = ?", (updatedPoint, user_id))
    conn.commit()
    conn.close()

    return redirect("/uselist")


@app.route("/pointDouble")
def pointDouble():
    user_id = session['user_id'][0]
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    # user_idをキーにして、ユーザーの今のポイントを取得
    c.execute("SELECT point FROM user where id = ?", (user_id,))
    user_point = c.fetchone()
    user_point = user_point[0]
    print(user_point)

    # user_idをキーにして、ユーザーの今のレベル管理用ポイントを取得
    # c.execute("SELECT point FROM level_table where user_id = ?", (user_id,))
    # current_level_point = c.fetchone()
    # current_level_point = current_level_point[0]

    # user_idをキーにして、ユーザーの今のレベルとレベル管理用ポイントを取得
    c.execute("SELECT level, level_point FROM user where id = ?", (user_id,))
    current_status = c.fetchone()
    current_level = current_status[0]
    current_level_point = current_status[1]
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
    c.execute("UPDATE user SET point=?, level_point=? where id = ?",
              (currentPoint, currentLevelPoint, user_id))
    c.execute("UPDATE tasktable SET flag = 0 where id = ?", (task_id,))

    # レベルテーブルを更新
    # c.execute("UPDATE level_table SET point = ? where user_id = ?",
    #           (currentLevelPoint, user_id))
    conn.commit()
    conn.close()

    # レベル管理用ポイントが200を超えるとレベルアップ！
    if currentLevelPoint >= 200:
        current_level += 1
        reset_counter = currentLevelPoint - 200

        # データベース更新
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        # c.execute("UPDATE level_table SET point=? where user_id = ?",
        #           (reset_counter, user_id))
        c.execute("UPDATE user SET level = ?, level_point=? where id = ?",
                  (current_level, reset_counter, user_id))
        conn.commit()
        conn.close()
        return render_template("levelUp.html")
    else:
        return redirect("/MyPage")


@app.route("/pointNormal")
def pointNormal():
    user_id = session['user_id'][0]
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    # user_idをキーにして、ユーザーの今のポイントを取得
    c.execute("SELECT point FROM user where id = ?", (user_id,))
    user_point = c.fetchone()
    user_point = user_point[0]
    print(user_point)

    # user_idをキーにして、ユーザーの今のレベル管理用ポイントを取得
    # c.execute("SELECT point FROM level_table where user_id = ?", (user_id,))
    # current_level_point = c.fetchone()
    # current_level_point = current_level_point[0]

    # user_idをキーにして、ユーザーの今のレベルとレベル管理用ポイントを取得
    c.execute("SELECT level, level_point FROM user where id = ?", (user_id,))
    current_status = c.fetchone()
    current_level = current_status[0]
    current_level_point = current_status[1]
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

    # ユーザーデータベースのポイントを更新
    c.execute("UPDATE user SET point=?, level_point=? where id = ?",
              (currentPoint, currentLevelPoint, user_id))
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
        # c.execute("UPDATE level_table SET point=? where user_id = ?",
        #           (reset_counter, user_id))
        c.execute("UPDATE user SET level = ?, level_point=? where id = ?",
                  (current_level, reset_counter, user_id))
        conn.commit()
        conn.close()
        return render_template("levelUp.html")
    else:
        return redirect("/MyPage")


@ app.route("/resultwin")
def resultwin():
    user_id = session['user_id']
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
    user_id = session['user_id'][0]
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    print(user_id)

    c.execute("SELECT user_name, point, level FROM user where id = ?", (user_id,))
    user_info = c.fetchone()
    user_name = user_info[0]
    user_point = user_info[1]
    user_level = user_info[2]
    print(user_id)
    print(user_info)

    conn.commit()
    conn.close()

    return render_template('MyPage.html', user_name=user_name, user_point=user_point, user_level=user_level)


@ app.route("/resultlose")
def ResultLose():
    user_id = session['user_id']
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


@ app.route("/addpage")
def addpage():
    return render_template("/addpage.html")


@ app.route("/start")
def start():
    return render_template("/start.html")


@app.route("/tasklist")
def task_list():
    if "user_id" in session:
        py_user_id = session["user_id"][0]
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute(
            "select id, task,point from tasktable where user_id = ?", (py_user_id,))
        task_list = []
        for row in c.fetchall():
            task_list.append({"id": row[0], "task": row[1], "point": row[2]})
        c.close()

        return render_template("tasklist.html", html_task_list=task_list)
    else:
        return redirect("/login")

# task追加のget通信


@app.route("/addtask")
def add_get():
    if "user_id" in session:
        return render_template("/addpage.html")
    else:
        return redirect("/login")

# task追加のpost通信


@app.route('/addtask', methods=['POST'])
def add_post():
    user_id = session["user_id"][0]
    add_task = request.form.get("task")
    add_point = request.form.get("point")
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasktable VALUES(null,?,?,?,0)",
              (add_task, add_point, user_id,))
    conn.commit()
    c.close()
    return redirect('/tasklist')

# uselistの作成


@app.route("/uselist")
def uselist():
    if "user_id" in session:
        py_user_id = session["user_id"][0]
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute(
            "select id, item, point from user_table where user_id = ?", (py_user_id,))
        item_list = []
        for row in c.fetchall():
            item_list.append({"id": row[0], "item": row[1], "point": row[2]})
        c.execute(
            "select point from user where id = ?", (py_user_id,))
        user_point = c.fetchone()
        c.close()
        print(item_list)

        return render_template("uselist.html", html_item_list=item_list, user_point=user_point)
    else:
        return redirect("/login")

# uselist追加のget通信


@app.route("/additem")
def add_item():
    if "user_id" in session:
        return render_template("/additempage.html")
    else:
        return redirect("/login")

# uselist追加のpost通信


@app.route('/additem', methods=['POST'])
def additem_post():
    user_id = session["user_id"][0]
    add_item = request.form.get("item")
    add_point = request.form.get("point")
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_table VALUES(null,?,?,?)",
              (add_item, add_point, user_id,))
    conn.commit()
    c.close()
    return redirect('/uselist')


# タスクリスト編集機能の実装
@app.route("/edittask/<int:id>")
def edit(id):
    if "user_id" in session:
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute("select id, task, point from tasktable where id = ?", (id,))
        task = c.fetchone()
        c.close
        if task is not None:
            task_id = task[0]
            user_task = task[1]
            user_point = task[2]
        else:
            return "タスクがありません"

        print(task_id)
        return render_template("task_edit.html", task_id=task_id, user_task=user_task, user_point=user_point)
    else:
        return redirect("/login")

# tasklist編集機能のpost通信


@app.route('/edittask', methods=['POST'])
def edit_post():
    taskId = request.form.get("task_id")
    taskId = int(taskId)
    task = request.form.get("task")
    point = request.form.get("point")
    point = int(point)
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("update tasktable set task=?, point = ? where id = ?",
              (task, point, taskId))
    conn.commit()
    c.close()
    return redirect('/tasklist')

# tasklistの削除機能の実装


@app.route('/deltask/<int:id>')
def task_del(id):
    if "user_id" in session:
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute("delete from tasktable where id = ?", (id,))
        conn.commit()
        c.close()
        return redirect("/tasklist")
    else:
        return redirect("/login")

# uselist編集機能の実装


@app.route("/edititem/<int:id>")
def edituselist(id):
    if "user_id" in session:
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute("select id, item, point from user_table where id = ?", (id,))
        task = c.fetchone()
        c.close
        if task is not None:
            task_id = task[0]
            user_item = task[1]
            user_point = task[2]
        else:
            return "タスクがありません"
        return render_template("use_edit.html", task_id=task_id, user_item=user_item, user_point=user_point)
    else:
        return redirect("/login")

# uselist編集機能のpost通信


@ app.route('/edititem', methods=['POST'])
def edituselist_post():
    itemId = request.form.get("task_id")
    itemId = int(itemId)
    point = request.form.get("point")
    point = int(point)
    item = request.form.get("item")
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute(
        "update user_table set item = ?, point = ? where id = ?", (item, point, itemId))
    conn.commit()
    c.close()
    return redirect('/uselist')

# uselistの削除機能の実装


@ app.route("/delitem/<int:id>")
def uselist_del(id):
    if "user_id" in session:
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute("delete from user_table where id = ?", (id,))
        conn.commit()
        c.close()
        return redirect("/uselist")
    else:
        return redirect("/login")


@ app.route('/comp')
def comp_login():
    return render_template("/comp.html")
#


@ app.route('/new_login')
def new_login_get():
    return render_template('new_login.html')


@ app.route('/TOP')
def TOP():
    return render_template('TOP.html')


@ app.route('/new_login', methods=["POST"])
def new_login_post():
    name = request.form.get('user_name')
    password = request.form.get('password')
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("INSERT INTO user VALUES(null,?,?,0,1,0)", (name, password))
    conn.commit()
    c.close()
    return redirect('/comp')


# login
@ app.route('/login', methods=["GET", "POST"])
def login_post():
    if request.method == "GET":
        if 'user_id' in session:
            return redirect("/MyPage")
        else:
            return render_template("login.html")
    else:
        name = request.form.get('user_name')
        password = request.form.get('password')
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute(
            "SELECT id FROM user WHERE user_name = ? AND password = ?", (name, password))
        py_user_id = c.fetchone()
        c.close()

        if py_user_id is not None:
            session["user_id"] = py_user_id
        # /new_loginをtopに変える↓
            return redirect('/MyPage')
        else:
            return redirect('/login')


@app.route("/logout")
def logout():
    session.pop('user_id', None)
    # ログアウト後はログインページにリダイレクトさせる
    return render_template('/TOP.html')


@ app.route('/task_edit')
def task_edit():
    return render_template("/task_edit.html")


if __name__ == "__main__":
    app.run(debug=True)
