from NoChatDB import NoChatDB
import time

# 消息类
# 用于控制消息的各种操作
class NoChatMsg():
	def __init__(self):
		self.from_uid = None
		self.to_uid = None
		self.text = None
		self.status = None
		
	def save(self):
		# 将消息存入数据库
		pass
