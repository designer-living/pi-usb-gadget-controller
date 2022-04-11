# -*- coding: utf-8 -*-
 
 
"""setup.py: setuptools control."""
 
 
import re
from setuptools import setup
 
 
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('pi_usb_gadget_controller/__init__.py').read(),
    re.M
    ).group(1)

 
with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")
 
 
setup(
    name = "pi_usb_gadget_controller",
    packages = ["pi_usb_gadget_controller"],
    entry_points = {
            "console_scripts": [
                'UsbGadgetController = pi_usb_gadget_controller.UsbGadgetController:main',
                'send_key = pi_usb_gadget_controller.send_key:main',
            ]
        },
    version = version,
    license='Apache 2.0'
    description = "Application to take commands and send via USB to a Media device like a FireTV or Andriod TV with ChromeCast",
    long_description = long_descr,
    author = "Foxy82",
    author_email = "foxy82.github@gmail.com",
    url = "https://github.com/foxy82/pi-usb-gadget-controller",
    download_url = f'https://github.com/foxy82/pi-usb-gadget-controller/{version}.tar.gz',
    install_requires = [
            'aiohttp',
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],        
)
