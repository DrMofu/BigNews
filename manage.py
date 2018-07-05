# -*- coding: UTF-8 -*-
# 执行各类数据库创建、数据操作等任务

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from index import app
from exts import db
from models import *

manager = Manager(app)

# 绑定app与db
migrate = Migrate(app,db)

#添加数据迁移命令集，并命名为db
manager.add_command('db',MigrateCommand) 

@manager.command
def test():
	print("server start")

	
# 初始化几个系统用户
@manager.command
def init_user():
	init = [{'type':3, 'username':'Admin', 'password':'Admin', 'describe':'管理员'},
	{'type':2, 'username':'36Kr', 'password':'36Kr', 'describe':'36氪官方认证用户'},
	{'type':1, 'username':'user', 'password':'user', 'describe':'普通用户'}
	]
	for userdata in init:
		user = User.query.filter(User.username == userdata['username']).first()
		if user:
			# print("%s 用户已存在" % userdata['username'])
			continue
		user = User(**userdata)
		db.session.add(user)
		db.session.commit()
	print("finished!")


if __name__ == '__main__':
	manager.run()


