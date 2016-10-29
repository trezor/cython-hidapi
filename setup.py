#!/usr/bin/python
from setuptools import setup, Extension
import os
import sys

hidapi_topdir = os.path.join('hidapi')
hidapi_include = os.path.join(hidapi_topdir, 'hidapi')
system_hidapi = 0
libs= []
src = ['hid.pyx', 'chid.pxd']

def hidapi_src(platform):
    return os.path.join(hidapi_topdir, platform, 'hid.c')

if '--with-system-hidapi' in sys.argv:
    sys.argv.remove('--with-system-hidapi')
    system_hidapi = 1
    hidapi_include = '/usr/include/hidapi'

if sys.platform.startswith('linux'):
    modules = []
    if '--without-libusb' in sys.argv:
        sys.argv.remove('--without-libusb')
        hidraw_module = 'hid'
    else:
        hidraw_module = 'hidraw'
        libs = ['usb-1.0', 'udev', 'rt']
        if system_hidapi == 1:
            libs.append('hidapi-libusb')
        else:
            src.append(hidapi_src('libusb'))
        modules.append(
            Extension('hid',
                sources = src,
                include_dirs = [hidapi_include, '/usr/include/libusb-1.0'],
                libraries = libs,
            )
        )
    libs = ['udev', 'rt']
    src = ['hid.pyx', 'chid.pxd']
    if system_hidapi == 1:
        libs.append('hidapi-hidraw')
    else:
        src.append(hidapi_src('linux'))
    modules.append(
        Extension(hidraw_module,
            sources = src,
            include_dirs = [hidapi_include],
            libraries = libs,
        )
    )

if sys.platform.startswith('darwin'):
    os.environ['CFLAGS'] = '-framework IOKit -framework CoreFoundation'
    os.environ['LDFLAGS'] = ''
    if system_hidapi == True:
        libs.append('hidapi')
    else:
        src.append(hidapi_src('mac'))
    modules = [
        Extension('hid',
            sources = src,
            include_dirs = [hidapi_include],
            libraries = libs,
        )
    ]

if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
    libs = ['setupapi']
    if system_hidapi == True:
        libs.append('hidapi')
    else:
        src.append(hidapi_src('windows'))
    modules = [
        Extension('hid',
            sources = src,
            include_dirs = [hidapi_include],
            libraries = libs,
        )
    ]

if 'bsd' in sys.platform:
    libs = ['usb-1.0']
    if system_hidapi == True:
        libs.append('hidapi-libusb')
    else:
        src.append(hidapi_src('libusb'))
    modules = [
        Extension('hid',
            sources = src,
            include_dirs = [hidapi_include, '/usr/include/libusb-1.0'],
            libraries = libs,
        )
    ]

setup(
    name = 'hidapi',
    version = '0.7.99.post20',
    description = 'A Cython interface to the hidapi from https://github.com/signal11/hidapi',
    author = 'Gary Bishop',
    author_email = 'gb@cs.unc.edu',
    maintainer = 'Pavol Rusnak',
    maintainer_email = 'stick@gk2.sk',
    url = 'https://github.com/trezor/cython-hidapi',
    package_dir = {'hid': 'hidapi/*'},
    classifiers = [
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    ext_modules = modules,
    setup_requires = ['Cython'],
    install_requires = ['setuptools>=19.0'],
)
