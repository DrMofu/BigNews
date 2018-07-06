from flask import redirect,url_for,g
from functools import wraps
from exts import db
from models import User
#限制登录装饰器
def login_required(func):
	@wraps(func)
	def wrapper(*args,**kwargs):
		if hasattr(g,'username'): # 用g和用session都一样
			return func(*args,**kwargs)
		else:
			print('权限限制，请先登录')
			return redirect(url_for('login'))
	return wrapper


def admin_required(func):
	@wraps(func)
	def wrapper(*args,**kwargs):
		if hasattr(g,'username'): # 第一个前提 已经登录
			user = User.query.filter(User.username == g.username).first()
			if user and (user.type == 3): # 数据存在且是管理员 才可以继续（验证user是否存在可以不用）
				return func(*args,**kwargs)
			else:
				print('权限不足')
				return redirect(url_for('index'))
		else:
			print('权限限制，请先登录')
			return redirect(url_for('login'))
	return wrapper