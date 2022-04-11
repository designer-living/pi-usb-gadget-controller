#!/bin/bash
sudo service usb_gadget_controller stop
sudo systemctl disable usb_gadget_controller.service
sudo rm -f /lib/systemd/system/usb_gadget_controller.service
sudo systemctl daemon-reload