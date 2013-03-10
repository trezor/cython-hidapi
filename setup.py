#!/usr/bin/python

# Depends on libusb-1.0-0-dev, libudev-dev

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os
os.environ['CFLAGS'] = "-I/usr/include/libusb-1.0"
os.environ['LDFLAGS'] = "-L/usr/lib/i386-linux-gnu -lusb-1.0 -ludev -lrt"

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("hid", ["hid.pyx", "hid-libusb.c"],
                   libraries=["usb-1.0", "udev", "rt"])]
)
