# pi-media-remote

## Overview

This repo allows you to make a Pi Zero W (2) appear as a USB media remote control. It can then be plugged into devices like an Android TV or Fire TV and used to control it over the network.  

## Requirements 

1. A Rasberry Pi Zero W or Rasberry Pi Zero W 2 (it may also work with a Pi 4 but I've not tested this)
1. A way to connect the Pi Zero to the device to be controlled.
    * For [Fire TV](https://www.amazon.co.uk/gp/product/B07M83762Y/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&amp;psc=1&_encoding=UTF8&tag=foxy82-21&linkCode=ur2&linkId=acf241e9ea2e454f9e9116b9aa54ad7a&camp=1634&creative=6738) I used this cable: [FireTv OTG Cable](https://www.amazon.co.uk/gp/product/B08Q36HB3G/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&amp;psc=1&_encoding=UTF8&tag=foxy82-21&linkCode=ur2&linkId=253509fffa53c07250e71ebdd6feae26&camp=1634&creative=6738)
    * For Google Ghromecast with Android TV I use this adapter: [Chromecast with Google TV OTG Cable](https://www.amazon.co.uk/gp/product/B08Q36HB3G/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&amp;psc=1&_encoding=UTF8&tag=foxy82-21&linkCode=ur2&linkId=fcd6d2731b8e1ad8d854ba923336bb38&camp=1634&creative=6738). This also allows you to use Wired Ethernet

## Installation

### Operating System

First install a minimal Linux OS on the Raspberry Pi Zero - I use [DietPi](https://dietpi.com/) with no extra software installed and connect it to your WiFi.

### Clone the repo

ssh to your pi and clone the repo

```
cd ~
sudo apt-get install git
git clone https://github.com/foxy82/pi-usb-gadget-controller.git
```

### Install USB Gadget

Setup the pi so that it will behave as a USB Gadget.

```
cd ~/pi-usb-gadget-controller
./install_usb_gadget.sh
```

### Install the app

Get the required packages first

```
sudo apt-get install python3 python3-pip
```

#### From pypi

```
sudo pip3 install pi_usb_gadget_controller
```

#### From source

```
cd ~/pi-usb-gadget-controller
sudo pip3 install .
```

### Running

The above will install anm executable called ```UsbGadgetController```. Running this will start a server on the default settings - you will need to run as sudo to access the USB gadget device or setup permissions to access it as a regular user. 

```
$ sudo UsbGadgetController
```

There are some options that can be set

```
$ UsbGadgetController -h
usage: UsbGadgetController [-h] [--device DEVICE] [--web_port WEB_PORT] [--socket_port SOCKET_PORT]
                              [--logging {DEBUG,INFO,WARNING,ERROR}]

Send commands to a USB Gadget

optional arguments:
  -h, --help            show this help message and exit
  --device DEVICE       The USB Gadget device. DEFAULTS to /dev/hidg0
  --web_port WEB_PORT   The port to start the web_port on. DEFAULTS to 8080. NOTE if you specify a port here you also need
                        to spcify a --socket_port otherwise the socket port won't be opened
  --socket_port SOCKET_PORT
                        The port to start the socket server on. DEFAULTS to 8888. NOTE if you specify a port here you also
                        need to spcify a --web_port otherwise the web port won't be opened
  --logging {DEBUG,INFO,WARNING,ERROR}
                        The logging level to use. DEFAULTS to INFO

```

### Install as a service (optional)

You can install the server as a service to run on start up:
```
cd ~/pi-usb-gadget-controller
sudo ./install_service.sh
```

This will use the default options. To change the options edit ```~/pi-usb-gadget-controller/usb_gadget_controller.service```  and edit the ```ExecStart``` line then run ```./install_service.sh``` (first install) or ```./update_service.sh``` (updating)

## Connect your pi

Shutdown the pi and then connect it to the device to be controlled using a *data* usb cable and using the *data* usb port on the Pi Zero (the one nearest the HDMI port on Zero W and Zero W2)

## Usage 

This app provides several ways to receive commands and currently supports the following:
* UP
* DOWN
* LEFT
* RIGHT
* SELECT
* HOME
* BACK
* PLAY
* MUTE

### Socket interface

A socket interface is provided on port 8888 (by default) it takes the key to press in upper case e.g. UP,DOWN

### Websocket interface

A websocket interface is provided at http://ip:8080/ws it will take the commands in uppercase e.g. UP, DOWN

### Rest API

A REST API is provided by doing a GET at http://ip:8080/rest/<command> where command is the key to send e.g. UP, DOWN

### GET Requests

You can also do plain GET requests to http://ip:8080/get/<command> where command is the key to send e.g. UP, DOWN. This call will provide a redirect to a web page (see below)

### Web Page

The app also provides 3 web pages with remote buttons to click and send commands:
* http://ip:8080 - is a web page using web socket for communication - it should be the fastest to use
* http://ip:8080/js - is a web page that uses JavaScript to make REST calls in the background - I have sometimes seen Chrome take up to 1+ seconds to actually send the command so WebSocket is prefered if you can use that.
* http://ip:8080/get - Sends GET requests and reloads the page on every click. Likely to be slow but will work if you don't want to use JavaScript or WebSockets.


## Update

This is a work in progress so there might be times when updating is more complex. However you can try running ```./update.sh``` from the root of the git repo.

## Uninstall

The best bet is to just write a brand new OS onto the SD card however if you do need to remove...

```
cd ~/pi-usb-gadget-controller
sudo ./uninstall_service.sh # Only if you installed this as a service
sudo ./uninstall_usb_gadget.sh # Follow the additional instructions
sudo pip uninstall pi_usb_gadget_controller
```


## Roadmap

Things i'm working on for this:

* V2 of the API to allow pressing and holding as well as allow keyboard keys to be sent.
* A seperate app which will take input from a 2.4 GHz USB remote and transmit it to this app
* Using a [Pulse Eight USB CEC Adapter](https://www.amazon.co.uk/Pulse-Eight-na-USB-CEC-Adapter/dp/B005JU6LWM/ref=sr_1_1?crid=N8E5OFI7LAC3&amp;keywords=pulse+eight+USB+CEC&amp;qid=1649681621&amp;sprefix=pulse+eight+usb+cec%252Caps%252C57&amp;sr=8-1&_encoding=UTF8&tag=foxy82-21&linkCode=ur2&linkId=9de6a10b778cb0ef9814579952996036&camp=1634&creative=6738) to take CEC commands and send it to this app.
* Moon shot - can we add a way for a mic to send us audio data so that we could do a voice search? 

## Useful links

Links that helped me come up with this solution

* Tutorial here on how to use the pi zero as a usb gadget - [https://www.isticktoit.net/?p=1383]
* Tutorial for someone doing volume control: https://www.ekwbtblog.com/entry/2019/01/31/000000
* Two tutorials on the report descriptor: [https://notes.iopush.net/blog/2016/custom-usb-hid-device-descriptor-media-keyboard/] and [https://eleccelerator.com/tutorial-about-usb-hid-report-descriptors/]
* Tool to decode the report descriptor: [https://eleccelerator.com/usbdescreqparser/] (need to replace \\x with space for the tool)
* To find keycodes: [https://www.usb.org/hid] document is titled "HID Usage Tables 1.22" we need section 15 "Consumer Control"