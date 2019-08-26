import asyncio
import json

async def tcp_echo_client(message):
	# Connect
	reader, writer = await asyncio.open_connection('127.0.0.1', 31000)
	
	# Exchange connector type
	message = json.loads((await reader.read(1024)).decode())
	if message[0] == 100:
		message = json.dumps([101, 'csengine']).encode()
	else:
		message = json.dumps([100]).encode()
	writer.write(message)

	# Close connection
	print('Closing connection')
	writer.close()
	await writer.wait_closed()

asyncio.run(tcp_echo_client('Hello, world!'))
