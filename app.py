from flask import Flask, render_template, request, redirect, session
# データベースのimport
import sqlite3
import random

# appにFlaskを定義して使えるようにする
app = Flask(__name__)


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
    userChoice = 5
    comChoice = random.randint(1, 6)
    print(comChoice)
    if userChoice == comChoice:
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

    # データベースを更新
        c.execute("UPDATE user SET point=? where id = ?",
                  (updatedPoint, user_id))
        conn.commit()
        conn.close()
    else:
        return ''' <p>ポイントが足りません</p> '''

    return render_template("/uselist.html")


@ app.route("/uselist")
def debug3():
    return render_template("/uselist.html")


@ app.route("/resultwin")
def debug2():
    return render_template("/resultwin.html")


if __name__ == "__main__":
    app.run()
