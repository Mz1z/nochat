from NoChatDB import NoChatDB
from NoChatMsg import NoChatMsg

# 用户类
# 用于在websocket会话中控制用户操作和行为
class NoChatUser():
	def __init__(self, uname, passwd):
		self.uname = uname
		self.passwd = passwd
		self.uid = None   # 通过self.login获取
		self.new_msg = []   # 新消息列表，登录后通过self.fetch_msg获取
		
	def login(self):
		# 登录
		# 如果登录成功则记录uid返回True，失败返回False
		db = NoChatDB()
		sql = 'SELECT uid FROM users WHERE uname=? and passwd=?;'
		ret = db.execute(sql, (self.uname, self.passwd))
		for row in ret:
			self.uid = row[0]    # 记录uid
			db.close()
			return True    # 登陆成功
		db.close()
		return False
		
	def register(self):
		# 注册
		# ...
		print('注册用户')
		
	# 返回NoChatMsg的对象的列表
	def fetch_msg(self):
		# 获取未读消息
		ret = []    # 用于返回的未读消息列表
		db = NoChatDB()
		sql = 'SELECT from_uid,to_uid,text,time from msg where to_uid=? and status=0;'
		tmp = db.execute(sql, (self.uid,))
		for row in tmp:
			tmp_msg = NoChatMsg(row[0], row[1], row[2])
			tmp_msg.time = row[3]
			ret.append(tmp_msg)
		db.close()
		return ret
		
		

# test
if __name__ == '__main__':
	user = NoChatUser('Mz2', '123456')
	ok = user.login()
	if ok == True:
		print(f'登陆成功 uid:{user.uid}')
