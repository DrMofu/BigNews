import sqlite3

create_User = '''
create table User(
	UID INTEGER PRIMARY KEY autoincrement,
	Type int not null,
	UserName varchar(16) not null,
	PassWord varchar(16) not null,
	SignTime text not null
);'''

create_News = '''
create table News(
	PID INTEGER PRIMARY KEY autoincrement,
	Title text not null,
	Article text not null,
	Date text,
	Type varchar(16) not null,
	Source varchar(16),
	Author varchar(16),
	Likes int not null,
	URL text,
	PicURL text,
	WaitForCheck int not null,
	Value int not null
);'''

create_Comments = '''
create table Comments(
	CID INTEGER PRIMARY KEY autoincrement,
	NewsType varchar(16) not null,
	NewsId int not null,
	UserId int not null,
	Comment text not null,
	Time text not null,
	ToUser int not null
);'''

create_Likes = '''
create table Likes(
	ID INTEGER PRIMARY KEY autoincrement,
	UID int not null,
	PID it not null
);'''

conn = sqlite3.connect('bignews.db')
cursor = conn.cursor()
c = conn.cursor()
c.execute(create_User)
c.execute(create_News)
c.execute(create_Comments)
c.execute(create_Likes)
print('DataBase Created')
conn.commit()
conn.close()