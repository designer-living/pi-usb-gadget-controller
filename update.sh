#!/bin/bash

# Uncomment if you need to install requirements
echo "Stopping Service"
sudo service usb_gadget_controller stop
echo "Service stopped"
echo "Updating software"
sudo pip install --no-deps --force-reinstall .
echo "Software updated"
echo "Starting service"
sudo service usb_gadget_controller start
echo "Service Started"
