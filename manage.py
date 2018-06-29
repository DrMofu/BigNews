# -*- coding: UTF-8 -*-
# 执行各类数据库创建、数据操作等任务

from flask_script import Manager
from index import app
from flask_migrate import Migrate,MigrateCommand
from exts import db
from models import *

manager = Manager(app)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand) #添加数据迁移命令集，并命名为db

@manager.command
def runserver():
	print ("server start")

if __name__ == '__main__':
	manager.run()