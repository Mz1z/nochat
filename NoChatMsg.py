from NoChatDB import NoChatDB
import time
import json


# 消息类
# 用于控制消息的各种操作
class NoChatMsg():
	def __init__(self, from_uid, to_uid, text, status=0):
		self.from_uid = from_uid
		self.to_uid = to_uid
		self.text = text
		self.status = status
		self.time = None
		
	def save(self):
		# 将消息存入数据库
		db = NoChatDB()
		sql = 'INSERT INTO `msg` (from_uid, to_uid, text, status, time) VALUES (?,?,?,?,?);'
		ret = db.execute(sql, 
			(self.from_uid, self.to_uid, self.text, self.status, int(time.time()))
		)
		db.close()
		
	def dump2dict(self):
		# 将消息转化为dict,方便之后的序列化
		_pack = {}
		_pack['from_uid'] = self.from_uid
		_pack['to_uid'] = self.to_uid
		_pack['text'] = self.text
		_pack['status'] = self.status
		_pack['time'] = self.time
		return _pack


if __name__ == '__main__':
	# 测试
	msg = NoChatMsg(1, 2, "who are you")
	msg.save()
