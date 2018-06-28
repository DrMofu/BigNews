# -*- coding: UTF-8 -*-

from flask import Flask,request,session,redirect,url_for,render_template,g
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


# 数据库模型
# 用户信息数据
class User(db.Model):
	__tablename__ = 'User'
	UID = db.Column(db.Integer,primary_key=True,autoincrement=True)
	Type = db.Column(db.Integer,nullable=False)
	UserName = db.Column(db.String(16),nullable=False)
	Password = db.Column(db.String(16),nullable=False)
	SignTime = db.Column(db.String(32),nullable=False)

# 新闻数据表集
class News_Game(db.Model):
	__tablename__ = 'News_Game'
	PID = db.Column(db.Integer,primary_key=True,autoincrement=True)
	Title = db.Column(db.String(255),nullable=False)
	Article = db.Column(db.Text,nullable=False)
	Date = db.Column(db.Text)
	Source = db.Column(db.String(16))
	Author = db.Column(db.String(16))
	Likes = db.Column(db.Integer,nullable=False)
	Value = db.Column(db.Integer,nullable=False)

# 用户留言数据
class Comments(db.Model):
	__tablename__ = 'Comments'
	CID = db.Column(db.Integer,primary_key=True,autoincrement=True)
	NewsType = db.Column(db.String(16),nullable=False)
	NewsId = db.Column(db.Integer,nullable=False)
	UserId = db.Column(db.Integer,nullable=False)
	Comment = db.Column(db.String(255),nullable=False)
	Time = db.Column(db.String(32),nullable=False)
	ToUser = db.Column(db.Integer)

# 待管理员审核文章
class WaitNews(db.Model):
	__tablename__ = 'WaitNews'
	WPID = db.Column(db.Integer,primary_key=True,autoincrement=True)
	Type = db.Column(db.String(16),nullable=False)
	Title = db.Column(db.String(255),nullable=False)
	Article = db.Column(db.Text,nullable=False)
	Date = db.Column(db.Text)
	Author = db.Column(db.String(16))

# 点赞记录
class Likes(db.Model):
	__tablename__ = 'Likes'
	ID = db.Column(db.Integer,primary_key=True,autoincrement=True)
	UID = db.Column(db.Integer,nullable=False)
	PID = db.Column(db.Integer,nullable=False)

db.create_all()

@app.route('/')
def index():
	return render_template('index.html')

# user模块
'''
login      --  登录+注册页
user       --  个人信息页
user_info  --  他人信息页
'''

# login 登录+注册
@app.route('/login/', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('/user/login.html')
	else:
		username = request.form.get('username')
		password = request.form.get('password')
		session['username'] = username
		return redirect(url_for('user'))

# user 个人信息页
@app.route('/user/')
def user():
	if hasattr(g,'username'):
		return g.username
	else:
		return redirect(url_for('login'))

# user_info 他人信息页
@app.route('/user/<userid>')
def user_info(userid):
	return userid

# 钩子函数
# before_request 在每次request前进行处理

@app.before_request
def get_info():
	if session.get('username'):
		g.username = session['username']

'''
# context_processor 对所有渲染文档，统一变量
@app.context_processor
def context_pro():
	if session.get('username'):
		return {'username':session.get('username')}
'''

if __name__ == '__main__':
	app.run()