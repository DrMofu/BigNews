# -*- coding: UTF-8 -*-
from exts import db

class User(db.Model):
	__tablename__ = 'User'
	UID = db.Column(db.Integer,primary_key=True,autoincrement=True)
	Type = db.Column(db.Integer,nullable=False)
	UserName = db.Column(db.String(16),nullable=False)
	Password = db.Column(db.String(16),nullable=False)
	SignTime = db.Column(db.String(32),nullable=False)
	# 可以使用 Comments(所有留言)，Tocomments（所有被回复），Likes(所有点的赞的id）

# 新闻数据表集
class News(db.Model):
	__tablename__ = 'News'
	PID = db.Column(db.Integer,primary_key=True,autoincrement=True)
	Title = db.Column(db.String(255),nullable=False)
	Article = db.Column(db.Text,nullable=False)
	Date = db.Column(db.Text)
	Type = db.Column(db.String(16),nullable=False)
	Source = db.Column(db.String(16))
	Author = db.Column(db.String(16))
	Likes = db.Column(db.Integer,nullable=False)
	Value = db.Column(db.Integer,nullable=False)
	# 可以使用 Comments(所有留言)，Likes(所有点的赞的id）

# 用户留言数据
class Comments(db.Model):
	__tablename__ = 'Comments'
	CID = db.Column(db.Integer,primary_key=True,autoincrement=True)
	NewsType = db.Column(db.String(16),nullable=False)
	NewsId = db.Column(db.Integer,db.ForeignKey('News.PID'),nullable=False) # 是table名（和mysql语句有关），不是类名
	UserId = db.Column(db.Integer,db.ForeignKey('User.UID'),nullable=False)
	Comment = db.Column(db.String(255),nullable=False)
	Time = db.Column(db.String(32),nullable=False)
	ToUser = db.Column(db.Integer,db.ForeignKey('User.UID'))

	# 创建类之间的关系
	user = db.relationship('User',backref=db.backref('Comments')) # 系统自动去User类找表名为User的UID
	# 调用user，会找到一个User类
	# backref 反向引用 使用User.comments（直接是User类），找到所有与一个User类关联的Comments类
	# 两个类相互关联，只用创一个，另一个不用创建
	news = db.relationship('News',backref=db.backref('Comments'))
	touser = db.relationship('User',backref=db.backref('Tocomments')) 

# 待管理员审核文章
class WaitNews(db.Model):
	__tablename__ = 'WaitNews'
	WPID = db.Column(db.Integer,primary_key=True,autoincrement=True)
	Type = db.Column(db.String(16),nullable=False)
	Title = db.Column(db.String(255),nullable=False)
	Article = db.Column(db.Text,nullable=False)
	Date = db.Column(db.Text)
	Author = db.Column(db.String(16))

# 点赞记录
class Likes(db.Model):
	__tablename__ = 'Likes'
	ID = db.Column(db.Integer,primary_key=True,autoincrement=True)
	UID = db.Column(db.Integer,db.ForeignKey('User.UID'),nullable=False)
	PID = db.Column(db.Integer,db.ForeignKey('News.PID'),nullable=False)

	user = db.relationship('User',backref=db.backref('Likes'))
	news = db.relationship('News',backref=db.backref('Likes'))