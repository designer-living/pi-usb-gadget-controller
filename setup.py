# -*- coding: utf-8 -*-
 
 
"""setup.py: setuptools control."""
 
 
import re
from setuptools import setup
 
 
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('pi_media_remote/__init__.py').read(),
    re.M
    ).group(1)

 
with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")
 
 
setup(
    name = "pi_media_remote",
    packages = ["pi_media_remote"],
    entry_points = {
            "console_scripts": [
                # TODO consolidate this into one app
                'UsbHidRest = pi_media_remote.UsbHidRest:main',
                'UsbHidServer = pi_media_remote.UsbHidServer:main',
                'send_key = pi_media_remote.send_key:main',
            ]
        },
    version = version,
    description = "Application to take commands and send via USB to a Media device like a FireTV or Andriod TV with ChromeCast",
    long_description = long_descr,
    author = "Foxy82",
    author_email = "foxy82.github@gmail.com",
    url = "https://github.com/foxy82/pi-media-remote",
    install_requires = [
            'Flask-RESTful',
        ],
    )
