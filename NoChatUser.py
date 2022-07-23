from NoChatDB import NoChatDB

# 用户类
# 用于在websocket会话中控制用户操作和行为
class NoChatUser():
	def __init__(self, uname, passwd):
		self.uname = uname
		self.passwd = passwd
		
	def login(self):
		# 登录
		# 如果登录成功则记录uid返回True，失败返回False
		db = NoChatDB()
		sql = 'SELECT uid FROM users WHERE uname=? and passwd=?;'
		ret = db.execute(sql, (self.uname, self.passwd))
		for row in ret:
			self.uid = row[0]
			db.close()
			return True    # 登陆成功
		db.close()
		return False
		

# test
if __name__ == '__main__':
	user = NoChatUser('Mz1', '123456')
	ok = user.login()
	if ok == True:
		print(f'登陆成功 uid:{user.uid}')
