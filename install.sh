# Set required settings and modules

echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
echo "libcomposite" | sudo tee -a /etc/modules

sudo cp pi_zero_usb_media_remote /usr/bin/pi_zero_usb_media_remote
sudo chmod +x /usr/bin/pi_zero_usb_media_remote
