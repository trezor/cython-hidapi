#!/usr/bin/python
from Cython.Build import cythonize
from setuptools import setup, Extension, Distribution
from subprocess import call, PIPE, Popen
import os
import platform
import re
import shlex
import subprocess
import sys

min_required_hidapi_version = "0.14"

libusb_pkgconfig = "libusb-1.0 >= 1.0.9"
hidapi_libusb_pkgconfig = "hidapi-libusb >= " + min_required_hidapi_version
hidapi_hidraw_pkgconfig = "hidapi-hidraw >= " + min_required_hidapi_version
hidapi_pkgconfig = "hidapi >= " + min_required_hidapi_version

tld = os.path.abspath(os.path.dirname(__file__))
embedded_hidapi_topdir = os.path.join(tld, "hidapi")
embedded_hidapi_include = os.path.join(embedded_hidapi_topdir, "hidapi")
embedded_hidapi_macos_include = os.path.join(embedded_hidapi_topdir, "mac")

ENV = {"PLATFORM": platform.system()}


def to_bool(bool_str):
    if str(bool_str).lower() in ["true", "t", "1", "on", "yes", "y"]:
        return True
    return False


def get_extension_compiler_type():
    """
    Returns a compiler to be used by setuptools to build Extensions
    Taken from https://github.com/pypa/setuptools/issues/2806#issuecomment-961805789
    """
    d = Distribution()
    build_ext = Distribution().get_command_obj("build_ext")
    build_ext.finalize_options()
    # register an extension to ensure a compiler is created
    build_ext.extensions = [Extension("ignored", ["ignored.c"])]
    # disable building fake extensions
    build_ext.build_extensions = lambda: None
    # run to populate self.compiler
    build_ext.run()
    return build_ext.compiler.compiler_type


# this could have been just pkgconfig.configure_extension(), but: https://github.com/matze/pkgconfig/issues/65
# additionally contains a few small improvements
def pkgconfig_configure_extension(ext, package):
    pkg_config_exe = os.environ.get("PKG_CONFIG", None) or "pkg-config"

    def exists(package):
        cmd = f"{pkg_config_exe} --exists '{package}'"
        return call(shlex.split(cmd)) == 0

    if not exists(package):
        raise Exception(f"pkg-config package '{package}' not found")

    def query_pkg_config(package, *options):
        cmd = f"{pkg_config_exe} {' '.join(options)} '{package}'"
        proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()

        return out.rstrip().decode("utf-8")

    def query_and_extend(option, target):
        os_opts = ["--msvc-syntax"] if get_extension_compiler_type() == "msvc" else []
        flags = query_pkg_config(package, *os_opts, option)
        flags = flags.replace('\\"', "")
        if flags:
            target.extend(re.split(r"(?<!\\) ", flags))

    query_and_extend("--cflags", ext.extra_compile_args)
    query_and_extend("--libs", ext.extra_link_args)

    return ext


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
                extra_compile_args=["-DHID_API_NO_EXPORT_DEFINE"],
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
                include_dirs=[embedded_hidapi_include, embedded_hidapi_macos_include],
                # TODO: remove -Wno-unreachable-code when the time comes: https://github.com/cython/cython/issues/3172
                extra_compile_args=[
                    "-isysroot",
                    macos_sdk_path,
                    "-Wno-unreachable-code",
                ],
                # TODO: remove '-framework AppKit' after switching to 0.14.1 or newer
                extra_link_args=[
                    "-framework",
                    "IOKit",
                    "-framework",
                    "CoreFoundation",
                    "-framework",
                    "AppKit",
                ],
            )
        ]

    elif sys.platform.startswith("linux"):
        modules = []
        if "--with-hidraw" in sys.argv:
            sys.argv.remove("--with-hidraw")
            HIDAPI_WITH_HIDRAW = True
        else:
            HIDAPI_WITH_HIDRAW = to_bool(os.getenv("HIDAPI_WITH_HIDRAW"))
        if "--with-libusb" in sys.argv:
            sys.argv.remove("--with-libusb")
            HIDAPI_WITH_LIBUSB = True
        else:
            HIDAPI_WITH_LIBUSB = to_bool(os.getenv("HIDAPI_WITH_LIBUSB"))

        # make libusb backend default if none is specified
        if not HIDAPI_WITH_HIDRAW and not HIDAPI_WITH_LIBUSB:
            HIDAPI_WITH_LIBUSB = True

        if HIDAPI_WITH_LIBUSB:
            hidraw_module = "hidraw"
            modules.append(
                pkgconfig_configure_extension(
                    Extension(
                        "hid",
                        sources=["hid.pyx", hidapi_src("libusb")],
                        include_dirs=[embedded_hidapi_include],
                    ),
                    libusb_pkgconfig,
                )
            )
        elif HIDAPI_WITH_HIDRAW:
            hidraw_module = "hid"
        else:
            raise ValueError("Unknown HIDAPI backend")

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
            pkgconfig_configure_extension(
                Extension(
                    "hid",
                    sources=["hid.pyx", hidapi_src("libusb")],
                    include_dirs=[embedded_hidapi_include],
                ),
                libusb_pkgconfig,
            )
        ]

    return modules


def hid_from_system_hidapi():
    if sys.platform.startswith("linux"):
        modules = []
        if "--with-hidraw" in sys.argv:
            sys.argv.remove("--with-hidraw")
            HIDAPI_WITH_HIDRAW = True
        else:
            HIDAPI_WITH_HIDRAW = to_bool(os.getenv("HIDAPI_WITH_HIDRAW"))
        if "--with-libusb" in sys.argv:
            sys.argv.remove("--with-libusb")
            HIDAPI_WITH_LIBUSB = True
        else:
            HIDAPI_WITH_LIBUSB = to_bool(os.getenv("HIDAPI_WITH_LIBUSB"))

        # make libusb backend default if none is specified
        if not HIDAPI_WITH_HIDRAW and not HIDAPI_WITH_LIBUSB:
            HIDAPI_WITH_LIBUSB = True

        if HIDAPI_WITH_LIBUSB:
            hidraw_module = "hidraw"
            modules.append(
                pkgconfig_configure_extension(
                    Extension("hid", sources=["hid.pyx"]), hidapi_libusb_pkgconfig
                )
            )
        elif HIDAPI_WITH_HIDRAW:
            hidraw_module = "hid"
        else:
            raise ValueError("Unknown HIDAPI backend")

        modules.append(
            pkgconfig_configure_extension(
                Extension(hidraw_module, sources=["hidraw.pyx"]),
                hidapi_hidraw_pkgconfig,
            )
        )
    else:
        modules = [
            pkgconfig_configure_extension(
                Extension("hid", sources=["hid.pyx"]), hidapi_pkgconfig
            )
        ]

    return modules


def find_version():
    filename = os.path.join(tld, "hid.pyx")
    with open(filename) as f:
        text = f.read()
    match = re.search(r"^__version__ = \"(.*)\"$", text, re.MULTILINE)
    if not match:
        raise RuntimeError("cannot find version")
    return match.group(1)


if "--with-system-hidapi" in sys.argv:
    sys.argv.remove("--with-system-hidapi")
    HIDAPI_SYSTEM_HIDAPI = True
else:
    HIDAPI_SYSTEM_HIDAPI = to_bool(os.getenv("HIDAPI_SYSTEM_HIDAPI"))

if HIDAPI_SYSTEM_HIDAPI:
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
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    ext_modules=cythonize(modules, language_level=3, compile_time_env=ENV),
    setup_requires=["setuptools>=19.0"],
)
