#!/bin/bash

# Uncomment if you need to install requirements
sudo service usb_gadget_controller stop
sudo pip install --no-deps --force-reinstall .
sudo service usb_gadget_controller start
