import asyncio
import websockets
import time
import json

# 导入数据库操作类
from NoChatDB import NoChatDB

# 导入用户类
from NoChatUser import NoChatUser



# 数据包类
class NoChatPacket():
	def __init__(self, data=None):
		self.code = 0
		self.cmd = 5
		self.msg = "ok"
		self.data = data
	
	# 生成并返回json字符串
	# code回应包
	def code_dumps(self):
		_pack = {}
		_pack['code'] = self.code
		_pack['msg'] = self.msg
		_pack['data'] = self.data
		return json.dumps(_pack, separators=(',', ':'))
		
	# cmd包
	def cmd_dumps(self):
		_pack = {}
		_pack['cmd'] = self.cmd
		_pack['data'] = self.data
		return json.dumps(_pack, separators=(',', ':'))


# 服务器类，通过这个类启动
class NoChatServer():
	def __init__(self, port):
		# 优雅的输出一段欢迎
		_welcome = ''+'''
  _   _            _____   _               _               __  __         __ 
 | \ | |          / ____| | |             | |      ____   |  \/  |       /_ |
 |  \| |   ___   | |      | |__     __ _  | |_    / __ \  | \  / |  ____  | |
 | . ` |  / _ \  | |      | '_ \   / _` | | __|  / / _` | | |\/| | |_  /  | |
 | |\  | | (_) | | |____  | | | | | (_| | | |_  | | (_| | | |  | |  / /   | |
 |_| \_|  \___/   \_____| |_| |_|  \__,_|  \__|  \ \__,_| |_|  |_| /___|  |_|
                                                  \____/                     
'''
		self.port = port
		self.users = {}             # 当前的在线用户字典{"uid": $websocket}
		self.output(_welcome)

	# run on self.port
	async def run(self):
		async with websockets.serve(self.handler, "", self.port):    # 回调函数self.handler处理所有的websocket请求
			self.output(f'server start ok! on port {self.port}')
			await asyncio.Future()           # run forever

	# handle an connection
	async def handler(self, websocket, path):
		self.output(path)    # 请求路径(暂时没有使用)
		_pack = NoChatPacket("Welcome to NoChat!").code_dumps()
		await websocket.send(_pack)                        # welcome
		# login
		# 如果登录成功返回user对象
		_user = await self.login_handler(websocket)
		if _user == False:
			return        # 登录包超时，断开连接
		else:
			self.output(f'用户uid: {_user.uid}已上线! 当前在线用户: {len(self.users)}', 2)
			
		# 测试，向所有在线用户发送用户上线通知
		await self.boardcast(f"有新用户上线biubiu: {_user.uid}")
		
		# 循环接收数据
		while True:
			try:
				# msg = await asyncio.wait_for(websocket.recv(), 60)       # 60s超时
				msg = await websocket.recv()   # 不设超时
				await self.session_handler(websocket, msg, _user)
			except asyncio.TimeoutError:
				self.output('Timeout close connect!', 2)
				break
			except websockets.ConnectionClosedOK:
				self.output('ConnectionClosedOK', 2)
				break
			except websockets.ConnectionClosedError:
				self.output('ConnectionClosedError', 2)
				break
			self.output(f"recv: {msg}", 2)
		
		# 登出用户
		await self.logout_handler(_user)
			
			
	# 登录处理函数
	#   return False会断开连接
	#   如果登录成功返回NoChatUser对象
	async def login_handler(self, websocket):
		self.output('等待登录...', 4)
		try:
			msg = await asyncio.wait_for(websocket.recv(), 5)   # 5秒内需要发送登录包
		except asyncio.TimeoutError:
			self.output('登录包超时!', 4)
			return False
		self.output('接收到登录包', 4)
		# 处理登录包
		try:
			_pack = json.loads(msg)
			self.output(str(_pack))
		except json.decoder.JSONDecodeError:
			self.output('json解析错误', 4)
			return False
		if _pack.get('cmd') == 1 and _pack.get('data') != None:
			# 验证账号密码
			_data = _pack.get('data')
			if _data.get('uname') == None or _data.get('passwd') == None:
				self.output('登录包有误', 4)
				return False
			else:
				# 获取用户输入的账号密码
				_uname = _data.get('uname')
				_passwd = _data.get('passwd')
				_user = NoChatUser(_uname, _passwd)
				if _user.login() == True:
					if _user.uid in self.users:    # 查看用户是否已经登录
						self.output(f'用户{_user.uname}已在线上啦!', 4)
						return False
					self.output(f'登陆成功', 4)
					# 在用户字典中添加这个用户以及连接, 用于跨对话发送消息
					self.users[_user.uid] = websocket
					# 发送确认回包
					_pack = NoChatPacket("login success").code_dumps()
					await websocket.send(_pack)
				return _user 
		else:
			return False
			
	# 登出用户handler
	async def logout_handler(self, _user):
		self.users.pop(_user.uid)   # 从在线用户集合中删除
		self.output(f'用户uid:{_user.uid}-{_user.uname}退出登录, 当前在线用户: {len(self.users)}', 2)
		
	# session中会话控制
	async def session_handler(self, websocket, msg, _user):
		# 处理msg消息
		try:
			_msg = json.loads(msg)
		except json.decoder.JSONDecodeError:
			self.output(f'json解析错误{msg}', 4)
			return False
		# 提取cmd
		_cmd = _msg.get("cmd")
		_data = _msg.get("data")
		if _cmd == None:
			return False
		elif _cmd == 11:       # 发消息包
			self.output(f'收到发消息包: to:{_data.get("to_uid")}:{_data.get("text")}', 4)
			# 查看用户是否在线，如果在线则发送该消息
			if _data.get("to_uid") in self.users:
				_conn =  self.users[_data.get("to_uid")]
				_pack = NoChatPacket()
				_pack.data = {
					"type": "recvmsg", 
					"data": {
						"from_uid": _user.uid,
						"text": _data.get("text"),
					},
				}
				_pack = _pack.cmd_dumps()
				await _conn.send(_pack)    # 给用户发消息
				self.output('成功发送~', 4)
			else:
				self.output('用户现在不在线T^T', 4)
		
		
	# 广播给所有连接
	# _pack为要发送的数据包
	async def boardcast(self, _pack):
		for _uid in self.users:
			_conn = self.users[_uid]
			await _conn.send(_pack)
	
	# timer
	# 计时器
	async def timer(self):
		while True:
			self.output(f"@timer: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}, online num: {len(self.users)}.")
			await asyncio.sleep(30)
			
	# 输出函数，便于重定向输出和格式化输出
	# 重要程度越高level越小
	def output(self, s, level=0, end='\n'):
		print(' '*level + '> ' + s, end=end)


def main():
	print('> starting server...')
	
	server = NoChatServer(2333)
	
	tasks = [
		server.run(),
		server.timer(),
	]
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(asyncio.wait(tasks))
	except KeyboardInterrupt:
		for task in asyncio.Task.all_tasks():
			task.cancel()
		loop.stop()
		loop.run_forever()
	
	loop.close()


if __name__ == '__main__':
	main()
