# -*- coding: UTF-8 -*-
# 执行各类数据库创建、数据操作等任务

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from index import app
from exts import db
from models import *
import crawler.run as crawler_news

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

@manager.command
def crawler():
	crawler_news.run_crawl()
	# return_list = crawler_news.get_toutiao()
	# for item in return_list:
	# 	print(item['time'])
	# 	news = News.query.filter(News.title == item['title']).first()
	# 	if news:
	# 		print('已经存在')
	# 		continue
	# 	news = News(title=item['title'],article=item['article'],time=item['time'],\
	# 		type=item['type'],source=item['source'],author=item['author'],\
	# 		waitforcheck=1,url=item['url'],picurl=item['img'])
	# 	username = news.author
	# 	user = create_credit_user(username) # 创建用户或查询用户
	# 	news.author_user = user # 绑定用户与新闻
	# 	news.author_id = user.uid
	# 	db.session.add(news)
	# 	db.session.commit()
	# crawler_news.delete_database()
if __name__ == '__main__':
	manager.run()


