# pi-media-remote

## Overview

This repo allows you to make a Pi Zero W appear as a USB media remote control. It can then be plugged into devices like an Android TV or Fire TV and used to control it. 

## Installation

First get required Linux packages:
```
sudo apt-get install git python3
```

Then clone this repo

```
git clone https://github.com/foxy82/pi-media-remote.git
```

To install run ```./install.sh```. Shutdown the pi and then connect it to the device to be controlled using a *data* usb cable and using the *data* usb port on the Pi Zero (the one nearest the HDMI port on Zero W and Zero W2)

## Useful links

Links that helped me come up with this solution

* Tutorial here on how to use the pi zero as a usb gadget - [https://www.isticktoit.net/?p=1383]
* Tutorial for someone doing volume control: https://www.ekwbtblog.com/entry/2019/01/31/000000

* Two tutorials on the report descriptor: [https://notes.iopush.net/blog/2016/custom-usb-hid-device-descriptor-media-keyboard/] and [https://eleccelerator.com/tutorial-about-usb-hid-report-descriptors/]
* Tool to decode the report descriptor: [https://eleccelerator.com/usbdescreqparser/] (need to replace \\x with space for the tool)
* To find keycodes: [https://www.usb.org/hid] document is titled "HID Usage Tables 1.22" we need section 15 "Consumer Control"

