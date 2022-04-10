#!/usr/bin/env python3
import logging
import sys

NULL_CHAR = bytes((0,))
RELEASE = NULL_CHAR*2


keys = {
    "UP": bytes((66,)) + NULL_CHAR,
    "DOWN": bytes((67,))+NULL_CHAR,
    "LEFT": bytes((68,))+NULL_CHAR,
    "RIGHT": bytes((69,))+NULL_CHAR,
    "SELECT": bytes((65,))+NULL_CHAR,
    "HOME": bytes((35,))+bytes((2,)),
    "BACK": bytes((36,))+bytes((2,)),
    "PLAY": bytes((205,))+NULL_CHAR,
    "MUTE": bytes((226,))+NULL_CHAR,
    "MIC": bytes((207,))+NULL_CHAR,
}


def print_usage():
  print("Usage: ", sys.argv[0], " ", '|'.join(keys.keys()))
  sys.exit(-1)


class SendGadgetDevice():

    def __init__(self, device, keep_usb_open=False):
        self._logger = logging.getLogger(__name__)
        self._keep_usb_open = keep_usb_open
        self._device = device
        self._fd = None

        if self._keep_usb_open:
            self._fd = open(self._device, 'rb+', buffering=0)
        pass

    def close(self):
        if self._fd is not None:
            self._fd.close()
            self._fd = None

    def _get_bytes_to_send(self, key):
        action = keys.get(key, None)
        if action is None:
            self._logger.warning(f"Key not found {key}")
        else:
            self._logger.debug(f"Found key {key} : {action}")

        return action

    def press_key(self, key):
        action = self._get_bytes_to_send(key)
        self._logger.debug(f"Pressing key {key} : {action} ")
        if self._keep_usb_open:
            self._key_down(action, self._fd)
            self._key_release(self._fd)
        else:
            # If we find a long running connection causes an issue we can just open on each key press.
            with open(self._device, 'rb+') as fd:
                self._key_down(action, fd)
                self._key_release(fd)

    def key_down(self, key):
        action = self._get_bytes_to_send(key)
        self._logger.debug(f"Key Down {key} : {action} ")
        if self._keep_usb_open:
            self._key_down(action, self._fd)
        else:
            # If we find a long running connection causes an issue we can just open on each key press.
            with open(self._device, 'rb+') as fd:
                self._key_down(action, fd)

    def key_release(self):
        self._logger.debug(f"Releasing keys")
        if self._keep_usb_open:
            self._key_release(self._fd)
        else:
            # If we find a long running connection causes an issue we can just open on each key press.
            with open(self._device, 'rb+') as fd:
                self._key_release(fd)

    def _key_down(self, key, fd):
        self._send_key(key, fd)

    def _key_release(self, fd):
        self._send_key(RELEASE, fd)

    def _send_key(self, action, fd):
        if action is None:
            return
        if fd is None:
            self._logger.warning(f"No where to send {action} to")
        else:
            self._logger.debug(f"Sending as fd not None {action}")
            fd.write(action)


def main():
  logging.basicConfig(level=logging.INFO)
  if len(sys.argv) != 2:
    print_usage()
#   press_key(sys.argv[1])
#   print("Done")
  device = '/dev/hidg0'
  sender = SendGadgetDevice(device)
  sender.press_key(sys.argv[1])