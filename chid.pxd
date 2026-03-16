from libc.stddef cimport wchar_t, size_t

cdef extern from "<hidapi.h>":
    const int HID_API_MAX_REPORT_DESCRIPTOR_SIZE
    const int HID_API_VERSION_MAJOR
    const int HID_API_VERSION_MINOR
    const int HID_API_VERSION_PATCH

    ctypedef struct hid_device:
        pass

    ctypedef enum hid_bus_type:
        HID_API_BUS_UNKNOWN,
        HID_API_BUS_USB,
        HID_API_BUS_BLUETOOTH,
        HID_API_BUS_I2C,
        HID_API_BUS_SPI

    cdef struct hid_device_info:
        char *path
        unsigned short vendor_id
        unsigned short product_id
        wchar_t *serial_number
        unsigned short release_number
        wchar_t *manufacturer_string
        wchar_t *product_string
        unsigned short usage_page
        unsigned short usage
        int interface_number
        hid_device_info *next
        hid_bus_type bus_type

    hid_device_info* hid_enumerate(unsigned short, unsigned short) nogil
    void hid_free_enumeration(hid_device_info*)

    hid_device* hid_open(unsigned short, unsigned short, const wchar_t*)
    hid_device* hid_open_path(char *path)
    void hid_close(hid_device *)
    int hid_init()
    int hid_exit()
    int hid_write(hid_device* device, unsigned char *data, int length) nogil
    int hid_read(hid_device* device, unsigned char* data, int max_length) nogil
    int hid_read_timeout(hid_device* device, unsigned char* data, int max_length, int milliseconds) nogil
    int hid_set_nonblocking(hid_device* device, int value)
    int hid_get_report_descriptor(hid_device* device, unsigned char *data, int length) nogil
    int hid_send_feature_report(hid_device* device, unsigned char *data, int length) nogil
    int hid_get_feature_report(hid_device* device, unsigned char *data, int length) nogil
    int hid_get_input_report(hid_device* device, unsigned char *data, int length) nogil

    int hid_get_manufacturer_string(hid_device*, wchar_t *, size_t)
    int hid_get_product_string(hid_device*, wchar_t *, size_t)
    int hid_get_serial_number_string(hid_device*, wchar_t *, size_t)
    int hid_get_indexed_string(hid_device*, int, wchar_t *, size_t)
    wchar_t *hid_error(hid_device *)
    char* hid_version_str()

IF PLATFORM == "Darwin":
    cdef extern from "<hidapi_darwin.h>":
        int hid_darwin_get_location_id (hid_device *dev, unsigned *location_id)
        void hid_darwin_set_open_exclusive(int open_exclusive)
        int hid_darwin_get_open_exclusive()
        int hid_darwin_is_device_open_exclusive(hid_device *dev)
