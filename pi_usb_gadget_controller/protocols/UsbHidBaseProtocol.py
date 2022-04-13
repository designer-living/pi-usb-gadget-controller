#!/usr/bin/env python3
from abc import ABC, abstractmethod
import asyncio

from pi_usb_gadget_controller.send_key import SendGadgetDevice


class UsbHidBaseProtocol(ABC, asyncio.Protocol):

    def __init__(self, device, logger, delimiter=ord('\n'), heartbeat=''):
        self._logger = logger
        self._delimiter = delimiter
        self._heartbeat = heartbeat

        self._gadget_device: SendGadgetDevice = device
        self._transport = None
        self._received_message = ""

    def connection_made(self, transport):
        try:
            peername = transport.get_extra_info('peername')
            self._logger.info('Connection from {}'.format(peername))
            self._transport = transport
            self._gadget_device.open()
        except Exception as e:
            self._logger.error(e)
            exit(-1)


    def data_received(self, data):
        self._logger.debug(f"Packet received: {data}")
        message = data.decode()
        self._logger.debug(f"Decoded Packet: {message}")
        for letter in message:
            if ord(letter) != self._delimiter:
                self._received_message += letter
            else:
                self._process_packet_for_heartbeat(self._received_message)
                self._received_message = ''

    def _process_packet_for_heartbeat(self, packet):
        if packet == self._heartbeat:
            self._logger.debug("HEARTBEAT")
            # This is used for heartbeats so do nothing but also no need to log
            pass
        else:
            self._process_packet(packet)

    @abstractmethod
    def _process_packet(self):
        pass

    def connection_lost(self, exc):
        self._logger.warning('Connection Lost')
        self._transport.close()
        self._gadget_device.close()