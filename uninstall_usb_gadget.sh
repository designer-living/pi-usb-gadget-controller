#!/bin/bash


sudo service usb_media_remote stop
sudo systemctl disable usb_media_remote.service
sudo rm -f /lib/systemd/system/usb_media_remote.service
sudo systemctl daemon-reload

sudo rm -f /usr/bin/pi_zero_usb_media_remote

# Now remove the following: Set required settings and modules
echo "Now remove 'dtoverlay=dwc2' from /boot/config.txt"
echo "Now remove 'dwc2' from /etc/modules"
echo "Now remove 'libcomposite' from /etc/modules"
