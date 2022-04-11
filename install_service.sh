#!/bin/bash

sudo cp ./usb_gadget_controller.service  /lib/systemd/system/usb_gadget_controller.service
sudo systemctl daemon-reload
sudo systemctl enable usb_gadget_controller.service
sudo service usb_gadget_controller start
