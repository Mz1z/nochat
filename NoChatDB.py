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

# 初始化nochat需要使用的数据库	
def init_db():
	db = NoChatDB('./db/nochat.db')
	# 创建用户表
	# 主键uid自增
	db.execute(
		'CREATE TABLE `users` ('+
			'uid INTEGER PRIMARY KEY,'+
			'uname TEXT NOT NULL UNIQUE,'+
			'passwd TEXT NOT NULL,'+
			'create_time INTEGER NOT NULL'+
		')'
	)
	# 创建消息表
	db.execute(
		'CREATE TABLE `msg` ('+
			'from_uid INTEGER NOT NULL,'+
			'to_uid INTEGER NOT NULL,'+
			'time INTEGER NOT NULL'+
		')'
	)
	# 给消息表上一个索引(后期再考虑，现在先放着)
	# db.execute('CREATE INDEX index_name on table_name (column1, column2);')
	

if __name__ == '__main__':
	init_db()    
	
