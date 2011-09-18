from libc.stddef cimport wchar_t, size_t

cdef extern from "hidapi.h":
  ctypedef struct hid_device:
    pass

  hid_device* hid_open(unsigned short, unsigned short, void*)
  int hid_write(hid_device* device, unsigned char *data, int length)
  int hid_read(hid_device* device, unsigned char* data, int max_length)
  int hid_set_nonblocking(hid_device* device, int value)

  int hid_get_manufacturer_string(hid_device*, wchar_t *, size_t)
  int hid_get_product_string(hid_device*, wchar_t *, size_t)
  int hid_get_serial_number_string(hid_device*, wchar_t *, size_t)
  wchar_t *hid_error(hid_device *)


  

