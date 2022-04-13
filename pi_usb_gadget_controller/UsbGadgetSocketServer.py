#!/usr/bin/env python3
import asyncio
import logging
from os import system
from pi_usb_gadget_controller.protocols.UsbHidProtocolV1 import UsbHidProtocolV1
from pi_usb_gadget_controller.protocols.UsbHidProtocolV2 import UsbHidProtocolV2


from pi_usb_gadget_controller.send_key import SendGadgetDevice





async def start_server():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    logging.info("Starting socket server")
    loop = asyncio.get_running_loop()
    device = SendGadgetDevice('/dev/hidg0')
    server = await loop.create_server(
        lambda: UsbHidProtocolV1(device),
        '0.0.0.0', 8888, start_serving=True)
    # server = await loop.create_server(
    #     lambda: UsbHidProtocolV2(device),
    #     '0.0.0.0', 8888, start_serving=True)
    return server


async def async_main():

    server = await start_server()

    async with server:
        await server.serve_forever()


def main():
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(async_main())
