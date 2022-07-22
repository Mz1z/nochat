import asyncio
import websockets
import time
import json

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
		print(_welcome)

	# run on self.port
	async def run(self):
		async with websockets.serve(self.handler, "", self.port):    # 回调函数self.handler处理所有的websocket请求
			print(f'  > server start ok! on port {self.port}')
			await asyncio.Future()           # run forever

	# handle an connection
	async def handler(self, websocket, path):
		print(path)    # 请求路径
		_pack = NoChatPacket("Welcome to NoChat!").dumps()
		await websocket.send(_pack)                        # welcome
		# login
		# ...
		
		# 循环接收
		while True:
			try:
				msg = await asyncio.wait_for(websocket.recv(), 20)             # 60s超时
			except asyncio.TimeoutError:
				print('  > Timeout close connect!')
				break
			except websockets.ConnectionClosedOK:
				print('  > ConnectionClosedOK')
				break
			except websockets.ConnectionClosedError:
				print('  > ConnectionClosedError')
				break
			print(f"recv: {msg}")
		
	# timer
	# 计时器
	async def timer(self):
		while True:
			print(f"> @timer: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
			await asyncio.sleep(30)


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
