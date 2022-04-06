import logging

from ReconnectingProtocol import ReconnectingProtocol
import asyncio
import sys


class MyClient(ReconnectingProtocol):

    def __init__(self, hostname, port, reconnect_time=10, heartbeat_time=None):
        super().__init__(hostname, port, reconnect_time, heartbeat_time)
        self.count = 0

    def data_received(self, data: bytes) -> None:
        print('Data received: {!r}'.format(data.decode()))

    def heartbeat(self):
        self.send_string(str(self.count))
        self.count = self.count + 1

async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s+' '))
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)



async def main():
    #a = MyClient("127.0.0.1", 8888, heartbeat_time=None)
    a = MyClient("192.168.1.126", 8888, heartbeat_time=None) # Android TV USB
    #MUTEa = MyClient("192.168.1.130", 8888, heartbeat_time=None) # Fire TV USB
    a.connect()
    while True:
        message = await ainput("Input:")
        if "keep" in message:
            a.set_keep_connected(False)
        a.send_string(message)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig()
    asyncio.run(main())
