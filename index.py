# -*- coding: UTF-8 -*-

from flask import Flask,request,session,redirect,url_for,render_template,g,flash
from models import *
from exts import db
from crawl import *
from decorators import *
import config
import datetime
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 对数据库建立，存储等操作在manage.py中进行

# 校验注册过程
def validateRegister(username,password1,password2):
	user=User.query.filter(User.username==username).first()
	if username=='':
		return(u'请输入用户名')
	else:
		if user:
			return(u'用户名已存在')
		else:
			if len(username)<4 or len(username)>16:
				return(u'用户名长度应为4-16字符')
			elif len(password1)<6 or len(password1)>12:
				return(u'密码长度应为6-12字符')
			elif password1 != password2:
				return(u'两次密码不一致')
			else:
				return('SUCCESS')

@app.route('/test/')
def test():
	return render_template('test.html')

# 主页面
@app.route('/')
def index():
	content = {
		'newss' : News.query.filter(News.waitforcheck > 0).order_by('-time').limit(20).all()
	}
	for item in content['newss']:
		if len(item.article)>100:
			item.article=item.article[:100]+'...'
			item.article = item.article.replace('</br>','').replace('　','').replace('<br/>','')

	return render_template('index.html',**content)

# 分类页面
@app.route('/catalogue/<kind>')
def catalogue(kind):
	content = {
		'newss' : News.query.filter(News.waitforcheck > 0, News.type == kind).order_by('-time').limit(20).all()
	}
	for item in content['newss']:
		if len(item.article)>100:
			item.article=item.article[:100]+'...'
			item.article = item.article.replace('</br>','').replace('　','').replace('<br/>','')
	return render_template('catalogue.html',**content)

# user模块
'''
login      --  登录
register   --  注册
logout     --  登出
user       --  个人信息页
user_info  --  他人信息页
'''
 
# login 登录
@app.route('/login/', methods = ['GET', 'POST'])
def login():
	if hasattr(g,'username'):
		return redirect(url_for('index'))
	else:
		if request.method == 'GET':
			return render_template('/user/login.html')
		else:
			username = request.form.get('username')
			password = request.form.get('password')
			user = User.query.filter(User.username == username,User.password == password).first()
			if user:
				session['username'] = user.username
				session['uid'] = user.uid
				session['utype']=user.type
				# session.permanent = True
				return redirect(url_for('index'))
			else:
				flash(u'用户名或密码错误')
				return redirect(url_for('login'))
			
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

			message=validateRegister(username,password1,password2)
			if message=='SUCCESS':
				nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
				user = User(type=1,username=username,password=password1,signtime=nowTime)
				db.session.add(user)
				db.session.commit()
				return redirect(url_for('login'))
			else:
				flash(message)
				return redirect(url_for('register'))

			# user = User.query.filter(User.username == username).first()
			# if user:
			# 	return '该用户名已注册'
			# else:
			# 	if password1!=password2:
			# 		return '两次密码不相符'
			# 	else:
			# 		nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
			# 		user = User(type=1,username=username,password=password1,signtime=nowTime)
			# 		db.session.add(user)
			# 		db.session.commit()
			# 		return redirect(url_for('login'))

# logout 注销
@app.route('/logout/')
def logout():
	session.clear()
	return redirect(url_for('index'))


# user 个人信息页
@app.route('/user/')
@login_required
def user():
	user = User.query.filter(User.username==g.username).first()
	news_num = 0
	news_num_wait = 0
	for news in user.news:
		if news.waitforcheck>0:
			news_num += 1
		elif news.waitforcheck == 0:
			news_num_wait += 1
	for like in user.likes:
		like.news.article = like.news.article.replace('</br>','').replace('　','').replace('<br/>','')
	for news in user.news:
	 	news.article = news.article.replace('</br>','').replace('　','').replace('<br/>','')
	inputDict = {
		'user':user,
		'news_num':news_num,
		'news_num_wait':news_num_wait
	}

	return render_template('/user/info.html',**inputDict)

# user_info 他人信息页
@app.route('/user/<username>')
def user_info(username):
	user = User.query.filter(User.username==username).first()
	if user:
		news_num = 0
		news_num_wait = 0
		for news in user.news:
			if news.waitforcheck>0:
				news_num += 1
			elif news.waitforcheck == 0:
				news_num_wait += 1
		for like in user.likes:
			like.news.article = like.news.article.replace('</br>','').replace('　','').replace('<br/>','')
		for news in user.news:
	 		news.article = news.article.replace('</br>','').replace('　','').replace('<br/>','')
		inputDict = {
			'user':user,
			'news_num':news_num,
			'news_num_wait':news_num_wait
		}

		return render_template('/user/info.html',**inputDict)
	else:
		return render_template('404.html')


# 新闻模块
'''
release      --  发布文章
newsPage     --  新闻页面
news_confirm --  新闻审核
add_comment  --  用户添加评论
change_like  --  用户点赞
'''

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

		pic=request.files['pic']
		picurl=None
		if pic:
			basepath=os.path.abspath(os.path.dirname(__file__))
			upload_path=os.path.join(basepath,'static/images/news',secure_filename(pic.filename))
			pic.save(upload_path)
			picurl=os.path.join('images/news',secure_filename(pic.filename))

		user = User.query.filter(User.username == g.username).first()
		news = News(title=title,article=content,type=type,source='用户发布',picurl=picurl,author=g.username,waitforcheck=0)
		news.author_user = user
		news.author_id = user.uid

		db.session.add(news)
		db.session.commit()
		return redirect(url_for('index'))



# news 具体内容页
@app.route('/news/<newsId>')
def newsPage(newsId):
	news = News.query.filter(News.pid == newsId).first()
	if news:
		likes = None
		if hasattr(g,'uid'):
			likes = Likes.query.filter(Likes.pid==news.pid,Likes.uid==g.uid).first()

		return render_template('news.html',news=news,likes=likes)
	else:
		return render_template('404.html')

# news_confirm 新闻审核
@app.route('/confirm/')
@admin_required
def news_confirm():
	news = News.query.filter(News.waitforcheck == 0).order_by('-time').limit(8).all()
	news_lenth = len(news)
	content = {
		'newss' : news,
		'news_lenth' : news_lenth
	}

	return render_template('confirm.html',**content)

@app.route('/confirm/upgrade/', methods=['POST'])
@admin_required
def confirm_upgrade():
	news_id = request.form.get('news_id')
	result = request.form.get('result')
	news = News.query.filter(News.pid == news_id).first()
	if result == 'yes':
		news.waitforcheck=2 # 管理员审核通过
	else:
		news.waitforcheck=-1 # 管理员审核不通过
	db.session.commit()
	return redirect(url_for('news_confirm'))



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

@app.route('/change_like/',methods=['POST'])
@login_required
def change_like():	
	news_id = request.form.get('news_id')
	username = g.username
	user = User.query.filter(User.username == username).first()
	news = News.query.filter(News.pid == news_id).first()
	uid = user.uid
	pid = news.pid
	like = Likes.query.filter(Likes.uid==uid,Likes.pid==pid).first()
	if like:#删除
		db.session.delete(like)
		news.likes -= 1
	else:
		like = Likes(uid=uid,pid=pid)
		like.user = user
		like.news = news
		db.session.add(like)
		news.likes += 1
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


# @app.route('/crawler_toutiao/')
# def crawler_toutiao():
# 	return_list = crawler_news.get_toutiao()
# 	for item in return_list:
# 		print(item['time'])
# 		news = News.query.filter(News.title == item['title']).first()
# 		if news:
# 			print('已经存在')
# 			continue
# 		news = News(title=item['title'],article=item['article'],time=item['time'],\
# 			type=item['type'],source=item['source'],author=item['author'],\
# 			waitforcheck=1,url=item['url'],picurl=item['img'])
# 		username = news.author
# 		user = create_credit_user(username) # 创建用户或查询用户
# 		news.author_user = user # 绑定用户与新闻
# 		news.author_id = user.uid
# 		db.session.add(news)
# 		db.session.commit()
	
# 	return 'finished'

# 钩子函数
# before_request 在每次request前进行处理

@app.before_request
def get_info():
	if session.get('username'):
		g.username = session['username']
	if session.get('uid'):
		g.uid = session['uid']	
	if session.get('utype'):
		g.utype=session['utype']

# context_processor 对所有渲染文档，统一变量
@app.context_processor
def context_pro():
	# username = session.get('username')
	# if username:
	# 	return{'username':username}
	# return {}
	if hasattr(g,'username') and hasattr(g,'utype'):
		return{'username':g.username,'utype':g.utype}
	elif hasattr(g,'username') :
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

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

if __name__ == '__main__':
	app.run()