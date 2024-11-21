from libc.stddef cimport wchar_t, size_t

cdef extern from "<hidapi.h>":
    const int HID_API_MAX_REPORT_DESCRIPTOR_SIZE

    ctypedef struct hid_device:
        pass

    ctypedef enum hid_bus_type:
        HID_API_BUS_UNKNOWN = 0x00,
        HID_API_BUS_USB = 0x01,
        HID_API_BUS_BLUETOOTH = 0x02,
        HID_API_BUS_I2C = 0x03,
        HID_API_BUS_SPI = 0x04

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
