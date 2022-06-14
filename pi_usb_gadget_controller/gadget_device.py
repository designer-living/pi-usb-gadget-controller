from abc import ABC, abstractmethod
import logging
import struct

from pi_usb_gadget_controller import keys
from pi_usb_gadget_controller.keys import NULL_CHAR

DELIMITER = '|'

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
        return (message in keys.keys_consumer_control) or \
               (message in keys.keys_system_control) or \
               (message.startswith('KEY_RAW|c')) # 0x0C is the Consumer Control page in the HID spec

    def get_key_down_bytes(self, key):
        if key.startswith("KEY_RAW"):
            split_key = key.split(DELIMITER, 2)
            # We only need the second bit.
            split_key = split_key[1]
            # Drop the first letter as that isn't sent to the connected device.
            split_key = split_key[1:]
            # Split string into string of bytes
            chunks = [split_key[i:i + 2] for i in range(0, len(split_key), 2)]
            # Reverse the list as we write the message the reverse of what we send.
            chunks.reverse()
            b = bytes()
            for chunk in chunks:
                # Convert each String hex into a byte
                b = b + bytearray.fromhex(chunk)
            return b
        else:
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


class MouseGadgetDevice(KeyPressingGadgetDevice):

    DELIMITER = '|'
    ENDIAN = 'little'

    def __init__(self, device, report_descriptor = None, keep_usb_open=False):
        super().__init__(device, logging.getLogger(__name__), keep_usb_open)
        self.report_descriptor = report_descriptor
        self.rel_report_id = bytes([0x1])
        self.abs_report_id = bytes([0x2])
        self.buttons_down = []

    def handle(self, message_type, message):
        handled = super().handle(message_type, message)
        if handled:
            return handled
        elif message_type == "abs":
            return self._handle_abs(message)
        elif message_type == "rel":
            return self._handle_rel(message)
        return False

    def key_we_handle(self, key):
        return key in keys.MOUSE_BUTTONS

    def _handle_abs(self, message):
        # TODO implement this
        split_message = message.split(self.DELIMITER)
        if len(split_message) != 2:
            self._logger.warning(f"Unexpected message: {message}")
        else:
            x_bytes = self.abs_bytes(split_message[0])
            y_bytes = self.abs_bytes(split_message[1])
            complete_report = self._get_bytes_for_message(self.abs_report_id, x_bytes, y_bytes)
            self._send_all_bytes([complete_report])
            return True
        return False

    def _handle_rel(self, message):
        split_message = message.split(self.DELIMITER)
        if len(split_message) != 2:
            self._logger.warning(f"Unexpected message: {message}")
        else:
            x_bytes = self.rel_bytes(split_message[0])
            y_bytes = self.rel_bytes(split_message[1])
            complete_report = self._get_bytes_for_message(self.rel_report_id, x_bytes, y_bytes)
            self._send_all_bytes([complete_report])
            return True
        return False

    def _get_bytes_for_message(self, report_id, x_bytes, y_bytes):
        button_press_bytes = self._get_button_press_bytes()
        complete_report = report_id + button_press_bytes + x_bytes + y_bytes + NULL_CHAR * 2
        return complete_report

    def get_key_down_bytes(self, key):
        if key not in self.buttons_down:
            self.buttons_down.append(key)
        return self._get_bytes_for_message(self.rel_report_id, NULL_CHAR, NULL_CHAR)

    def get_key_up_bytes(self, key):
        if key in self.buttons_down:
            self.buttons_down.remove(key)
        return self._get_bytes_for_message(self.rel_report_id, NULL_CHAR, NULL_CHAR)

    def _get_button_press_bytes(self):
        total = 0
        for key in self.buttons_down:
            total = total + keys.MOUSE_BUTTONS.get(key, 0)
        self._logger.info(f"Total: {total}")
        return bytes([total])

    def abs_bytes(self, value):
        return struct.pack(">B", int(value))

    def rel_bytes(self, value):
        return struct.pack(">b", int(value))


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
