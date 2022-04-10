#!/bin/bash

#sudo pip3 install -r ./requirements.txt
sudo cp ./UsbHidRest.py /usr/bin/UsbHidRest.py
sudo cp ./send_key.py /usr/bin/send_key.py
sudo chmod +x /usr/bin/UsbHidRest.py
sudo chmod +x /usr/bin/send_key.py
sudo cp ./usb_rest_server.service  /lib/systemd/system/usb_rest_server.service
sudo systemctl daemon-reload
sudo systemctl enable usb_rest_server.service
sudo service usb_rest_server stop
sudo service usb_rest_server start
