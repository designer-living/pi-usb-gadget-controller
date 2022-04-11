#!/bin/bash

# Install required debian software
sudo apt-get install -y alsa-utils python3 python3-pip

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
sudo service usb_media_remote start

# Set the Server to listen for commands on startup
sudo pip3 install -r ./requirements.txt
sudo python3 setup.py install

sudo cp ./usb_gadget_controller.service  /lib/systemd/system/usb_gadget_controller.service
sudo systemctl daemon-reload
sudo systemctl enable usb_gadget_controller.service
sudo service usb_gadget_controller start
