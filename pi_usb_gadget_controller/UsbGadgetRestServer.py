import asyncio
import logging
import aiohttp
from aiohttp import web
from pi_usb_gadget_controller.gadget_device import ConsumerControlGadgetDevice
from pi_usb_gadget_controller.html import JS_HOMEPAGE, HOMEPAGE_GET_REQUEST, WS_HOMEPAGE


class UsbGadgetRestServer():

    def __init__(self, device):
        self.logger = logging.getLogger(__name__)
        self.gadget_device = device
        self.app = web.Application()
        self.app.router.add_get('/', self.handle)
        self.app.router.add_get('/ws', self.websocket_handler)
        self.app.router.add_get('/js', self.js_handler)
        self.app.router.add_get('/rest/{key}', self.key_handler)
        self.app.router.add_get('/get', self.get_handler)
        self.app.router.add_get('/get/{key}', self.get_key_handler)

    def make_handler(self):
        return self.app.make_handler()
        
    def get_return_message(self,success, action):
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


    def send_key(self, key):
        success, action = self.gadget_device.handle('press', f'KEY_{key}')
        message = self.get_return_message(success, action)
        return message


    async def handle(self, request):
        return web.Response(text=WS_HOMEPAGE,  content_type='text/html')

    async def get_handler(self, request):
        return web.Response(text=HOMEPAGE_GET_REQUEST,  content_type='text/html')

    async def js_handler(self, request):
        return web.Response(text=JS_HOMEPAGE,  content_type='text/html')

    async def key_handler(self, request):
        key = request.match_info.get('key', None)
        logging.info(f"Key: {key}")
        message = self.send_key(key)
        return web.json_response(message)

    async def websocket_handler(self, request):
        self.logger.info("Websocket connection")
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    logging.info(f"Msg: {msg.data}")
                    message = self.send_key(msg.data)
                    await ws.send_json(message)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                self.logger.error(f'ws connection closed with exception {ws.exception()}')
        self.logger.info('websocket connection closed')
        return ws


    async def get_key_handler(self, request):
        key = request.match_info.get('key', None)
        logging.info(f"Key: {key}")
        message = self.send_key(key)
        raise web.HTTPFound('/get')


def main():
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    device = ConsumerControlGadgetDevice('/dev/hidg0')
    server = UsbGadgetRestServer(device)

    handler = server.make_handler()
    f = loop.create_server(handler, '0.0.0.0', 8080)
    srv = loop.run_until_complete(f)
    loop.run_forever()
