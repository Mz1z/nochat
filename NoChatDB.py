import sqlite3


# 数据库类，使用sqlite3进行封装
# 如果之后要使用到别的数据库直接在这个基础上改就好了
class NoChatDB():
	def __init__(self, dbpath='./db/nochat.db'):
		self.db_conn = sqlite3.connect(dbpath)
		self.db_cursor = self.db_conn.cursor()
		
	def close(self):
		self.db_conn.close()
		
	# 返回游标
	# args为元组格式
	def execute(self, sql, args=None):
		if args == None:
			ret = self.db_cursor.execute(sql)
		else:
			ret = self.db_cursor.execute(sql, args)
		self.db_conn.commit()
		return ret
		
def init_db():
	db = NoChatDB('./db/nochat.db')
	db.execute(
		'CREATE TABLE `users` ('+
			'uname TEXT PRIMARY KEY,'+
			'passwd TEXT NOT NULL,'+
			'create_time INT NOT NULL'+
		')'
	)
	

if __name__ == '__main__':
	init_db()    # 初始化nochat需要使用的数据库
	
