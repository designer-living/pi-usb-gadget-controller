import asyncio
import sys


async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s+' '))
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    while True:
        message = await ainput("Enter String: ")
        if message == "\n" or message == b'':
            print('Close the connection')
            writer.close()
            await writer.wait_closed()
            break

        print(f'Send: {message!r}')
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(100)
        if data == b'':
            print('Close the connection')
            writer.close()
            await writer.wait_closed()
            break

        print(f'Received: {data.decode()!r}')


if __name__ == '__main__':
    asyncio.run(tcp_echo_client())
