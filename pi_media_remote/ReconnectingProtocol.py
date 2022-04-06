from abc import ABC, abstractmethod
import asyncio
import logging


class ReconnectingProtocol(ABC, asyncio.Protocol):

    def __init__(self, hostname, port, reconnect_time=10, heartbeat_time=None):
        self._logger = logging.getLogger(__name__)
        self._loop = asyncio.get_event_loop()
        self._hostname = hostname
        self._port = port
        self._reconnect_time = reconnect_time
        self._connected = False
        self._keep_connected = True
        self._transport = None
        self.peer_name = ""
        self._heartbeat_time = heartbeat_time
        self._heartbeat_task = None

    def connect(self):
        self._loop.create_task(self._wait_to_reconnect())

    async def _connect(self):
        connection_coroutine = self._loop.create_connection(lambda: self, host=self._hostname, port=self._port)
        connection_task = self._loop.create_task(connection_coroutine)
        result = await asyncio.gather(connection_task, return_exceptions=True)
        if isinstance(result[0], Exception):
            self._logger.error("Error connecting: {}".format(result[0]))

    async def _wait_to_reconnect(self):
        await self._connect()
        while not self._connected and self._keep_connected:
            await asyncio.sleep(self._reconnect_time)
            await self._connect()

    def connection_made(self, transport):
        self._connected = True
        self._transport = transport
        self.peer_name = transport.get_extra_info("peername")
        self._logger.info("Connection Made: {}".format(self.peer_name))
        self.connected(transport)
        # Maybe?
        if self._heartbeat_time is not None:
            self._heartbeat_task = self._loop.create_task(self._heartbeat())

    async def _heartbeat(self):
        while True:
            await asyncio.sleep(self._heartbeat_time)
            self._logger.debug('Sending heartbeat to {}:{}'.format(self._hostname, self._port))
            self.heartbeat()

    def connected(self, transport):
        pass

    def disconnected(self, exc):
        pass

    def heartbeat(self):
        pass

    @abstractmethod
    def data_received(self, data: bytes) -> None:
        pass

    def send_string(self, message: str):
        self.send_byte_array(message.encode())

    def send_byte_array(self, message: bytes):
        if self._connected:
            self._logger.debug("send_data client: {} = {}".format(self.peer_name, message))
            self._transport.write(message)
        else:
            self._logger.warning(
                "Not connected message: {} won't be sent to: {}:{}".format(message, self._hostname, self._port))

    def set_keep_connected(self, keep_connected):
        self._keep_connected = keep_connected

    def connection_lost(self, exc):
        self._connected = False
        if self._heartbeat_task is not None:
            self._heartbeat_task.cancel()
        self._logger.error(
            "Disconnected from {} will try to reconnect in {} seconds".format(self._hostname, self._reconnect_time))
        self.disconnected(exc)

        if self._keep_connected:
            self._loop.create_task(self._wait_to_reconnect())
