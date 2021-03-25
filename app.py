from datetime import datetime
from flask import Flask, render_template, request, redirect
# SQLデータベースの定義
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# todoというデータベースを使う
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 数字の指定はx文字以下という設定で空の項目は設定できないことにしている
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    # 期限の設定、必須の項目のみFalseの設定をする
    due = db.Column(db.DateTime, nullable=False)

# index.htmlの取得
# GETによってPOSTメソッドの取得
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # 投稿全て表示
        posts = Post.query.order_by(Post.due).all()
        return render_template('index.html', posts=posts)
    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')

        due = datetime.strptime(due, '%Y-%m-%d')
        # create.htmlで作成されたタスクを新しい投稿として受けとっている
        new_post = Post(title=title, detail=detail, due=due)

        # この2行セットでデータベースに保存することができる
        db.session.add(new_post)
        db.session.commit()

        return redirect('/')


# create.htmlの取得
@app.route('/create')
def create():
    return render_template('create.html')

# detail(詳細)
@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    return render_template('detail.html', post=post)

# update(編集)
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    # 編集ページに飛んだ時にそのまま編集ページを返す
    if request.method == 'GET':
        # 元々入力したpostの値を格納
        return render_template('update.html', post=post)
    else:
        #     updateのページ
        # 編集ページで変更した内容を各項目反映する
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')
    #     dbに反映
    db.session.commit()
    # 編集を完了した時にトップページを返す
    return redirect('/')

# delete(削除)
@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    # post(投稿)のdelete(削除)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
