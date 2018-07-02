import sqlite3

def get_conn():
	return sqlite3.connect('bignews.db')

class User(object):
	def __init__(self,Type,UserName,PassWord,SignTime):
		self.Type = Type
		self.UserName = UserName
		self.PassWord = PassWord
		self.SignTime = SignTime

	def INSERT(self):
		sql = "INSERT INTO User (Type,UserName,PassWord,SignTime)\
			VALUES(?,?,?,?)"
		conn = get_conn()
		cursor = conn.cursor()
		cursor.execute(sql,(self.Type,self.UserName,self.PassWord,self.SignTime))
		conn.commit()
		conn.close()