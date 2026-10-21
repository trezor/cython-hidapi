# Native libusb receive queue diagnostics

This contribution exposes the experimentally validated `hid.device.get_queue_stats()` API in Cython. The method returns a dictionary containing `received`, `dropped`, and `max_queue` counters for the existing open device.

```python
device = hid.device()
device.open(0x1A61, 0x3950)
try:
    result = device.get_queue_stats()
    if result["dropped"]:
        raise IOError("HID input reports were dropped")
finally:
    device.close()
```

## Requirements and implementation

This method requires an underlying HIDAPI C library that exports `hid_get_queue_stats()`, as implemented in the related C patch at [stman/hidapi](https://github.com/stman/hidapi/tree/fix/libusb-input-report-overflow).

The tested proof-of-concept uses Python 3.14 and `hidapi` 0.15.0 with the vendored **libusb** backend, and validates the native counters under the existing receive-thread mutex. It does not open a second HID device.

The native queue code was modified from `num_queued > 30` to `num_queued > 1022`, with received/dropped/max_queue accounting. The successful end-to-end run reported `received=22658`, `dropped=0`, `max_queue=84`, matching between Python and the native C close log.

## Build integration and compatibility

The embedded HIDAPI submodule is pinned to the matching corrected C implementation
in the contributor fork. Initialize it with `git submodule update --init` before
building. The fork URL makes the commit available before the C contribution lands
upstream; the pin should be moved to an upstream commit after acceptance.

The default Linux build includes both libusb (`hid`) and hidraw (`hidraw`).
The statistics method retains the validated dictionary and error behavior:
a closed device raises `ValueError`; an unavailable API or unsupported backend
raises `IOError`. Windows, macOS, Linux hidraw and NetBSD remain supported but do
not supply libusb queue statistics. Older system HIDAPI libraries remain buildable:
the wrapper checks `HID_API_HAS_QUEUE_STATS` in the installed header and returns
an unavailable result without referencing a missing native symbol. System builds
need matching patched headers and libraries to obtain statistics.

Counters last for one open device lifetime. `received` includes reports later
dropped; `max_queue` measures depth before overflow removal and can reach 1025.
The native implementation keeps 1024 reports and logs counters on libusb close.

Build sequentially using `python setup.py build_ext --inplace -j 1`.
Run `python -m unittest test_queue_stats` for hardware-free import and closed-device
checks; do not run `tests.py` when device enumeration is prohibited.

## Contribution build validation

Linux x86_64, Python 3.14, Cython 3.3.0, GCC 15.2: both embedded libusb
and hidraw extensions built successfully with `build_ext --inplace -j 1`.
The hardware-free unittest imported both built modules and verified closed-device
errors. A standalone compile/link/run of the compatibility wrapper against the
unmodified upstream header passed without linking the new native symbol.
The pinned native implementation also passed its synthetic queue tests.
Only existing setuptools deprecation warnings were emitted. Windows, macOS and
NetBSD require platform CI; no hardware or acquisition tests were run here.
