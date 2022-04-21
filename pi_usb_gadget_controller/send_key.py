#!/usr/bin/env python3
import logging
import sys
from pi_usb_gadget_controller.gadget_device import ConsumerControlGadgetDevice
from pi_usb_gadget_controller.keys import keys, get_bytes_for_key, CONSUMER_CONTROL_RELEASE


def print_usage():
  print("Usage: ", sys.argv[0], " ", '|'.join(keys.keys()))
  sys.exit(-1)


def main():
  logging.basicConfig(level=logging.ERROR)
  if len(sys.argv) != 2:
    print_usage()
  device = '/dev/hidg1'
  sender = ConsumerControlGadgetDevice(device)
  success, action = sender.press_key(sys.argv[1])
  if success and action is None:
      print_usage()
  elif not success:
      print(f"Error: {action}")