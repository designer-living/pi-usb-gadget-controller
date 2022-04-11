import asyncio
import logging
from pi_media_remote.UsbGadgetSocketServer import UsbHidProtocol
from pi_media_remote.UsbGadgetRestServer import app


async def async_main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    logging.info("Starting socket server")
    socket_server = await loop.create_server(
        lambda: UsbHidProtocol(),
        '0.0.0.0', 8888)

    logging.info("Starting web/rest/ws server")
    handler = app.make_handler()
    rest_server = await loop.create_server(handler, '0.0.0.0', 8080)

    await asyncio.Event().wait()


def main():
    asyncio.run(async_main())
