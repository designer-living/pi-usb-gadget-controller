import argparse
import asyncio
import logging
import os.path
from pi_usb_gadget_controller.UsbGadgetRestServer import UsbGadgetRestServer
from pi_usb_gadget_controller.protocols.UsbHidProtocolV2 import UsbHidProtocolV2
from pi_usb_gadget_controller.send_key import SendGadgetDevice


async def async_main(socket_port, web_port, device):
    # Get a reference to the event loop as we plan to use
    # low-level APIs.

    logging.info(f"Using device: {device}")
    if not os.path.exists(device):
        logging.error(f"{device} doesn't exist or you don't have permissions to access it")
        exit(-1)
    else:
        logging.info(f"Confirmed {device} exists")

    if socket_port is None and web_port is None:
        socket_port = 8888
        web_port = 8080

    loop = asyncio.get_running_loop()

    if socket_port is not None:
        logging.info(f"Starting socket server on {socket_port}")
        socket_server = await loop.create_server(
            lambda: UsbHidProtocolV2(device=SendGadgetDevice(device)),
            '0.0.0.0', socket_port)

    if web_port is not None:
        logging.info(f"Starting web/rest/ws server on {web_port}")
        app = UsbGadgetRestServer(device=SendGadgetDevice(device))
        handler = app.make_handler()
        rest_server = await loop.create_server(handler, '0.0.0.0', web_port)

    await asyncio.Event().wait()


def main():
    parser = argparse.ArgumentParser(description="Send commands to a USB Gadget")
    parser.add_argument("--device", action="store", help="The USB Gadget device. DEFAULTS to /dev/hidg0", default='/dev/hidg0')
    parser.add_argument("--web_port", type=int, action="store", help="The port to start the web_port on. DEFAULTS to 8080. NOTE if you specify a port here you also need to spcify a --socket_port otherwise the socket port won't be opened")
    parser.add_argument("--socket_port", type=int, action="store", help="The port to start the socket server on. DEFAULTS to 8888. NOTE if you specify a port here you also need to spcify a --web_port otherwise the web  port won't be opened")
    parser.add_argument("--logging", action="store", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO', help="The logging level to use. DEFAULTS to INFO")
    args = parser.parse_args()
    config = vars(args)

    logging.basicConfig(level=config['logging'])
    asyncio.run(async_main(
        config['socket_port'],
        config['web_port'],
        config['device']
    ))
