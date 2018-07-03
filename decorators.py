from flask import redirect,url_for,g
from functools import wraps

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