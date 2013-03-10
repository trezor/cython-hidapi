#!/usr/bin/python

# Depends on libusb-1.0-0-dev, libudev-dev

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os
import sys

sources = ["hid.pyx"]

if sys.platform.startswith('linux'):
    os.environ['CFLAGS'] = "-I/usr/include/libusb-1.0"
    os.environ['LDFLAGS'] = "-lusb-1.0 -ludev -lrt"
    sources.append("hid-libusb.c")
    libs = ["usb-1.0", "udev", "rt"]

if sys.platform.startswith('darwin'):
    os.environ['CFLAGS'] = "-framework IOKit -framework CoreFoundation"
    os.environ['LDFLAGS'] = ""
    sources.append("hid-mac.c")
    libs = []

if sys.platform.startswith('win'):
    sources.append("hid-windows.c")
    libs = ["setupapi"]

setup(
    name = 'hidapi',
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("hid",  sources, libraries = libs)]
)
