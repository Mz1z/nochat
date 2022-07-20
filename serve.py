import asyncio
import websockets
import time


class NoChatServer():
	def __init__(self):
		pass

	async def run(self, port):
		start_server = websockets.serve(self.handler, "", port)
		await start_server
		print(f'  > server start ok! on port {port}')
		await asyncio.Future()           # run forever

	async def handler(self, websocket, path):
		print(path)
		while True:
			try:
				msg = await websocket.recv()
			except websockets.ConnectionClosedOK:
				break
			print(f"recv: {msg}")
		print('  > close a connection')


def main():
	print('> starting server...')
	
	server = NoChatServer()
	tasks = [
		server.run(2333),
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
