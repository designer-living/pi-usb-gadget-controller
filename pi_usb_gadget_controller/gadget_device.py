from abc import ABC, abstractmethod
import logging

from pi_usb_gadget_controller import keys
from pi_usb_gadget_controller.keys import NULL_CHAR


class GadgetDevice(ABC):

    def __init__(self, device, logger, keep_usb_open=False):
        self._logger = logger
        self._keep_usb_open = keep_usb_open
        self._device = device
        self._fd = None

        if self._keep_usb_open:
            self._fd = open(self._device, 'rb+', buffering=0)

    def open(self):
        if self._keep_usb_open and self._fd is None:
            self._fd = open(self._device, 'rb+', buffering=0)

    def close(self):
        if self._fd is not None:
            self._fd.close()
            self._fd = None

    @abstractmethod
    def handle(self, message_type, message):
        """
        Ask the gadget to handle this message_type/message.
        returns True if handled or False if this gadget can't
        handle this message.
        """
        return False

    def _send_all_bytes(self, list_of_actions):
        if self._keep_usb_open:
            for b in list_of_actions:
                self._send_bytes(b, self._fd)
        else:
            with open(self._device, 'rb+') as fd:
                for b in list_of_actions:
                    self._send_bytes(b, fd)

    def _send_bytes(self, action, fd):
        if action is None:
            return
        if fd is None:
            self._logger.warning(f"No where to send {action} to")
        else:
            self._logger.debug(f"Sending as fd not None {action}")
            fd.write(action)


class KeyPressingGadgetDevice(GadgetDevice, ABC):
    """
    Base class for any Device which is like a key press - e.g. Keyboard / Consumer Control.
    This will abstract away sending the bytes.
    """
    def __init__(self, device, logger, keep_usb_open=False):
        super().__init__(device, logger, keep_usb_open)

    @abstractmethod
    def key_we_handle(self, message):
        return False

    def message_type_we_handle(self, message_type):
        return message_type == "up" or message_type == "down" or message_type == "hold" or message_type == "press"

    def handle(self, message_type, message):
        if self.message_type_we_handle(message_type):
            if self.key_we_handle(message):
                return self._handle(message_type, message)
        return False

    def _handle(self, message_type, key):
        try:
            self._logger.debug(f"{message_type} on key {key}")
            bytes_to_send = self.get_bytes_to_send(message_type, key)
            if len(bytes_to_send) > 0:
                self._send_all_bytes(bytes_to_send)
                return True, bytes_to_send
            else:
                return False, f"Key not found {key}"
        except Exception as e:
            self._logger.error(e)
            return False, str(e)

    def get_bytes_to_send(self, message_type, key):
        bytes_to_send = []
        if message_type == 'down' or message_type == 'press':
            down_bytes = self.get_key_down_bytes(key)
            if down_bytes:
                bytes_to_send.append(down_bytes)
        if message_type == 'up' or message_type == "press":
            up_bytes = bytes_to_send.append(self.get_key_up_bytes(key))
            if up_bytes:
                bytes_to_send.append(up_bytes)
        return bytes_to_send


    @abstractmethod
    def get_key_down_bytes(self, key):
        pass


    @abstractmethod
    def get_key_up_bytes(self, key):
        pass


class ConsumerControlGadgetDevice(KeyPressingGadgetDevice):

    def __init__(self, device, keep_usb_open=False):
        super().__init__(device, logging.getLogger(__name__), keep_usb_open)

    def key_we_handle(self, message):
        return (message in keys.keys_consumer_control) or (message in keys.keys_system_control)

    def get_key_down_bytes(self, key):
        press_bytes = keys.keys_system_control.get(key, None)
        if not press_bytes:
            press_bytes = keys.keys_consumer_control.get(key, None)

        if not press_bytes:
            press_bytes = keys.keys.get(key, None)
        return press_bytes

    def get_key_up_bytes(self, key):
        return keys.CONSUMER_CONTROL_RELEASE


class KeyboardGadgetDevice(KeyPressingGadgetDevice):

    def __init__(self, device, keep_usb_open=False):
        super().__init__(device, logging.getLogger(__name__), keep_usb_open)
        self.modifier_keys_down = {}
        self.keys_down = []

    def key_we_handle(self, key):
        return (key in keys.KEYBOARD_MODIFIER_KEYS) or (key in keys.keys_keyboard)

    def get_key_down_bytes(self, key):
        if key in keys.KEYBOARD_MODIFIER_KEYS:
            self.modifier_keys_down[key] = True
        else:
            self.keys_down.append(key)
        return self._get_bytes_for_message()

    def get_key_up_bytes(self, key):
        if key in keys.KEYBOARD_MODIFIER_KEYS:
            self.modifier_keys_down.pop(key, None)
        else:
            if key in self.keys_down:
                self.keys_down.remove(key)
        return self._get_bytes_for_message()

    def _get_bytes_for_message(self):
        modifier_byte = self._get_modifier_keys_bytes()
        key_press_bytes = self._get_key_press_bytes()
        return modifier_byte + NULL_CHAR + key_press_bytes

    def _get_modifier_keys_bytes(self):
        total = 0
        for key in self.modifier_keys_down:
            total = total + keys.KEYBOARD_MODIFIER_KEYS.get(key, 0)
        self._logger.info(f"Total: {total}")
        return bytes([total])

    def _get_key_press_bytes(self):
        key_bytes = bytes([])
        if len(self.keys_down) > 6:
            self._logger.warning(f"More than 6 keys pressed only taking the top 6. {self.keys_down}")
        for x in range(6):
            if len(self.keys_down) > x:
                key_bytes = key_bytes + (keys.keys_keyboard.get(self.keys_down[x], NULL_CHAR))
            else:
                key_bytes = key_bytes + (NULL_CHAR)
        return key_bytes

        
class CompositeGadgetDevice(GadgetDevice):

    def __init__(self, *devices):
        self._logger = logging.getLogger(__name__)
        self.devices = [*devices]

    def open(self):
        for device in self.devices:
            device.open()

    def close(self):
        for device in self.devices:
            device.close()

    def handle(self, message_type, message):
        for device in self.devices:
            if device.handle(message_type, message):
                return True
        return False

    def _send_bytes(self, action, fd):
        raise Exception("Can't send bytes to a composite device")
