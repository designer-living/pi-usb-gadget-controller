#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Convenience wrapper for running UsbHidServer directly from source tree."""

import logging
from pi_media_remote.UsbGadgetSocketServer import main


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
