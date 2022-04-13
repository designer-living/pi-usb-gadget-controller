import logging
from pi_usb_gadget_controller.protocols.UsbHidBaseProtocol import UsbHidBaseProtocol

from pi_usb_gadget_controller.send_key import SendGadgetDevice


class UsbHidProtocolV2(UsbHidBaseProtocol):
    """
    UsbHidProtocolV2 improves on V1 by allowing press and hold. 
    It takes messages in the format: <key_state>|<key_code><delimiter>
    where key_state is: up (key released), down (key pushed), press (key was pressed and then immediatly released)
    e.g. down|UP\n will push (but not release) the UP key.
    """
    def __init__(self, device, packet_delimiter='\n'):
        super().__init__(device, logging.getLogger(__name__), packet_delimiter)
        self._message_delimiter = '|'


    def _process_packet(self, packet: str):
        splitpacket = packet.split(self._message_delimiter)
        if len(splitpacket) != 2:
            self._logger.warning(f"Unexpected message {packet}")
        else:                
            key_state = splitpacket[0]
            key_code = splitpacket[1]
            if key_state == "up":
                self._gadget_device.key_release()
            elif key_state == "down":
                self._gadget_device.key_down(key_code)
            elif key_state == "hold":
                # We don't do anything on hold let the 
                pass
            elif key_state == "press":
                self._gadget_device.press_key(key_code)
            else:
                self._logger.warning(f"Unexpected key state: {key_state} in packet: {packet}")

