cdef extern from "hidapi.h":
  ctypedef struct hid_device:
    pass
  cdef struct hid_device_info:
    char* path
    unsigned short vendor_id
    unsigned short product_id
    char *serial_number
    unsigned short release_number
    char *manufacturer_string
    char *product_string
    unsigned short usage_page
    int interface_number
    hid_device_info* next    

  hid_device* hid_open(unsigned short, unsigned short, Py_UNICODE*)
  int hid_write(hid_device* device, unsigned char *data, int length)
  int hid_read(hid_device* device, unsigned char* data, int max_length)
  int hid_set_nonblocking(hid_device* device, int value)

  #hid_device_info* hid_enumerate(unsigned short vendor_id, unsigned short product_id)
  #void hid_free_enumeration(hid_device_info*)
  int hid_get_manufacturer_string(hid_device* device, Py_UNICODE* string, int maxlen)
  int hid_get_product_string(hid_device* device, Py_UNICODE* string, int maxlen)
  int hid_get_serial_number_string(hid_device* device, Py_UNICODE* string, int maxlen)
  int hid_get_product_string(hid_device* device, Py_UNICODE* string, int maxlen)
  Py_UNICODE* hid_error(hid_device* device)
  

