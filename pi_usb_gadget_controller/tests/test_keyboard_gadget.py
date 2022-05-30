from pi_usb_gadget_controller.gadget_device import KeyboardGadgetDevice
import unittest
from unittest.mock import patch, mock_open, call


class TestKeyboardGadgetDevice(unittest.TestCase):

    def test_keyboard_handles_key_down(self):
        device_name = "/dev/hidg0"
        open_mock_remote = mock_open()
        with patch("builtins.open", open_mock_remote) as mock_file:
            remote_gadget = KeyboardGadgetDevice(device_name)
            remote_gadget.handle("down", "KEY_A")
        open_mock_remote.assert_called_once_with(device_name, 'rb+')
        handle = open_mock_remote()
        handle.write.assert_called_once_with(bytes((0x0, 0x0, 0x04, 0x0, 0x0, 0x0, 0x0, 0x0)))

    def test_keyboard_handles_key_up(self):
        device_name = "/dev/hidg0"
        open_mock_remote = mock_open()
        with patch("builtins.open", open_mock_remote) as mock_file:
            remote_gadget = KeyboardGadgetDevice(device_name)
            remote_gadget.handle("up", "KEY_A")
        open_mock_remote.assert_called_once_with(device_name, 'rb+')
        handle = open_mock_remote()
        handle.write.assert_called_once_with(bytes((0x0, 0x0, 0x00, 0x0, 0x0, 0x0, 0x0, 0x0)))

    def test_keyboard_handles_key_press(self):
        device_name = "/dev/hidg0"
        open_mock_remote = mock_open()
        with patch("builtins.open", open_mock_remote) as mock_file:
            remote_gadget = KeyboardGadgetDevice(device_name)
            remote_gadget.handle("press", "KEY_A")
        open_mock_remote.assert_called_once_with(device_name, 'rb+')
        handle = open_mock_remote()
        print(open_mock_remote.mock_calls)
        self.assertEqual(2, open_mock_remote.call_count)
        calls = [
            call(bytes((0x0, 0x0, 0x04, 0x0, 0x0, 0x0, 0x0, 0x0))),
            call(bytes((0x0, 0x0, 0x00, 0x0, 0x0, 0x0, 0x0, 0x0))),
        ]
        handle.write.assert_has_calls(calls)

    def test_keyboard_handles_shift_key(self):
        device_name = "/dev/hidg0"
        open_mock_remote = mock_open()
        with patch("builtins.open", open_mock_remote) as mock_file:
            remote_gadget = KeyboardGadgetDevice(device_name)
            remote_gadget.handle("down", "KEY_LEFTSHIFT")
            remote_gadget.handle("press", "KEY_A")
            remote_gadget.handle("up", "KEY_LEFTSHIFT")

        open_mock_remote.assert_any_call(device_name, 'rb+')
        handle = open_mock_remote()
        calls = [
            call(bytes((0x2, 0x0, 0x00, 0x0, 0x0, 0x0, 0x0, 0x0))),
            call(bytes((0x2, 0x0, 0x04, 0x0, 0x0, 0x0, 0x0, 0x0))),
            call(bytes((0x2, 0x0, 0x00, 0x0, 0x0, 0x0, 0x0, 0x0))),
            call(bytes((0x0, 0x0, 0x00, 0x0, 0x0, 0x0, 0x0, 0x0))),
        ]
        handle.write.assert_has_calls(calls)

    def test_keyboard_handles_multiple_keys(self):
        device_name = "/dev/hidg0"
        open_mock_remote = mock_open()
        with patch("builtins.open", open_mock_remote) as mock_file:
            remote_gadget = KeyboardGadgetDevice(device_name)
            remote_gadget.handle("down", "KEY_LEFTSHIFT")
            remote_gadget.handle("down", "KEY_RIGHTCTRL")
            remote_gadget.handle("press", "KEY_A")
            remote_gadget.handle("up", "KEY_LEFTSHIFT")
            remote_gadget.handle("up", "KEY_RIGHTCTRL")

        open_mock_remote.assert_any_call(device_name, 'rb+')
        handle = open_mock_remote()
        calls = [
            call(bytes((0x2, 0x0, 0x00, 0x0, 0x0, 0x0, 0x0, 0x0))),
            call(bytes((0x12, 0x0, 0x00, 0x0, 0x0, 0x0, 0x0, 0x0))),
            call(bytes((0x12, 0x0, 0x04, 0x0, 0x0, 0x0, 0x0, 0x0))),
            call(bytes((0x12, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0))),
            call(bytes((0x10, 0x0, 0x00, 0x0, 0x0, 0x0, 0x0, 0x0))),
            call(bytes((0x0, 0x0, 0x00, 0x0, 0x0, 0x0, 0x0, 0x0))),
        ]
        handle.write.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
