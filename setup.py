#!/usr/bin/python
from setuptools import setup, Extension
import os
import sys
import subprocess

hidapi_topdir = os.path.join("hidapi")
hidapi_include = os.path.join(hidapi_topdir, "hidapi")
system_hidapi = 0
libs = []
src = ["hid.pyx", "chid.pxd"]


def hidapi_src(platform):
    return os.path.join(hidapi_topdir, platform, "hid.c")


if "--with-system-hidapi" in sys.argv:
    sys.argv.remove("--with-system-hidapi")
    system_hidapi = 1
    hidapi_include = "/usr/include/hidapi"

if sys.platform.startswith("linux"):
    modules = []
    if "--without-libusb" in sys.argv:
        sys.argv.remove("--without-libusb")
        hidraw_module = "hid"
    else:
        hidraw_module = "hidraw"
        libs = ["usb-1.0", "udev", "rt"]
        if system_hidapi == 1:
            libs.append("hidapi-libusb")
        else:
            src.append(hidapi_src("libusb"))
        modules.append(
            Extension(
                "hid",
                sources=src,
                include_dirs=[hidapi_include, "/usr/include/libusb-1.0"],
                libraries=libs,
            )
        )
    libs = ["udev", "rt"]
    src = ["hidraw.pyx", "chid.pxd"]
    if system_hidapi == 1:
        libs.append("hidapi-hidraw")
    else:
        src.append(hidapi_src("linux"))
    modules.append(
        Extension(
            hidraw_module, sources=src, include_dirs=[hidapi_include], libraries=libs,
        )
    )

if sys.platform.startswith("darwin"):
    macos_sdk_path = (
        subprocess.check_output(["xcrun", "--show-sdk-path"]).decode().strip()
    )
    os.environ["CFLAGS"] = (
        '-isysroot "%s" -framework IOKit -framework CoreFoundation -framework AppKit'
        % macos_sdk_path
    )
    os.environ["LDFLAGS"] = ""
    if system_hidapi == True:
        libs.append("hidapi")
    else:
        src.append(hidapi_src("mac"))
    modules = [
        Extension("hid", sources=src, include_dirs=[hidapi_include], libraries=libs,)
    ]

if sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
    libs = ["setupapi"]
    if system_hidapi == True:
        libs.append("hidapi")
    else:
        src.append(hidapi_src("windows"))
    modules = [
        Extension("hid", sources=src, include_dirs=[hidapi_include], libraries=libs,)
    ]

if "bsd" in sys.platform:
    if "freebsd" in sys.platform:
        libs = ["usb", "hidapi"]
        include_dirs_bsd = ["/usr/local/include/hidapi"]
    else:
        libs = ["usb-1.0"]
        include_dirs_bsd = [
            hidapi_include,
            "/usr/include/libusb-1.0",
            "/usr/local/include/libusb-1.0",
            "/usr/local/include/",
        ]
        if system_hidapi == True:
            libs.append("hidapi-libusb")
        else:
            src.append(hidapi_src("libusb"))
    modules = [
        Extension("hid", sources=src, include_dirs=include_dirs_bsd, libraries=libs,)
    ]

setup(
    name="hidapi",
    version="0.11.2",
    description="A Cython interface to the hidapi from https://github.com/libusb/hidapi",
    long_description=open("README.rst", "rt").read(),
    author="Pavol Rusnak",
    author_email="pavol@rusnak.io",
    maintainer="Pavol Rusnak",
    maintainer_email="pavol@rusnak.io",
    url="https://github.com/trezor/cython-hidapi",
    package_dir={"hid": "hidapi/*"},
    classifiers=[
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    ext_modules=modules,
    setup_requires=["Cython"],
    install_requires=["setuptools>=19.0"],
)
