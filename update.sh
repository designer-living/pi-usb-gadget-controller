#!/bin/bash

# Uncomment if you need to install requirements
# sudo pip3 install -r ./requirements.txt


sudo service usb_hid_server stop
sudo service usb_media_remote stop

sudo python3 setup.py install

sudo service usb_hid_server start
sudo service usb_media_remote start