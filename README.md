# pi-media-remote

## Overview

This repo allows you to make a Pi Zero W (2) appear as a USB media remote control. It can then be plugged into devices like an Android TV or Fire TV and used to control it over the network.  

## Requirements 

1. A Rasberry Pi Zero W or Rasberry Pi Zero W 2 (it may also work with a Pi 4 but I've not tested this)
1. A way to connect the Pi Zero to the device to be controlled.
    * For [Fire TV](https://www.amazon.co.uk/gp/product/B08MQZYSVC/ref=as_li_tl?ie=UTF8&camp=1634&creative=6738&creativeASIN=B08MQZYSVC&linkCode=as2&tag=foxy82-21&linkId=515ca2c069563973ff420dad6d0b9333) I used this cable: [FireTv OTG Cable](https://www.amazon.co.uk/gp/product/B08Q36HB3G/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&amp;psc=1&_encoding=UTF8&tag=foxy82-21&linkCode=ur2&linkId=253509fffa53c07250e71ebdd6feae26&camp=1634&creative=6738)
    * For Google Ghromecast with Android TV I use this adapter: [Chromecast with Google TV OTG Cable](https://www.amazon.co.uk/gp/product/B08Q36HB3G/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&amp;psc=1&_encoding=UTF8&tag=foxy82-21&linkCode=ur2&linkId=fcd6d2731b8e1ad8d854ba923336bb38&camp=1634&creative=6738)

## Installation

First install a minimal Linux OS on the Raspberry Pi Zero

First get required Linux packages:
```
sudo apt-get install git python3
```

Then clone this repo

```
git clone https://github.com/foxy82/pi-media-remote.git
```

To install run ```./install.sh```. Shutdown the pi and then connect it to the device to be controlled using a *data* usb cable and using the *data* usb port on the Pi Zero (the one nearest the HDMI port on Zero W and Zero W2)

## Update

This is a work in progress so there might be times when updating is more complex. However you can try running ```./update.sh``` from the root of the git repo.

## Uninstall

The best bet is to just write a brand new OS onto the SD card however if you do need to remove have a look at ```uninstall.sh``` which removes some files and guides you on other changes needed to remove this.

## Roadmap

Things i'm working on for this:

* V2 of the API to allow pressing and holding as well as allow keyboard keys to be sent.
* A seperate app which will take input from a 2.4 GHz USB remote and transmit it to this app
* Using a [Pulse Eight USB CEC Adapter](https://www.amazon.co.uk/Pulse-Eight-na-USB-CEC-Adapter/dp/B005JU6LWM/ref=sr_1_1?crid=N8E5OFI7LAC3&amp;keywords=pulse+eight+USB+CEC&amp;qid=1649681621&amp;sprefix=pulse+eight+usb+cec%252Caps%252C57&amp;sr=8-1&_encoding=UTF8&tag=foxy82-21&linkCode=ur2&linkId=9de6a10b778cb0ef9814579952996036&camp=1634&creative=6738) to take CEC commands and send it to this app.

## Useful links

Links that helped me come up with this solution

* Tutorial here on how to use the pi zero as a usb gadget - [https://www.isticktoit.net/?p=1383]
* Tutorial for someone doing volume control: https://www.ekwbtblog.com/entry/2019/01/31/000000
* Two tutorials on the report descriptor: [https://notes.iopush.net/blog/2016/custom-usb-hid-device-descriptor-media-keyboard/] and [https://eleccelerator.com/tutorial-about-usb-hid-report-descriptors/]
* Tool to decode the report descriptor: [https://eleccelerator.com/usbdescreqparser/] (need to replace \\x with space for the tool)
* To find keycodes: [https://www.usb.org/hid] document is titled "HID Usage Tables 1.22" we need section 15 "Consumer Control"

