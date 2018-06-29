def createDB(db):
	# 数据库模型
	# 用户信息数据
	class User(db.Model):
		__tablename__ = 'User'
		UID = db.Column(db.Integer,primary_key=True,autoincrement=True)
		Type = db.Column(db.Integer,nullable=False)
		UserName = db.Column(db.String(16),nullable=False)
		Password = db.Column(db.String(16),nullable=False)
		SignTime = db.Column(db.String(32),nullable=False)

	# 新闻数据表集
	class News_Game(db.Model):
		__tablename__ = 'News_Game'
		PID = db.Column(db.Integer,primary_key=True,autoincrement=True)
		Title = db.Column(db.String(255),nullable=False)
		Article = db.Column(db.Text,nullable=False)
		Date = db.Column(db.Text)
		Source = db.Column(db.String(16))
		Author = db.Column(db.String(16))
		Likes = db.Column(db.Integer,nullable=False)
		Value = db.Column(db.Integer,nullable=False)

	# 用户留言数据
	class Comments(db.Model):
		__tablename__ = 'Comments'
		CID = db.Column(db.Integer,primary_key=True,autoincrement=True)
		NewsType = db.Column(db.String(16),nullable=False)
		NewsId = db.Column(db.Integer,nullable=False)
		UserId = db.Column(db.Integer,nullable=False)
		Comment = db.Column(db.String(255),nullable=False)
		Time = db.Column(db.String(32),nullable=False)
		ToUser = db.Column(db.Integer)

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
		UID = db.Column(db.Integer,nullable=False)
		PID = db.Column(db.Integer,nullable=False)
