import asyncio
import logging
from pi_media_remote.UsbHidServer import start_server
from pi_media_remote.UsbHidRest import main as rest_main

def main():
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(start_server())
    rest_main()
