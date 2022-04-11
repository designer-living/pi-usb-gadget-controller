#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Convenience wrapper for running a test client directly from source tree."""

import logging
from pi_usb_gadget_controller.test_client.TestSocketClient import main


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
