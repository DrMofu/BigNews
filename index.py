# -*- coding: UTF-8 -*-

from flask import Flask,request,session,redirect,url_for,render_template,g
from models import *
from exts import db
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 对数据库建立，存储等操作在manage.py中进行


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