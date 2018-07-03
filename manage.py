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
	print ("server start")


# 默认创建一个特定用户
def create_user():
	return 0
	
# 初始化几个系统用户
def init_user():
	pass


if __name__ == '__main__':
	manager.run()


