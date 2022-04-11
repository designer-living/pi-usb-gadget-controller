#!/bin/bash

# Uncomment if you need to install requirements
# sudo pip3 install -r ./requirements.txt


sudo service usb_gadget_controller stop

sudo python3 setup.py install --force

sudo service usb_gadget_controller start
