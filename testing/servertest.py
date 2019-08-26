import asyncio
import json

engine = None
clients = {}

async def handle_connections(reader, writer):
	# Prompt connector for what client they are
	message = json.dumps([100]).encode()
	writer.write(message)
	await writer.drain()

	message = json.loads((await reader.read(1024)).decode())
	addr = writer.get_extra_info('peername')
	print(f'Received {message!r} from {addr!r}')

	print('Close connection')
	writer.close()

async def main():
	server = await asyncio.start_server(handle_connections, '127.0.0.1', 31000)

	addr = server.sockets[0].getsockname()
	print(f'Serving on {addr!r}')

	async with server:
		await server.serve_forever()

asyncio.run(main())
