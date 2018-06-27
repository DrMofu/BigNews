#encodig:utf-8

from flask import Flask,request,session,redirect,url_for,render_template
import config as config

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
	return render_template('index.html')

# user模块
'''
login --  登录+注册页
user  --  个人信息页
'''

# login 登录+注册
@app.route('/login/', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('/user/login.html')
	else:
		username = request.form.get('username')
		password = request.form.get('password')
		return redirect(url_for('user',userid=username))

# user 个人信息页
@app.route('/user/<userid>')
def user(userid):
	return userid

if __name__ == '__main__':
	app.run()