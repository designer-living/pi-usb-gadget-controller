from pi_usb_gadget_controller.gadget_device import CompositeGadgetDevice, ConsumerControlGadgetDevice, KeyboardGadgetDevice
import unittest
from unittest.mock import patch, mock_open, MagicMock


def get_mock_open(files: dict[str, str]):
    def open_mock(filename, *args, **kwargs):
        for expected_filename, content in files.items():
            if filename == expected_filename:
                return content.return_value
        raise FileNotFoundError('(mock) Unable to open {filename}')

    return MagicMock(side_effect=open_mock)


class TestCompositeGadgetDevice(unittest.TestCase):

    def test_composite_device_one_device(self):
        device_name = "/dev/hidg1"
        open_mock_remote = mock_open()
        with patch("builtins.open", open_mock_remote) as mock_file:
            remote_gadget = ConsumerControlGadgetDevice(device_name)
            composite_device = CompositeGadgetDevice(remote_gadget)
            remote_gadget.handle("down", "KEY_ENTER")
        open_mock_remote.assert_called_once_with(device_name, 'rb+')
        handle = open_mock_remote()
        handle.write.assert_called_once_with(bytes((0x41, 0x0)))

    def test_composite_device(self):
        device_name_kb = "/dev/hidg0"
        device_name_remote = "/dev/hidg1"
        open_mock_remote = mock_open()
        open_mock_kb = mock_open()

        files = {device_name_kb: open_mock_kb,
                 device_name_remote: open_mock_remote}

        with patch("builtins.open", get_mock_open(files)) as mock_file:
            remote_gadget = ConsumerControlGadgetDevice(device_name_remote)
            kb_gadget = KeyboardGadgetDevice(device_name_kb)
            composite_gadget = CompositeGadgetDevice(remote_gadget, kb_gadget)
            composite_gadget.handle("down", "KEY_A")
            composite_gadget.handle("down", "KEY_ENTER")

        handle_remote = open_mock_remote()
        handle_remote.write.assert_called_once_with(bytes((0x41, 0x0)))
        handle_kb = open_mock_kb()
        handle_kb.write.assert_called_once_with(bytes((0x0, 0x0, 0x04, 0x0, 0x0, 0x0, 0x0, 0x0)))


if __name__ == '__main__':
    unittest.main()
