import asyncio
import websockets
import time
import json

# 导入数据库操作类
from NoChatDB import NoChatDB



# 数据包类
class NoChatPacket():
	def __init__(self, data=None):
		self.code = 0
		self.msg = "ok"
		self.data = data
	
	# 生成并返回json字符串
	def dumps(self):
		_pack = {}
		_pack['code'] = self.code
		_pack['msg'] = self.msg
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
		self.users = set()             # 当前的在线用户集合
		self.output(_welcome)

	# run on self.port
	async def run(self):
		async with websockets.serve(self.handler, "", self.port):    # 回调函数self.handler处理所有的websocket请求
			self.output(f'server start ok! on port {self.port}')
			await asyncio.Future()           # run forever

	# handle an connection
	async def handler(self, websocket, path):
		self.output(path)    # 请求路径
		_pack = NoChatPacket("Welcome to NoChat!").dumps()
		await websocket.send(_pack)                        # welcome
		# login
		login = await self.login_handler(websocket)
		if login == False:
			return        # 登录包超时，断开连接
		
		# 循环接收数据
		while True:
			try:
				msg = await asyncio.wait_for(websocket.recv(), 60)       # 60s超时
			except asyncio.TimeoutError:
				self.output('Timeout close connect!', 2)
				break
			except websockets.ConnectionClosedOK:
				self.output('ConnectionClosedOK', 2)
				break
			except websockets.ConnectionClosedError:
				self.output('ConnectionClosedError', 2)
				break
			self.output(f"recv: {msg}")
			
	# 登录处理函数
	#   return False会断开连接
	async def login_handler(self, websocket):
		self.output('等待登录...', 2)
		try:
			msg = await asyncio.wait_for(websocket.recv(), 5)   # 5秒内需要发送登录包
		except asyncio.TimeoutError:
			self.output('登录包超时!', 2)
			return False
		self.output('接收到登录包', 2)
		# 处理登录包
		try:
			_pack = json.loads(msg)
			self.output(str(_pack))
		except json.decoder.JSONDecodeError:
			self.output('json解析错误', 2)
			return False
		if _pack.get('cmd') == 1 and _pack.get('data') != None:
			self.output('登陆成功', 2)
			# 验证账号密码
			_data = _pack.get('data')
			if _data.get('uname') == None or _data.get('passwd') == None:
				self.output('登录包有误', 2)
				return False
			else:
				# 获取用户输入的账号密码
				_uname = _data.get('uname')
				_passwd = _data.get('passwd')
				# ...
				self.users.add(_uname)
				# 发送确认回包
				_pack = NoChatPacket("login success").dumps()
				await websocket.send(_pack)
			# 登录成功返回uid
			# ...
			return True   
		else:
			return False
		
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
