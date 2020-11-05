

    from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = b'random string...'

name_list = {}

@app.route('/', methods=['GET'])
def index():
   global name_list

   title ="メッセージ"
   msg = "はじめてのFlask"
   return render_template('login.html', \
           title='Messages', \
           message=msg,
           name = name_list)
   return redirect('/')

@app.route('/login' , methods=['POST'])
def login_post():
   global name_list

   id = request.form.get('id')
   pwd = request.form.get('pass')

   #idが既にあるかどうかを確認する
   if id in name_list:
       #IDとpasswordが一致しているかを確認する。
       if pwd == name_list[id]:
           #ログイン可能な状態にする
           session['flag'] = True
       #IDとpasspwrdが一致しない場合は
       else:
           session['flag'] = False
   #idの新規登録の場合
   else:
       name_list[id] = pwd
       session['flag'] = True #ログイン可能な状態にする

   session['id'] = id
   user_id = session.get("id")
   #idとpasseprdが一致するかどうかの確認
   if session['flag']: #一致した場合
       return redirect('/')
   else: #一致しなかった場合
       title = 'ログイン'
       msg = 'パスワードが間違っています'
       return render_template('login.html',\
           title = title,\
           message = msg,\
           name = name_list,\
           user_id=user_id)
   

if __name__ == '__main__':
   # app.run(debug=True)
   app.run()