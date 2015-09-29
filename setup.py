#!/usr/bin/python
from setuptools import setup, Extension
import os
import sys

setup_args = {}
hidapi_topdir = os.path.join('hidapi')
hidapi_include = os.path.join(hidapi_topdir, 'hidapi')
def hidapi_src(platform):
    return os.path.join(hidapi_topdir, platform, 'hid.c')

# Add the build_ext command if cython is already installed
cmdclass = None
try:
    from Cython.Distutils import build_ext
    cmdclass = {'build_ext': build_ext}
    setup_args['cmdclass'] = cmdclass
except ImportError:
    pass

if sys.platform.startswith('linux'):
    modules = [
        Extension('hid',
                  sources = ['hid.pyx', 'chid.pxd', hidapi_src('libusb')],
                  include_dirs = [hidapi_include, '/usr/include/libusb-1.0'],
                  libraries = ['usb-1.0', 'udev', 'rt'],
        ),
        Extension('hidraw',
                  sources = ['hidraw.pyx', hidapi_src('linux')],
                  include_dirs = [hidapi_include],
                  libraries = ['udev', 'rt'],
        )
    ]

if sys.platform.startswith('darwin'):
    os.environ['CFLAGS'] = '-framework IOKit -framework CoreFoundation'
    os.environ['LDFLAGS'] = ''
    modules = [
        Extension('hid',
                  sources = ['hid.pyx', 'chid.pxd', hidapi_src('mac')],
                  include_dirs = [hidapi_include],
                  libraries = [],
        )
    ]

if sys.platform.startswith('win'):
    modules = [
        Extension('hid',
            sources = ['hid.pyx', 'chid.pxd', hidapi_src('windows')],
            include_dirs = [hidapi_include],
            libraries = ['setupapi'],
        )
    ]

setup(
    name = 'hidapi',
    version = '0.7.99-8',
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
    ],
    ext_modules = modules,
    setup_requires = ['cython'],
    **setup_args
)
