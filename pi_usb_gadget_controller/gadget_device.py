from abc import ABC, abstractmethod
import logging

from pi_usb_gadget_controller import keys


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
    def get_bytes_for_key(self, key):
        pass

    def _get_bytes_to_send(self, key):
        action, release = self.get_bytes_for_key(key)
    
        if action is None:
            self._logger.warning(f"Key not found {key}")
        else:
            self._logger.debug(f"Found key {key} : {action} : {release}")

        return action, release

    def press_key(self, key):
        try: 
            self._logger.debug(f"Pressing key {key}")
            action, release = self._get_bytes_to_send(key)
            if not action is None:
                if self._keep_usb_open:
                    self._send_key(action, self._fd)
                    self._send_key(release, self._fd)
                else:
                    # If we find a long running connection causes an issue we can just open on each key press.
                    with open(self._device, 'rb+') as fd:
                        self._send_key(action, fd)
                        self._send_key(release, fd)
                return True, action
            else:
                return False, f"Key not found {key}"
        except Exception as e:
            self._logger.error(e)
            return False, str(e)

    def key_down(self, key):
        try: 
            self._logger.debug(f"Key Down {key}")
            action, _ = self._get_bytes_to_send(key)
            if not action is None:
                if self._keep_usb_open:
                    self._send_key(action, self._fd)
                else:
                    # If we find a long running connection causes an issue we can just open on each key press.
                    with open(self._device, 'rb+') as fd:
                        self._send_key(action, fd)
                return action
            else:
                return False, f"Key not found {key}"
        except Exception as e:
            self._logger.error(e)
            return False, str(e)

    def key_release(self, key):
        try: 
            self._logger.debug(f"Releasing {key}")
            _, release = self._get_bytes_to_send(key)
            if not release is None:
                if self._keep_usb_open:
                    self._send_key(release, self._fd)
                else:
                    # If we find a long running connection causes an issue we can just open on each key press.
                    with open(self._device, 'rb+') as fd:
                        self._send_key(release, fd)
                return True, "Success"
        except Exception as e:
            self._logger.error(e)
            return False, str(e)

    def _send_key(self, action, fd):
        if action is None:
            return
        if fd is None:
            self._logger.warning(f"No where to send {action} to")
        else:
            self._logger.debug(f"Sending as fd not None {action}")
            fd.write(action)

class ConsumerControlGadgetDevice(GadgetDevice):

    def __init__(self, device, keep_usb_open=False):
        super().__init__(device, logging.getLogger(__name__), keep_usb_open)

    def get_bytes_for_key(self, key):
        press_bytes = keys.keys_system_control.get(key, None)
        if not press_bytes:
            press_bytes = keys.keys_consumer_control.get(key, None)

        if not press_bytes:
            press_bytes = keys.keys.get(key, None)

        return press_bytes, keys.CONSUMER_CONTROL_RELEASE


class KeyboardGadgetDevice(GadgetDevice):
    # TODO rewrite this to remember state.

    def __init__(self, device, keep_usb_open=False):
        super().__init__(device, logging.getLogger(__name__), keep_usb_open)
        self.KEY_LEFTCTRL = False
        self.KEY_LEFTSHIFT = False
        self.KEY_LEFTALT = False
        self.KEY_LEFTMETA = False
        self.KEY_RIGHTCTRL = False
        self.KEY_RIGHTSHIFT = False
        self.KEY_RIGHTALT = False
        self.KEY_RIGHTMETA = False

    def _set_key(self, key, value):
        self._logger.info(f"Set key {key}-{value}")
        if key == 'KEY_LEFTCTRL':
            self.KEY_LEFTCTRL = value
        if key == 'KEY_LEFTSHIFT':
            self.KEY_LEFTSHIFT = value
        if key == 'KEY_LEFTALT':
            self.KEY_LEFTALT = value
        if key == 'KEY_LEFTMETA':
            self.KEY_LEFTMETA = value
        if key == 'KEY_RIGHTCTRL':
            self.KEY_RIGHTCTRL = value
        if key == 'KEY_RIGHTSHIFT':
            self.KEY_RIGHTSHIFT = value
        if key == 'KEY_RIGHTALT':
            self.KEY_RIGHTALT = value
        if key == 'KEY_RIGHTMETA':
            self.KEY_RIGHTMETA = value

    def key_down(self, key):
        self._logger.info("Key Down")
        self._set_key(key, True)
        return super().key_down(key)

    def key_release(self, key):
        self._logger.info("Key Release")
        self._set_key(key, False)
        return super().key_release(key)


    def get_bytes_for_key(self, key):
        # TODO handle shift, etc
        modifier_byte = self._handle_modifier_keys(key)
        self._logger.info("Mod")
        key_press_bytes = keys.keys_keyboard.get(key, None)
        press_bytes = None
        if key_press_bytes is not None:
            press_bytes = modifier_byte + keys.NULL_CHAR + key_press_bytes + keys.NULL_CHAR*5
        elif key in keys.KEYBOARD_MODIFIER_KEYS:
            press_bytes = modifier_byte + keys.NULL_CHAR + keys.NULL_CHAR + keys.NULL_CHAR*5

        return press_bytes, keys.KEYBOARD_RELEASE

    def _handle_modifier_keys(self, key):

        total = 0
        if self.KEY_LEFTCTRL:
            total = total + keys.KEYBOARD_MODIFIER_KEYS.get('KEY_LEFTCTRL')
        if self.KEY_LEFTSHIFT:
            total = total + keys.KEYBOARD_MODIFIER_KEYS.get('KEY_LEFTSHIFT')
        if self.KEY_LEFTALT:
            total = total + keys.KEYBOARD_MODIFIER_KEYS.get('KEY_LEFTALT')
        if self.KEY_LEFTMETA:
            total = total + keys.KEYBOARD_MODIFIER_KEYS.get('KEY_LEFTMETA')
        if self.KEY_RIGHTCTRL:
            total = total + keys.KEYBOARD_MODIFIER_KEYS.get('KEY_RIGHTCTRL')
        if self.KEY_RIGHTSHIFT:
            total = total + keys.KEYBOARD_MODIFIER_KEYS.get('KEY_RIGHTSHIFT')
        if self.KEY_RIGHTALT:
            total = total + keys.KEYBOARD_MODIFIER_KEYS.get('KEY_RIGHTALT')
        if self.KEY_RIGHTMETA:
            total = total + keys.KEYBOARD_MODIFIER_KEYS.get('KEY_RIGHTMETA')
        self._logger.info(f"Total: {total}")
        return bytes([total])

        

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

    def get_bytes_for_key(self, key):
        pass

    def can_handle_key(self, device, key):
        self._logger.info(f"Can handle? {key} - {device}")
        action, _ = device.get_bytes_for_key(key)
        if action is not None:
            self._logger.info(f"YES Can handle? {key} - {device}")
            return True
        return False


    def press_key(self, key):
        try: 
            for device in self.devices:
                if self.can_handle_key(device, key):
                    return device.press_key(key)
        except Exception as e:
            self._logger.error(e)
            return False, str(e)

    def key_down(self, key):
        try: 
            for device in self.devices:
                if self.can_handle_key(device, key):
                    self._logger.info("KEYYING DOWN")
                    return device.key_down(key)
        except Exception as e:
            self._logger.error(e)
            return False, str(e)

    def key_release(self, key):
        try: 
            for device in self.devices:
                if self.can_handle_key(device, key):
                    return device.key_release(key)
        except Exception as e:
            self._logger.error(e)
            return False, str(e)
