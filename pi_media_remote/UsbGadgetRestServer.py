import asyncio
import logging
from aiohttp import web
from pi_media_remote.send_key import SendGadgetDevice
from pi_media_remote.html import HOMEPAGE

logger = logging.getLogger(__name__)

async def handle(request):
    return web.Response(text=HOMEPAGE,  content_type='text/html')



async def key_handler(request):
    key = request.match_info.get('key', None)
    logging.info(f"Key: {key}")
    if key is None:
        return web.Response(text=HOMEPAGE,  content_type='text/html')
    gadget_device.press_key(key.upper())
    return web.Response(text="Done")

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/{key}', key_handler)
gadget_device = SendGadgetDevice('/dev/hidg0')



def main():
    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    f = loop.create_server(handler, '0.0.0.0', 8080)
    srv = loop.run_until_complete(f)
    loop.run_forever()

    # Start up
    pass