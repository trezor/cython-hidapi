#!/usr/bin/python
from Cython.Build import cythonize
from setuptools import setup, Extension
import os
import pkgconfig
import re
import subprocess
import sys

tld = os.path.abspath(os.path.dirname(__file__))
embedded_hidapi_topdir = os.path.join(tld, "hidapi")
embedded_hidapi_include = os.path.join(embedded_hidapi_topdir, "hidapi")


def hidapi_src(platform):
    return os.path.join(embedded_hidapi_topdir, platform, "hid.c")


def hid_from_embedded_hidapi():
    # TODO: what about MinGW/msys?
    if sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
        modules = [
            Extension(
                "hid",
                sources=["hid.pyx", hidapi_src("windows")],
                include_dirs=[embedded_hidapi_include],
                libraries=["setupapi"],
            )
        ]

    elif sys.platform.startswith("darwin"):
        macos_sdk_path = (
            subprocess.check_output(["xcrun", "--show-sdk-path"]).decode().strip()
        )
        modules = [
            Extension(
                "hid",
                sources=["hid.pyx", hidapi_src("mac")],
                include_dirs=[embedded_hidapi_include],
                # TODO: -Wno-unreachable-code: https://github.com/cython/cython/issues/3172
                extra_compile_args=['-isysroot', macos_sdk_path, '-Wno-unreachable-code'],
                # TODO: remove '-framework AppKit' after switching to 0.14.1 or newer
                extra_link_args=['-framework', 'IOKit', '-framework', 'CoreFoundation', '-framework', 'AppKit']
            )
        ]

    elif sys.platform.startswith("linux"):
        modules = []
        if "--without-libusb" in sys.argv:
            sys.argv.remove("--without-libusb")
            hidraw_module = "hid"
        else:
            hidraw_module = "hidraw"
            modules.append(
                Extension(
                    "hid",
                    sources=["hid.pyx", hidapi_src("libusb")],
                    include_dirs=[embedded_hidapi_include],
                    extra_compile_args=[pkgconfig.cflags('libusb-1.0 >= 1.0.9')],
                    extra_link_args=[pkgconfig.libs('libusb-1.0 >= 1.0.9')]
                )
            )
        modules.append(
            Extension(
                hidraw_module,
                sources=["hidraw.pyx", hidapi_src("linux")],
                include_dirs=[embedded_hidapi_include],
                libraries=["udev"],
            )
        )

    else:
        modules = [
            Extension(
                "hid",
                sources=["hid.pyx", hidapi_src("libusb")],
                include_dirs=[embedded_hidapi_include],
                extra_compile_args=[pkgconfig.cflags('libusb-1.0 >= 1.0.9')],
                extra_link_args=[pkgconfig.libs('libusb-1.0 >= 1.0.9')]
            )
        ]

    return modules


def hid_from_system_hidapi():
    if sys.platform.startswith("linux"):
        modules = []
        if "--without-libusb" in sys.argv:
            sys.argv.remove("--without-libusb")
            hidraw_module = "hid"
        else:
            hidraw_module = "hidraw"
            modules.append(
                Extension(
                    "hid",
                    sources=["hid.pyx"],
                    extra_compile_args=[pkgconfig.cflags('hidapi-libusb >= 0.14')],
                    extra_link_args=[pkgconfig.libs('hidapi-libusb >= 0.14')]
                )
            )
        modules.append(
            Extension(
                hidraw_module,
                sources=["hidraw.pyx"],
                extra_compile_args=[pkgconfig.cflags('hidapi-hidraw >= 0.14')],
                extra_link_args=[pkgconfig.libs('hidapi-hidraw >= 0.14')]
            )
        )
    else:
        modules = [
            Extension(
                "hid",
                sources=["hidraw.pyx"],
                extra_compile_args=[pkgconfig.cflags('hidapi >= 0.14')],
                extra_link_args=[pkgconfig.libs('hidapi >= 0.14')]
            )
        ]
    return modules


def find_version():
    filename = os.path.join(tld, 'hid.pyx')
    with open(filename) as f:
        text = f.read()
    match = re.search(r"^__version__ = \"(.*)\"$", text, re.MULTILINE)
    if not match:
        raise RuntimeError('cannot find version')
    return match.group(1)


if "--with-system-hidapi" in sys.argv:
    sys.argv.remove("--with-system-hidapi")
    modules = hid_from_system_hidapi()
else:
    modules = hid_from_embedded_hidapi()


setup(
    name="hidapi",
    version=find_version(),
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
    ext_modules=cythonize(modules, language_level=3),
    install_requires=["setuptools>=19.0"],
)
