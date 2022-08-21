from NoChatDB import NoChatDB
import time

# 消息类
# 用于控制消息的各种操作
class NoChatMsg():
	def __init__(self, from_uid, to_uid, text, status='unread'):
		self.from_uid = from_uid
		self.to_uid = to_uid
		self.text = text
		self.status = status
		
	def save(self):
		# 将消息存入数据库
		db = NoChatDB()
		sql = 'INSERT INTO `msg` (from_uid, to_uid, text, status, time) VALUES (?,?,?,?,?);'
		ret = db.execute(sql, 
			(self.from_uid, self.to_uid, self.text, self.status, int(time.time()))
		)
		db.close()


if __name__ == '__main__':
	# 测试
	msg = NoChatMsg(1, 2, "who are you")
	msg.save()
