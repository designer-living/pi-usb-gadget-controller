import asyncio
import logging
from pi_media_remote.UsbHidServer import start_server
from pi_media_remote.UsbHidRest import main as rest_main

async def async_main():
    server = await start_server()
    await server.start_serving()


    # async with server:
    #     await server.serve_forever()

    

def main():
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(async_main())
    rest_main()
