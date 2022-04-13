import logging
from pi_usb_gadget_controller.protocols.UsbHidBaseProtocol import UsbHidBaseProtocol

class UsbHidProtocolV1(UsbHidBaseProtocol):

    def __init__(self, device, delimiter='\n'):
        super().__init__(device, logging.getLogger(__name__), delimiter)


    def _process_packet(self, packet):
        self._gadget_device.press_key(packet)