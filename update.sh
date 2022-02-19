#!/bin/bash

sudo pip3 install -r ./requirements.txt
sudo cp ./UsbHidServer.py /usr/bin/UsbHidServer.py
sudo chmod +x /usr/bin/UsbHidServer.py
sudo cp ./usb_hid_server.service  /lib/systemd/system/usb_hid_server.service
sudo systemctl daemon-reload
sudo systemctl enable usb_hid_server.service
sudo service usb_hid_server stop
sudo service usb_hid_server start
