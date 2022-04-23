import logging
import argparse
from pi_usb_gadget_controller.test_client.ReconnectingProtocol import ReconnectingProtocol
from pi_usb_gadget_controller.keys import keys
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

async def user_input(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s+' '))
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)


def process_input(user_input):
    if user_input.replace('\n') in keys.keys:
        return[user_input]
    
    processed = []
    for user_char in user_input:
        if user_char == '\n':
            continue
        if user_char.isalpha():
            processed.append(f'press|KEY_{user_char.upper()}\n' )
        elif user_char.isdigit():
            processed.append(f'press|KEY_{user_char}\n')


async def async_main(ip, port):
    logging.info(f"Running test client connecting to {ip}:{port}")
    client = MyClient(ip, port, heartbeat_time=None)
    client.connect()
    while True:
        user_input = await user_input("Input:")
        messages = process_input(user_input)
        for message in messages:
            client.send_string(message)


def main():
    parser = argparse.ArgumentParser(description="Test client to connect to the USB Gadget socket port")
    parser.add_argument("--ip", action="store", default="127.0.0.1", help="The ip of the USB Gadget server")
    parser.add_argument("--port", type=int, default=8888, action="store", help="The port to start the socket server on. NOTE if you specify a port here you also need to spcify a --web_port otherwise the web  port won't be opened")
    parser.add_argument("--logging", action="store", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO', help="The logging level to use")
    args = parser.parse_args()
    config = vars(args)

    logging.basicConfig(level=config['logging'])
    asyncio.run(async_main(
        config['ip'],
        config['port']
    ))
