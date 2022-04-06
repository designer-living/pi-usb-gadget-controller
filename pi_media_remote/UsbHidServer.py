#!/usr/bin/env python3
import asyncio
import logging

NULL_CHAR = bytes((0,))


class UsbHidProtocol(asyncio.Protocol):

    command_map = {
        "UP": bytes((66,)) + NULL_CHAR,
        "DOWN": bytes((67,)) + NULL_CHAR,
        "LEFT": bytes((68,)) + NULL_CHAR,
        "RIGHT": bytes((69,)) + NULL_CHAR,
        "SELECT": bytes((65,)) + NULL_CHAR,
        "HOME": bytes((35,)) + bytes((2,)),
        "BACK": bytes((36,)) + bytes((2,)),
        "PLAY": bytes((205,)) + NULL_CHAR,
        "MUTE": bytes((226,)) + NULL_CHAR,
        "MIC": bytes((207,)) + NULL_CHAR,
    }

    def __init__(self, keep_usb_open=False, delimiter=ord('\n'), device='/dev/hidg0'):
        self._logger = logging.getLogger(__name__)
        self._delimiter = delimiter
        self._device = device

        self._keep_usb_open = keep_usb_open

        self._fd = None
        self._transport = None
        self._received_message = ""

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        self._logger.info('Connection from {}'.format(peername))
        self._transport = transport
        if self._keep_usb_open:
            self._fd = open(self._device, 'rb+', buffering=0)

    def data_received(self, data):
        message = data.decode()
        self._logger.debug(f"Packet received: {message}")
        for letter in message:
            if ord(letter) != self._delimiter:
                self._received_message += letter
            else:
                self._process_packet(self._received_message)
                self._received_message = ''

    def _process_packet(self, packet):
        action = self.command_map.get(packet, None)
        self._logger.debug(f"Sending key {packet} : {action} ")
        if action is not None:
            self._press_key(action)
        elif packet == '\n':
            # This is used for heartbeats so do nothing but also no need to log
            pass
        else:
            self._logger.warning(f"No key mapping for command {packet}")

    def connection_lost(self, exc):
        self._logger.warning('Connection Lost')
        self._transport.close()
        if self._fd is not None:
            self._fd.close()
            self._fd = None

    def _press_key(self, key):
        if self._keep_usb_open:
            self._key_down(key, self._fd)
            self._key_release(self._fd)
        else:
            # If we find a long running connection causes an issue we can just open on each key press.
            with open(self._device, 'rb+') as fd:
                self._key_down(key, fd)
                self._key_release(fd)

    def _key_down(self, key, fd):
        self._send_key(key, fd)

    def _key_release(self, fd):
        self._send_key(NULL_CHAR*2, fd)

    def _send_key(self, key, fd):
        if fd is not None:
            self._logger.debug(f"Sending as fd not None {key}")
            fd.write(key)


async def async_main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: UsbHidProtocol(),
        '0.0.0.0', 8888)

    async with server:
        await server.serve_forever()


def main():
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(async_main())
