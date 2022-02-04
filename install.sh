#!/bin/bash

# Set required settings and modules
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
echo "libcomposite" | sudo tee -a /etc/modules

# Install the USB HID files
sudo cp ./pi_zero_usb_media_remote /usr/bin/pi_zero_usb_media_remote
sudo chmod +x /usr/bin/pi_zero_usb_media_remote

# Set the USB HID file to run on startup
sudo cp ./usb_media_remote.service /lib/systemd/system/usb_media_remote.service
sudo systemctl daemon-reload
sudo systemctl enable usb_media_remote.service

# Set the Server to listen for commands on startup
sudo cp ./UsbHidServer.py /usr/bin/UsbHidServer.py
sudo chmod +x /usr/bin/UsbHidServer.py
sudo cp ./usb_hid_server.service  /lib/systemd/system/usb_hid_server.service
sudo systemctl daemon-reload
sudo systemctl enable usb_hid_server.service
