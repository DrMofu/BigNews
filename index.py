# -*- coding: UTF-8 -*-

from flask import Flask,request,session,redirect,url_for,render_template,g
from models import *
from exts import db
from crawler import *
from decorators import *
import config
import datetime

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 对数据库建立，存储等操作在manage.py中进行

@app.route('/test/')
def test():
	return render_template('test.html')

@app.route('/')
def index():
	content = {
		'newss' : News.query.order_by('-time').limit(10).all()
	}

	return render_template('index.html',**content)

# user模块
'''
login      --  登录+注册页
user       --  个人信息页
user_info  --  他人信息页
'''

# login 登录
@app.route('/login/', methods = ['GET', 'POST'])
def login():
	if hasattr(g,'username'):
		return '已处在登录状态，不可登录'
	else:
		if request.method == 'GET':
			return render_template('/user/login.html')
		else:
			username = request.form.get('username')
			password = request.form.get('password')
			user = User.query.filter(User.username == username,User.password == password).first()
			if user:
				session['username'] = user.username
				# session.permanent = True
				return redirect(url_for('index'))
			else:
				return '登录错误'
			
# register 注册
@app.route('/register/', methods = ['GET', 'POST'])
def register():
	if hasattr(g,'username'):
		return '已处在登录状态，暂停注册'
	else:
		if request.method == 'GET':
			return render_template('/user/register.html')
		else:
			username = request.form.get('username')
			password1 = request.form.get('password1')
			password2 = request.form.get('password2')

			user = User.query.filter(User.username == username).first()
			if user:
				return '该用户名已注册'
			else:
				if password1!=password2:
					return '两次密码不相符'
				else:
					nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
					user = User(type=1,username=username,password=password1,signtime=nowTime)
					db.session.add(user)
					db.session.commit()
					return 'finished'
# logout 注销
@app.route('/logout/')
def logout():
	session.clear()
	return redirect(url_for('index'))


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


# release 发布文章模块
@app.route('/release/', methods = ['GET', 'POST'])
@login_required
def release():
	if request.method == 'GET':
		return render_template('release.html')
	else:
		title = request.form.get('title')
		content = request.form.get('content')
		type = request.form.get('type')
		user = User.query.filter(User.username == g.username).first()
		news = News(title=title,article=content,type=type,source='用户发布',author=g.username,waitforcheck=0)
		news.author_user = user
		news.author_id = user.uid

		db.session.add(news)
		db.session.commit()
		return redirect(url_for('index'))



# news 具体内容页
@app.route('/news/<newsId>')
def newsPage(newsId):
	news = News.query.filter(News.pid == newsId).first()
	return render_template('news.html',news=news)


# add_comment 添加评论
@app.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():
	content = request.form.get('push_comment')
	news_id = request.form.get('news_id')
	username = g.username
	user = User.query.filter(User.username == username).first()
	news = News.query.filter(News.pid == news_id).first()
	new_comment = Comments(newsid=news_id,userid=user.uid,comment=content) 
	new_comment.user = user
	new_comment.news = news

	db.session.add(new_comment)
	db.session.commit()
	return redirect(url_for('newsPage',newsId = news_id))


# 爬虫模块
@app.route('/crawler/')
def crawler():
	return_list = crawler_36kr()
	for news in return_list:
		username = news.author
		user = create_credit_user(username) # 创建用户或查询用户
		news.author_user = user # 绑定用户与新闻
		news.author_id = user.uid
		db.session.add(news)
		db.session.commit()
	return 'finished'

# 钩子函数
# before_request 在每次request前进行处理

@app.before_request
def get_info():
	if session.get('username'):
		g.username = session['username']
		

# context_processor 对所有渲染文档，统一变量
@app.context_processor
def context_pro():
	# username = session.get('username')
	# if username:
	# 	return{'username':username}
	# return {}
	if hasattr(g,'username'):
		return{'username':g.username}
	return {}




# 默认创建一个特定用户
def create_credit_user(username, type=2, password='123456', describe='认证用户'):
	user = User.query.filter(User.username == username).first()
	if user:
		# print("%s 用户已存在" % username)
		return user
	user = User(username=username,type=type,password=password,describe=describe)
	db.session.add(user)
	db.session.commit()
	return user



if __name__ == '__main__':
	app.run()