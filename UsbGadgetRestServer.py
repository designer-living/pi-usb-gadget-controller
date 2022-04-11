#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Convenience wrapper for running UsbGadgetRestServer directly from source tree."""

import logging 
from pi_usb_gadget_controller.UsbGadgetRestServer import main


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
