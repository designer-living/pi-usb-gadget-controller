from pi_usb_gadget_controller.gadget_device import ConsumerControlGadgetDevice
import unittest
from unittest.mock import patch, mock_open, call


class TestCompositeGadgetDevice(unittest.TestCase):

    def test_remote_handles_key_down(self):
        device_name = "/dev/hidg1"
        open_mock_remote = mock_open()
        with patch("builtins.open", open_mock_remote) as mock_file:
            remote_gadget = ConsumerControlGadgetDevice(device_name)
            remote_gadget.handle("down", "KEY_ENTER")
        open_mock_remote.assert_called_once_with(device_name, 'rb+')
        handle = open_mock_remote()
        handle.write.assert_called_once_with(bytes((0x41, 0x0)))

    def test_remote_handles_key_up(self):
        device_name = "/dev/hidg1"
        open_mock_remote = mock_open()
        with patch("builtins.open", open_mock_remote) as mock_file:
            remote_gadget = ConsumerControlGadgetDevice(device_name)
            remote_gadget.handle("up", "KEY_ENTER")
        open_mock_remote.assert_called_once_with(device_name, 'rb+')
        handle = open_mock_remote()
        handle.write.assert_called_once_with(bytes((0x0, 0x0)))

    def test_remote_handles_key_press(self):
        device_name = "/dev/hidg1"
        open_mock_remote = mock_open()
        with patch("builtins.open", open_mock_remote) as mock_file:
            remote_gadget = ConsumerControlGadgetDevice(device_name)
            remote_gadget.handle("press", "KEY_ENTER")
        open_mock_remote.assert_called_once_with(device_name, 'rb+')
        handle = open_mock_remote()
        calls = [
            call(bytes((0x41, 0x0))),
            call(bytes((0x0, 0x0))),
        ]
        self.assertEqual(2, open_mock_remote.call_count)
        handle.write.assert_has_calls(calls)

    def test_remote_handles_raw_key(self):
        device_name = "/dev/hidg1"
        open_mock_remote = mock_open()
        with patch("builtins.open", open_mock_remote) as mock_file:
            remote_gadget = ConsumerControlGadgetDevice(device_name)
            remote_gadget.handle("down", "KEY_RAW|c02f8")
        open_mock_remote.assert_called_once_with(device_name, 'rb+')
        handle = open_mock_remote()
        handle.write.assert_called_once_with(bytes((0xF8, 0x02)))

if __name__ == '__main__':
    unittest.main()
