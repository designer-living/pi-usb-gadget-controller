#!/bin/bash

# Remove the USB HID file
sudo service usb_media_remote stop
sudo systemctl disable usb_media_remote.service
sudo rm -f /lib/systemd/system/usb_media_remote.service
sudo systemctl daemon-reload
sudo rm -f /usr/bin/pi_zero_usb_media_remote

# Remove the server
sudo service usb_gadget_controller stop
sudo systemctl disable usb_gadget_controller.service
sudo rm -f /lib/systemd/system/usb_gadget_controller.service
sudo systemctl daemon-reload


# MANUAL STEPS below

# Remove "dtoverlay=dwc2" from /boot/config/txt
# Remove "dwc2" from /etc/modules
# Remove "libcomposite" /etc/modules

# Remove this package
# sudo pip3 uninstall pi_media_remote

# Remove the pip packages we installed - don't remove ones you are using elsewgere
# sudo pip3 uninstall -r ./requirements.txt

# Remove packages we installed. Run the command manaully with only the packages you want to remove
# sudo apt-get remove -y alsa-utils python3 python3-pip
