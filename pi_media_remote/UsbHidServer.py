#!/usr/bin/env python3
import asyncio
import logging

from pi_media_remote.send_key import SendGadgetDevice


class UsbHidProtocol(asyncio.Protocol):

    def __init__(self, keep_usb_open=False, delimiter=ord('\n'), device='/dev/hidg0'):
        self._logger = logging.getLogger(__name__)
        self._delimiter = delimiter
        self._device = device
        self._keep_usb_open = keep_usb_open

        self._gadget_device = None
        self._transport = None
        self._received_message = ""

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        self._logger.info('Connection from {}'.format(peername))
        self._transport = transport
        self._gadget_device = SendGadgetDevice(self._device, self._keep_usb_open)


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
        if packet == '\n':
            # This is used for heartbeats so do nothing but also no need to log
            pass
        else:
            self._gadget_device.press_key(packet)

    def connection_lost(self, exc):
        self._logger.warning('Connection Lost')
        self._transport.close()
        if self._gadget_device is not None:
            self._gadget_device.close()
            self._gadget_device = None


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
