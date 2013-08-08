#!/usr/bin/python

# dependencies: libusb-1.0-0-dev, libudev-dev

# python setup.py sdist upload

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os
import sys

sources = ["hid.pyx", os.path.join(os.getcwd(), "hidapi", "libusb", "hid.c")]]

if sys.platform.startswith('linux'):
    sources_raw = ["hid-raw.pyx", "hid-linux-raw.c"] 
    sources.append("hid-libusb.c")
    libs = ["usb-1.0", "udev", "rt"]
    libs_raw = ["udev", "rt"]
    modules = [Extension("hid",  sources, libraries = libs, extra_compile_args=["-I/usr/include/libusb-1.0"])
            , Extension("hidraw", sources_raw, libraries=libs_raw)]

if sys.platform.startswith('darwin'):
    os.environ['CFLAGS'] = "-framework IOKit -framework CoreFoundation"
    os.environ['LDFLAGS'] = ""
    sources.append("hid-mac.c")
    libs = []
    modules = [Extension("hid",  sources, libraries = libs)]

if sys.platform.startswith('win'):
    sources.append("hid-windows.c")
    libs = ["setupapi"]
    modules = [Extension("hid",  sources, libraries = libs)]

setup(
    name = 'hidapi',
    version = '0.7.0-1',
    description = 'A Cython interface to the hidapi from https://github.com/signal11/hidapi',
    author = 'gbishop',
    author_email = 'gb@cs.unc.edu',
    url = 'https://github.com/gbishop/cython-hidapi',
    classifiers = [
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
    ],
    cmdclass = {'build_ext': build_ext},
    ext_modules = modules
)
