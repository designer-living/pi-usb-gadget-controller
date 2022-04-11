import asyncio
import logging
import aiohttp
from aiohttp import web
from pi_media_remote.send_key import SendGadgetDevice
from pi_media_remote.html import JS_HOMEPAGE, HOMEPAGE_GET_REQUEST, WS_HOMEPAGE

logger = logging.getLogger(__name__)
gadget_device = SendGadgetDevice('/dev/hidg0')

def get_return_message(success, action):
    message = {
        'status' : 'ok',
        'message' : action
    }
    if not success:
        message['status'] = "error"
        message['message'] = action
    else:
        if action is None:
            message['message'] = f"Key not found {action}"
        else:
            message['message'] = f"Sent {action}"
    return message


def send_key(key):
    success, action = gadget_device.press_key(key)
    message = get_return_message(success, action)
    return message


async def handle(request):
    return web.Response(text=WS_HOMEPAGE,  content_type='text/html')

async def get_handler(request):
    return web.Response(text=HOMEPAGE_GET_REQUEST,  content_type='text/html')

async def js_handler(request):
    return web.Response(text=JS_HOMEPAGE,  content_type='text/html')

async def key_handler(request):
    key = request.match_info.get('key', None)
    logging.info(f"Key: {key}")
    message = send_key(key.upper())
    return web.json_response(message)

async def websocket_handler(request):
    logger.info("Websocket connection")
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                logging.info(f"Msg: {msg.data}")
                message = send_key(msg.data.upper())
                await ws.send_json(message)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            logger.error(f'ws connection closed with exception {ws.exception()}')
    logger.info('websocket connection closed')
    return ws


async def get_key_handler(request):
    key = request.match_info.get('key', None)
    logging.info(f"Key: {key}")
    message = send_key(key.upper())
    raise web.HTTPFound('/get')

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/ws', websocket_handler)
app.router.add_get('/js', js_handler)
app.router.add_get('/rest/{key}', key_handler)
app.router.add_get('/get', get_handler)
app.router.add_get('/get/{key}', get_key_handler)


def main():
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    f = loop.create_server(handler, '0.0.0.0', 8080)
    srv = loop.run_until_complete(f)
    loop.run_forever()
