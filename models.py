# -*- coding: UTF-8 -*-
from exts import db

class Test(db.Model):
	__tablename__ = 'test'
	uid = db.Column(db.Integer,primary_key=True,autoincrement=True)
	username = db.Column(db.String(16),nullable=False)
	password = db.Column(db.String(16),nullable=False)

class User(db.Model):
	__tablename__ = 'user'
	uid = db.Column(db.Integer,primary_key=True,autoincrement=True)
	type = db.Column(db.Integer,nullable=False)
	username = db.Column(db.String(16),nullable=False)
	password = db.Column(db.String(16),nullable=False)
	signtime = db.Column(db.String(32),nullable=False)
	describe = db.Column(db.String(32))
	# 可以使用 Comments(所有留言)，Tocomments（所有被回复），Likes(所有点的赞的id）


# 新闻数据表集
class News(db.Model):
	__tablename__ = 'news'
	pid = db.Column(db.Integer,primary_key=True,autoincrement=True)
	title = db.Column(db.String(255),nullable=False)
	article = db.Column(db.Text,nullable=False)
	date = db.Column(db.Text)
	type = db.Column(db.String(16),nullable=False)
	source = db.Column(db.String(16))
	author = db.Column(db.String(16))
	likes = db.Column(db.Integer,nullable=False)
	url = db.Column(db.String(255))
	picurl = db.Column(db.String(255))
	waitforcheck = db.Column(db.Integer,nullable=False)
	value = db.Column(db.Integer,nullable=False)
	# 可以使用 Comments(所有留言)，Likes(所有点的赞的id）

# 用户留言数据
class Comments(db.Model):
	__tablename__ = 'comments'
	cid = db.Column(db.Integer,primary_key=True,autoincrement=True)
	newstype = db.Column(db.String(16),nullable=False)
	newsid = db.Column(db.Integer,db.ForeignKey('news.pid'),nullable=False) # 是table名（和mysql语句有关），不是类名
	userid = db.Column(db.Integer,db.ForeignKey('user.uid'),nullable=False)
	comment = db.Column(db.String(255),nullable=False)
	time = db.Column(db.String(32),nullable=False)
	touser = db.Column(db.Integer,db.ForeignKey('user.uid'))

	# 创建类之间的关系
	# user_ = db.relationship('User',backref=db.backref('comments')) # 系统自动去User类找表名为user的UID
	# 调用user，会找到一个User类
	# backref 反向引用 使用User.comments（直接是User类），找到所有与一个User类关联的Comments类
	# 两个类相互关联，只用创一个，另一个不用创建
	# news_ = db.relationship('News',backref=db.backref('comments'))
	# touser_ = db.relationship('User',backref=db.backref('tocomments')) 

'''
# 待管理员审核文章
class WaitNews(db.Model):
	__tablename__ = 'WaitNews'
	WPID = db.Column(db.Integer,primary_key=True,autoincrement=True)
	Type = db.Column(db.String(16),nullable=False)
	Title = db.Column(db.String(255),nullable=False)
	Article = db.Column(db.Text,nullable=False)
	Date = db.Column(db.Text)
	Author = db.Column(db.String(16))
'''

# 点赞记录
class Likes(db.Model):
	__tablename__ = 'likes'
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	uid = db.Column(db.Integer,db.ForeignKey('user.uid'),nullable=False)
	pid = db.Column(db.Integer,db.ForeignKey('news.pid'),nullable=False)

	# user = db.relationship('User',backref=db.backref('likes'))
	# news = db.relationship('News',backref=db.backref('likes'))